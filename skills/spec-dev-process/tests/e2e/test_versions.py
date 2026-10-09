"""e2e:文件版本追蹤反映到審計與看板。testcase1 複本上:
review → v1 → 確認 REQ-002 的追溯圖(記下 v1)→ PM 改 §3.2 一句 → review → v2:
看板資料有 v2、pm-spec.md 的 diff 與變更段落、上游鍵 pm:REQ-002 在 v2 變更;
REQ-002 的已通過確認變成「上游已變」(WARN),其他需求的確認不受影響;沒變就不記新版。"""
import json, pathlib, shutil, tempfile, unittest
from core import config as C
from tools.execute import runner_v1 as R
from tools.review import signoff_v1 as SO

TC1 = C.ROOT / "examples" / "testcase1-form-system"

class VersionsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp()); self.proj = self.tmp / "tc1"
        shutil.copytree(TC1, self.proj, ignore=shutil.ignore_patterns("audit"))
        self.spec = self.proj / "specs" / "rd" / "issue-c" / "spec"

    def tearDown(self): shutil.rmtree(self.tmp)

    def review(self):
        cfg = C.load_config(self.spec, None); cfg["reviewer"] = {**(cfg.get("reviewer") or {}), "render_check": "off"}
        return R.run_pipeline(R.make_ctx(self.spec, cfg), to="S6", no_stop=True)

    def item(self, ctx, i): return next(x for x in ctx["data"]["audit"]["items"] if x["id"] == i)

    def test_pm_change_marks_signed_items_upstream_and_shows_diff(self):
        c = self.review(); V = c["data"]["versions"]; self.assertEqual(V["current"], 1)
        self.assertIn("specs/in-progress/issue-c/pm-spec.md", [d["path"] for d in V["docs"]])
        self.assertEqual(self.review()["data"]["versions"]["current"], 1, "沒變就不記新版")
        rv = c["review_dir"]
        for i in ("AUTO-TRACE-REQ-002", "AUTO-TRACE-REQ-001"):
            it = self.item(c, i); msg = SO.apply(rv, i, "Paul", "approved", it["hash"], duty="intent"); self.assertIn("(v1)", msg)
            SO.apply(rv, i, "Paul", "approved", it["hash"], duty="testable")
        self.assertRegex((rv / "audit" / "signoff.md").read_text(encoding="utf-8"), r"\| AUTO-TRACE-REQ-002 \| intent \| .* \| approved \| Paul \| [\d-]+ \|  \| v1 \|")
        self.assertEqual(self.item(self.review(), "AUTO-TRACE-REQ-002")["signoff"], "approved")
        pm = self.proj / "specs" / "in-progress" / "issue-c" / "pm-spec.md"; t = pm.read_text(encoding="utf-8")
        lines = t.splitlines(); i = next(n for n, l in enumerate(lines) if l.startswith("### 3.2"))
        lines.insert(i + 1, "審核者核准前需確認附件齊全。"); pm.write_text("\n".join(lines) + "\n", encoding="utf-8")
        c2 = self.review(); V = c2["data"]["versions"]
        self.assertEqual(V["current"], 2)
        ch = V["timeline"][0]; self.assertEqual(ch["v"], 2)
        pmc = next(x for x in ch["changed"] if x["path"].endswith("pm-spec.md"))
        self.assertTrue(any(s.startswith("3.2") for s in pmc["sections"]), pmc["sections"]); self.assertEqual((pmc["add"], pmc["dele"]), (1, 0))
        self.assertIn("+審核者核准前需確認附件齊全。", V["diffs"]["2:specs/in-progress/issue-c/pm-spec.md"]["lines"])
        self.assertIn("pm:REQ-002", ch["keys"]); self.assertNotIn("pm:REQ-001", ch["keys"])
        it2 = self.item(c2, "AUTO-TRACE-REQ-002")
        self.assertEqual(it2["signoff"], "upstream"); self.assertEqual(it2["signoffs"]["intent"]["upstream"], [{"key": "pm:REQ-002", "v": 2}])
        self.assertEqual(self.item(c2, "AUTO-TRACE-REQ-001")["signoff"], "approved", "別的需求不受影響")
        g = [x for x in c2["gate"] if x["rule"] == "G-DG-signoff" and x["level"] == "WARN"]
        self.assertTrue(any("AUTO-TRACE-REQ-002" in x["msg"] and "pm:REQ-002(v2)" in x["msg"] for x in g), [x["msg"] for x in g])
        # 重看後再確認 → 記 v2 → 回到通過
        SO.apply(rv, "AUTO-TRACE-REQ-002", "Paul", "approved", it2["hash"], duty="intent"); SO.apply(rv, "AUTO-TRACE-REQ-002", "Paul", "approved", it2["hash"], duty="testable")
        self.assertEqual(self.item(self.review(), "AUTO-TRACE-REQ-002")["signoff"], "approved")
