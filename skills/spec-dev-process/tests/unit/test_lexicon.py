"""unit:SA0 前置解析(analyze.lexicon)。以 testcase1 issue-c 的人工斷詞(sa/01)為對照組,鎖住召回與分類品質下限。"""
import pathlib, unittest
from core import config as C
from tools.analyze import lexicon_v1 as L

TC = C.ROOT / "examples" / "testcase1-form-system"
MANUAL = {"nouns": {"表單", "填寫紀錄", "審核紀錄", "理由", "工作天", "待審清單"},
          "actions": {"送出", "核准", "退回", "修改", "重新送出", "提醒", "指派"},
          "roles": {"填寫者", "審核者", "部門主管", "系統"}}

class LexiconTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lex = L.load_lexicon({})
        docs = [("pm_spec:pm-spec.md", (TC / "specs/in-progress/issue-c/pm-spec.md").read_text(encoding="utf-8")),
                ("mock:approval.html", (TC / "specs/in-progress/issue-c/mock/approval.html").read_text(encoding="utf-8")),
                ("ref:coding.md", (TC / "docs/guidelines/coding.md").read_text(encoding="utf-8"))]
        cls.rows = L.analyze(docs, lex, {"表單": {"symbol": "Form", "specs": ["issue-b"]}, "填寫紀錄": {"symbol": "FormSubmission", "specs": ["issue-b"]}})
        cls.terms = {k: {it["term"] for it in cls.rows[k]} for k in ("nouns", "actions", "roles", "statuses")}

    def test_recall_against_manual_word_break(self):
        self.assertGreaterEqual(len(MANUAL["nouns"] & self.terms["nouns"]), 5)      # 已知漏:待審清單(「看待審清單」被 待 切開)
        self.assertEqual(MANUAL["actions"] & self.terms["actions"], MANUAL["actions"])
        self.assertEqual(MANUAL["roles"] & self.terms["roles"], MANUAL["roles"])

    def test_status_values_are_attributes_not_actions(self):
        self.assertIn("待審核", self.terms["statuses"]); self.assertNotIn("待審核", self.terms["actions"])

    def test_boundary_entropy_removes_fragments(self):
        for frag in ("醒審核者", "單審核者", "准或退回", "核准或退"):
            for k in self.terms: self.assertNotIn(frag, self.terms[k], frag)

    def test_role_phrases_folded_into_base_role(self):
        self.assertNotIn("提醒審核者", self.terms["roles"]); self.assertNotIn("表單審核者", self.terms["roles"])

    def test_glossary_symbol_promotes_and_is_reported(self):
        n = {it["term"]: it for it in self.rows["nouns"]}
        self.assertEqual(n["填寫紀錄"]["symbol"], "FormSubmission"); self.assertEqual(n["填寫紀錄"]["suggest"], "升")

    def test_demoted_terms_are_kept_not_dropped(self):
        a = {it["term"]: it for it in self.rows["actions"]}
        self.assertIn("指派", a); self.assertEqual(a["指派"]["suggest"], "降")   # 低頻但關鍵(缺口 #1):降級不等於丟棄

    def test_english_tokens_kept_separately(self):
        en = {it["term"] for it in self.rows["english"]}
        self.assertTrue(en & {"Handler", "Domain", "INotifier", "Repository"}, en)
