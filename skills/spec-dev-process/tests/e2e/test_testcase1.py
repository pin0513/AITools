"""e2e:testcase1 表單系統 issue-c 端到端。做一次(review.sh)→ 驗證一次(0 FAIL)→ 證明一次(survey 證據逐條回 codebase 比對、SA 素材進面板)。"""
import json, pathlib, re, shutil, subprocess, sys, tempfile, unittest
from core import config as C

ROOT = C.ROOT; TC = ROOT / "examples" / "testcase1-form-system"

class Testcase1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = pathlib.Path(tempfile.mkdtemp()); cls.proj = cls.tmp / "testcase1-form-system"
        shutil.copytree(TC, cls.proj, ignore=shutil.ignore_patterns("html", "traceability.json", "90-*", "boundary-report.md", "check-panel.html", "survey-candidates.md"))
        env = {"SPEC_DEV": str(ROOT / "spec-dev.py"), "PATH": "/usr/bin:/bin:/usr/local/bin"}
        cls.r = subprocess.run(["bash", str(cls.proj / "specs/tools/spec-reviewer/review.sh"), "issue-c"], capture_output=True, text=True, encoding="utf-8", env=env)
        cls.review = cls.proj / "specs/rd/issue-c/spec-review"
        cls.tr = json.loads((cls.review / "traceability.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls): shutil.rmtree(cls.tmp)

    def test_do_once_review_sh_succeeds_with_zero_fail(self):
        self.assertEqual(self.r.returncode, 0, self.r.stdout + self.r.stderr)
        self.assertEqual([g for g in self.tr["gate"] if g["level"] == "FAIL"], [])
        self.assertEqual(self.tr["kpis"]["boundary_fail"], 0); self.assertEqual(self.tr["kpis"]["uncovered_req"], 0)
        for f in ("check-panel.html", "90-traceability.md", "boundary-report.md", "survey-candidates.md", "html/sa-07-state.html"):
            self.assertTrue((self.review / f).exists(), f)

    def test_sa_modeling_all_seven_steps_with_diagrams(self):
        self.assertEqual(len(self.tr["sa_files"]), 9)   # SA0 產生物 + 7 步 + survey-mapping.md
        self.assertIn("sa/00-lexicon.md", self.tr["sa_files"]); self.assertTrue((self.review / "lexicon.json").exists())
        self.assertGreater(self.tr["lexicon"]["stats"]["cjk_candidates"], self.tr["lexicon"]["stats"]["kept"])
        kinds = sorted(a["kind"] for a in self.tr["sa_artifacts"])
        self.assertEqual(kinds, ["class", "flowchart", "flowchart", "sequence", "state"])
        self.assertTrue(all(g["level"] == "INFO" for g in self.tr["gate"] if g["rule"] == "G-SA-steps"))

    def test_prove_survey_evidence_resolves_to_real_code(self):
        rows = [r for r in self.tr["survey"] if r["status"] in ("existing", "modify")]
        self.assertGreaterEqual(len(rows), 10)
        verified = [g for g in self.tr["gate"] if g["rule"] == "G-SV-evidence" and "已驗證" in g["msg"]]
        n_ev = sum(len([e for e in r["evidence"].split(";") if e.strip()]) for r in rows)
        self.assertEqual(len(verified), n_ev)
        sa2 = {e["name"]: e["en"] for e in self.tr["sa_entities"]}
        for r in rows:                                    # 獨立於規則引擎再比對一次
            for ev in [e.strip() for e in r["evidence"].split(";") if e.strip()]:
                m = re.match(r'^(.+?):(\d+)(?:\s+"(.+)")?$', ev); path, line, literal = m.group(1), int(m.group(2)), m.group(3)
                text = (self.proj / path).read_text(encoding="utf-8").splitlines()[line - 1]
                if literal: self.assertIn(literal, text, f"{r['element']} {ev}"); continue
                name = r["element"] if re.search(r"[A-Za-z]{3}", r["element"]) else sa2.get(re.sub(r"\s*\(.*\)", "", r["element"]), "")
                toks = [t for t in re.split(r"[^A-Za-z0-9_]+", name) if len(t) >= 3]
                self.assertTrue(toks and any(re.search(r"\b" + re.escape(t) + r"\b", text, re.I) for t in toks), f"{r['element']} {ev}: {text}")

    def test_prove_sa_hand_off_into_rd_spec(self):
        """SA 的實體要出現在 RD spec 的 Component 或領域模型;survey 的 new 元素要是 Component 表的 new。"""
        comp_names = " ".join(c["name"] for c in self.tr["components"])
        for e in self.tr["sa_entities"]:
            self.assertTrue(e["en"] in comp_names or e["en"] in (self.proj / "specs/rd/issue-c/spec/20-domain-model.md").read_text(encoding="utf-8"), e["en"])
        new_cmds = [r["element"] for r in self.tr["survey"] if r["kind"] == "Command" and r["status"] == "new"]
        for cmd in new_cmds: self.assertIn(cmd, comp_names, cmd)

    def test_evidence_chain_is_fully_inline(self):
        """證據鏈:每條需求的 PM 錨點都能在內嵌的 PM 原文找到段落;mock 內嵌;AC 有 gherkin 原文與行號;元件/測試列有行號。"""
        src = self.tr["sources"]; anchors = {s["anchor"] for s in src["pm_spec"]["sections"]}
        self.assertEqual(src["pm_spec"]["path"], "specs/in-progress/issue-c/pm-spec.md"); self.assertGreater(len(anchors), 8)
        for r in self.tr["requirements"]:
            self.assertIn(r["source"].split(" ")[0], anchors, r["id"])
        self.assertTrue(any("html" in m for m in src["mocks"]))
        for r in self.tr["requirements"]:
            if "non_functional" in r["types"]: continue
            for ac in r["acs"]: self.assertIn(ac, self.tr["ac_text"], ac); self.assertTrue(self.tr["ac_text"][ac]["line"] > 0)
        self.assertTrue(all(l["line"] for l in self.tr["ac_links"]) and all(t["line"] for t in self.tr["tests"]) and all(c["line"] for c in self.tr["components"]))
        self.assertEqual(sorted(self.tr["uc_text"]), ["UC-001", "UC-002", "UC-003", "UC-004"])
        html = (self.review / "check-panel.html").read_text(encoding="utf-8")
        self.assertIn("E. 證據鏈", html); self.assertIn("srcdoc=", html)   # mock 內嵌在面板裡

    def test_bilingual_elements_and_cross_spec_glossary(self):
        """中文元素經詞彙表 / SA2 解析後可驗;跨 spec 詞彙表由 issue-b + issue-c 合併;本 spec 命名與 issue-b 一致。"""
        gl = self.proj / "specs" / "glossary.md"
        self.assertTrue(gl.exists()); text = gl.read_text(encoding="utf-8")
        self.assertIn("| 填寫紀錄 | FormSubmission |", text); self.assertIn("issue-b, issue-c", text); self.assertIn("| (無) |", text)
        g = {x["msg"]: x for x in self.tr["gate"] if x["rule"] == "G-SV-evidence"}
        self.assertTrue(any("填寫紀錄" in m and "已驗證" in m and "解析" in m for m in g), list(g)[:5])
        self.assertTrue(any("必填檢查" in m and '字面 "FIELD_REQUIRED"' in m for m in g))
        self.assertTrue(any(x["rule"] == "G-GL-consistency" and x["level"] == "INFO" and "填寫紀錄" in x["msg"] for x in self.tr["gate"]))
        self.assertFalse(any(x["rule"] == "G-GL-consistency" and x["level"] == "FAIL" for x in self.tr["gate"]))
        self.assertGreaterEqual(len(self.tr["glossary"]["terms"]), 8); self.assertEqual(self.tr["glossary"]["conflicts"], [])

    def test_check_board_shows_sa_materials_and_survey(self):
        html = (self.review / "check-panel.html").read_text(encoding="utf-8")
        payload = json.loads(html.split("const DATA = ", 1)[1].split(";\n</script>", 1)[0])
        self.assertEqual(payload["kpis"], self.tr["kpis"])
        self.assertEqual(len(payload["trace"]["sa_artifacts"]), 5); self.assertEqual(len(payload["trace"]["survey"]), len(self.tr["survey"]))
        self.assertIn("SA 建模素材", html); self.assertIn("Survey Mapping", html)

    def test_looping_breaking_evidence_is_caught(self):
        """改壞一條證據行號 → 再跑 → 必須 FAIL(回圈的閉環)。"""
        p = self.review / "survey-mapping.md"; orig = p.read_text(encoding="utf-8")
        p.write_text(orig.replace("src/api/Forms.Domain/FormSubmission.cs:4", "src/api/Forms.Domain/FormSubmission.cs:1"), encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, str(ROOT / "spec-dev.py"), "check", str(self.proj / "specs/rd/issue-c/spec")], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 1); self.assertIn("G-SV-evidence", r.stdout); self.assertIn("FormSubmission.cs:1", r.stdout)
        finally:
            p.write_text(orig, encoding="utf-8")
