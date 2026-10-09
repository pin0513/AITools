"""e2e:真的跑 CLI。範例必須得到刻意留的 FAIL;乾淨骨架 + 專案覆寫要能 init → check;產生物齊全。"""
import json, pathlib, shutil, subprocess, sys, tempfile, unittest
from core import config as C

ROOT = C.ROOT; CLI = ROOT / "spec-dev.py"; EX = ROOT / "examples" / "avatar-upload"

def cli(*args):
    return subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True, text=True, encoding="utf-8")

class ExampleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp()); self.d = self.tmp / "avatar-upload"
        shutil.copytree(EX, self.d, ignore=shutil.ignore_patterns("html", "traceability.json", "90-*", "boundary-report.md", "check-panel.html"))
    def tearDown(self): shutil.rmtree(self.tmp)

    def test_all_produces_everything_and_reports_intended_fails(self):
        r = cli("all", self.d, "--offline")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        for f in ("traceability.json", "90-traceability.md", "boundary-report.md", "check-panel.html", "html/30-architecture-c4.html"):
            self.assertTrue((self.d / f).exists(), f)
        tr = json.loads((self.d / "traceability.json").read_text(encoding="utf-8"))
        fails = sorted((b["rule"], b["target"]) for b in tr["boundary_checks"] if b["status"] == "FAIL")
        self.assertEqual(fails, [("B2", "CMP-003"), ("B7", "AC-003-1")])
        self.assertEqual(tr["kpis"]["uncovered_ids"], ["REQ-003"])
        html = (self.d / "check-panel.html").read_text(encoding="utf-8")
        self.assertIn("mermaid.initialize", html)
        payload = json.loads(html.split("const DATA = ", 1)[1].split(";\n</script>", 1)[0])
        self.assertEqual(payload["kpis"], tr["kpis"])                       # 面板與 json 一致
        self.assertEqual(len(payload["gate"]), len(tr["gate"]))
        self.assertTrue(any(g["rule"] == "G-S3-boundary" for g in payload["gate"]))
        self.assertEqual(payload["kpis"]["uncovered_ids"], ["REQ-003"])
        self.assertGreater((self.d / "check-panel.html").stat().st_size, 2_000_000)  # offline 內嵌

    def test_strict_run_stops_at_s3(self):
        r = cli("run", self.d, "--to", "S6")
        self.assertEqual(r.returncode, 1)
        self.assertIn("stop at S3", r.stdout)
        self.assertFalse((self.d / "check-panel.html").exists())

    def test_fixing_the_md_clears_the_fail(self):
        p = self.d / "30-architecture-c4.md"
        p.write_text(p.read_text(encoding="utf-8").replace("| CMP-003 | Member (Aggregate) | Domain | Member | CMP-005 |", "| CMP-003 | Member (Aggregate) | Domain | Member | |"), encoding="utf-8")
        t = self.d / "60-test-design.md"
        t.write_text(t.read_text(encoding="utf-8").replace("| TST-005 |", "| TST-006 | GetAvatarUrlQueryHandlerTests | unit | CMP-006 | AC-003-1 |\n| TST-005 |"), encoding="utf-8")
        r = cli("check", self.d)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_each_finding_printed_once(self):
        """stage trace 只印計數,總表列明細:同一筆 [LEVEL] 規則 訊息 不得出現兩次。"""
        import collections, re
        r = cli("all", self.d)
        lines = [l.strip() for l in r.stdout.splitlines() if re.match(r"^\s*\[(FAIL|WARN|INFO)\]", l)]
        dup = [l for l, n in collections.Counter(lines).items() if n > 1]
        self.assertEqual(dup, [], r.stdout)
        self.assertIn("總表", r.stdout)

    def test_extract_only(self):
        r = cli("extract", self.d)
        self.assertEqual(r.returncode, 0, r.stdout); self.assertIn("REQ 5", r.stdout)

class FreshSkeletonTest(unittest.TestCase):
    def setUp(self): self.tmp = pathlib.Path(tempfile.mkdtemp())
    def tearDown(self): shutil.rmtree(self.tmp)

    def test_init_then_check_with_project_override(self):
        d = self.tmp / "proj" / "docs" / "rd-spec" / "order-cancel"
        r = cli("init", d, "--title", "訂單取消"); self.assertEqual(r.returncode, 0, r.stdout)
        (self.tmp / "proj" / ".spec-dev.yaml").write_text("rules:\n  disable: [G-M-log]\ntech_boundary:\n  tech_allowlist: [ASP.NET Core, EF Core, MediatR]\n", encoding="utf-8")
        r = cli("check", d)
        self.assertIn("config override", r.stdout)
        self.assertNotIn("G-M-log", r.stdout)           # 規則被專案停用
        self.assertEqual(r.returncode, 0, r.stdout)      # 骨架本身 0 FAIL

    def test_missing_required_file_is_contract_fail(self):
        d = self.tmp / "x"; cli("init", d, "--title", "x")
        (d / "10-requirements.md").unlink()
        r = cli("run", d, "--to", "S6")
        self.assertEqual(r.returncode, 1); self.assertIn("缺檔 10-requirements.md", r.stdout); self.assertIn("stop at S0", r.stdout)

    def test_fresh_skeleton_strict_run_stops_at_s1_without_method_log(self):
        d = self.tmp / "y"; cli("init", d, "--title", "y")
        r = cli("run", d, "--to", "S6")
        self.assertEqual(r.returncode, 1); self.assertIn("G-M-log", r.stdout); self.assertIn("stop at S1", r.stdout)
        self.assertTrue((d / "sa" / "07-state.md").exists())   # init 也建了 SA 模板

class ListingTest(unittest.TestCase):
    def test_rules_and_tools_listing(self):
        self.assertIn("B8", cli("rules").stdout); self.assertIn("analyze.extract", cli("tools").stdout)
