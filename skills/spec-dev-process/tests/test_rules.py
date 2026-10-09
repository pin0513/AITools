import pathlib, sys, unittest, builtins
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from specdev import rules as R, extract as X, mdtables as M, yamlmini  # noqa: E402

def base():
    return {"requirements": [{"id": "REQ-001", "title": "t", "types": ["functional"], "source": "PM§1", "acs": ["AC-001-1"]}],
            "components": [
                {"id": "CMP-001", "name": "Ctl", "layer": "Api", "context": "A", "depends": ["CMP-002"], "external": [], "tech": [], "interface": ""},
                {"id": "CMP-002", "name": "Handler", "layer": "Application", "context": "A", "depends": ["CMP-003", "CMP-004"], "external": [], "tech": [], "interface": ""},
                {"id": "CMP-003", "name": "Agg", "layer": "Domain", "context": "A", "depends": [], "external": [], "tech": [], "interface": ""},
                {"id": "CMP-004", "name": "Repo : IRepo", "layer": "Infrastructure", "context": "A", "depends": [], "external": [], "tech": [], "interface": "IRepo"}],
            "ac_links": [{"ac": "AC-001-1", "component": "CMP-002", "via": "SEQ-001", "role": ""}],
            "apis": [], "failure_modes": [], "ownership": [], "erd_entities": [],
            "tests": [{"id": "TST-001", "name": "T", "kind": "unit", "components": ["CMP-001", "CMP-002", "CMP-003", "CMP-004"], "acs": ["AC-001-1"]}],
            "fitness": [], "gaps": [], "use_cases": [], "artifacts": [], "extract_errors": []}

CFG = {"tech_boundary": {"layers": ["Api", "Application", "Domain", "Infrastructure"], "stack": {"runtime": ".NET"}, "tech_allowlist": ["EF Core"]}}

def by(rule, out, status=None):
    return [b for b in out if b["rule"] == rule and (status is None or b["status"] == status)]

class RulesTest(unittest.TestCase):
    def test_clean_design_has_no_fail(self):
        out = R.run(base(), [], CFG)
        self.assertEqual(by("B2", out, "FAIL"), [])
        self.assertEqual(by("B1", out, "FAIL"), [])
        self.assertTrue(any(b["evidence"].startswith("Application → CMP-004 經介面") for b in by("B2", out, "PASS")))

    def test_domain_depending_on_infrastructure_fails_b2(self):
        tr = base(); tr["components"][2]["depends"] = ["CMP-004"]
        out = R.run(tr, [], CFG)
        self.assertEqual(len(by("B2", out, "FAIL")), 1)
        self.assertIn("反向依賴", by("B2", out, "FAIL")[0]["evidence"])

    def test_application_to_concrete_infrastructure_warns(self):
        tr = base(); tr["components"][3]["name"] = "Repo"; tr["components"][3]["interface"] = ""
        self.assertEqual(len(by("B2", R.run(tr, [], CFG), "WARN")), 1)

    def test_cross_context_infrastructure_fails_b3(self):
        tr = base(); tr["components"][3]["context"] = "B"
        self.assertEqual(len(by("B3", R.run(tr, [], CFG), "FAIL")), 1)

    def test_external_b4(self):
        tr = base(); tr["components"][1]["external"] = ["Blob"]
        self.assertEqual(len(by("B4", R.run(tr, [], CFG), "FAIL")), 1)
        tr = base(); tr["components"][3]["external"] = ["Blob"]
        self.assertEqual(len(by("B4", R.run(tr, [], CFG), "WARN")), 1)
        tr["failure_modes"] = [{"system": "Blob", "component": ["CMP-004"], "timeout": "10s", "retry": "3", "degrade": "503", "compensate": ""}]
        self.assertEqual(len(by("B4", R.run(tr, [], CFG), "PASS")), 1)

    def test_ownership_b5(self):
        tr = base(); tr["erd_entities"] = ["Foo"]
        self.assertEqual(len(by("B5", R.run(tr, [], CFG), "FAIL")), 1)
        tr["ownership"] = [{"table": "Foo", "owner": "A", "access": ""}]
        self.assertEqual(len(by("B5", R.run(tr, [], CFG), "PASS")), 1)

    def test_nfr_binding_b6(self):
        tr = base(); tr["requirements"].append({"id": "NFR-001", "title": "n", "types": ["non_functional"], "source": "", "acs": [], "binds": []})
        out = R.run(tr, [], CFG)
        self.assertEqual(len([b for b in by("B6", out, "WARN") if "未綁定" in b["evidence"]]), 1)
        self.assertEqual(len(by("B1", out, "FAIL")), 1)
        tr["requirements"][1]["binds"] = ["CMP-001"]; tr["fitness"] = [{"nfr": "NFR-001", "how": "k6", "threshold": "", "where": ""}]
        self.assertEqual(by("B6", R.run(tr, [], CFG), "WARN"), [])

    def test_untested_ac_fails_b7(self):
        tr = base(); tr["tests"][0]["acs"] = []
        self.assertEqual(len(by("B7", R.run(tr, [], CFG), "FAIL")), 1)

    def test_tech_whitelist_b8(self):
        tr = base(); tr["components"][3]["tech"] = ["ef core", "Azure.Storage.Blobs"]
        out = R.run(tr, [], CFG)
        self.assertEqual(len(by("B8", out, "FAIL")), 1)
        self.assertIn("Azure.Storage.Blobs", by("B8", out, "FAIL")[0]["evidence"])
        log = [{"seq": 1, "req": "*", "stage": "S3", "method": "Spike.Blob", "rule": "B8", "in": "CMP-004", "out": "OPEN", "evidence": "explicit", "gaps": []}]
        self.assertEqual(len(by("B8", R.run(tr, log, CFG), "WARN")), 1)
        log[0]["out"] = "PASS"
        self.assertEqual(len(by("B8", R.run(tr, log, CFG), "PASS")), 1)

    def test_gate_zero_log_and_assumed(self):
        tr = base()
        g = R.gate(tr, [], [])
        self.assertTrue(any("0 筆" in x["msg"] and x["ids"] == ["REQ-001"] for x in g))
        log = [{"seq": 1, "req": "REQ-001", "stage": "S1", "method": "UseCase", "rule": "M1", "in": "PM§1", "out": "UC-001", "evidence": "assumed", "gaps": ["x"]}]
        g = R.gate(tr, log, [])
        self.assertFalse(any("0 筆" in x["msg"] for x in g))
        self.assertTrue(any(x["level"] == "WARN" and "assumed" in x["msg"] for x in g))

    def test_kpis_uncovered_uses_structured_ids(self):
        tr = base(); tr["tests"][0]["acs"] = []
        out = R.run(tr, [], CFG); g = R.gate(tr, [], out)
        self.assertEqual(R.kpis(tr, out, g)["uncovered_ids"], ["REQ-001"])

class ExtractTest(unittest.TestCase):
    def test_table_classification(self):
        d = M.parse("x.md", "## 追溯\n| AC | CMP | via | 職責 |\n|---|---|---|---|\n| AC-1-1 | CMP-001 | SEQ-001 | 檢查 |\n")
        self.assertEqual(M.classify(d.tables[0]), "ac_links")
        self.assertEqual(d.tables[0].rows[0]["CMP"], "CMP-001")
        self.assertIsNone(M.classify(M.parse("x.md", "| a | b |\n|---|---|\n| 1 | 2 |\n").tables[0]))

    def test_mermaid_attaches_to_heading(self):
        d = M.parse("x.md", "## S\n### SEQ-001 上傳(UC-001 / REQ-001)\n```mermaid\nsequenceDiagram\nA->>B: x\n```\n")
        self.assertEqual(d.mermaid[0].heading, "SEQ-001 上傳(UC-001 / REQ-001)")

    def test_example_extracts_and_checks(self):
        ex = ROOT / "examples" / "avatar-upload"
        tr = X.extract(ex)
        self.assertEqual([r["id"] for r in tr["requirements"]], ["REQ-001", "REQ-002", "REQ-003", "NFR-001", "NFR-002"])
        self.assertEqual(len(tr["components"]), 6)
        self.assertEqual(sorted({a["kind"] for a in tr["artifacts"]}), ["c4-component", "c4-container", "c4-context", "class", "erd", "flowchart", "sequence", "state"])
        self.assertEqual(tr["extract_errors"], [])
        out = R.run(tr, X.load_log(ex), yamlmini.load(ROOT / "config.yaml"))
        fails = sorted((b["rule"], b["target"]) for b in out if b["status"] == "FAIL")
        self.assertEqual(fails, [("B2", "CMP-003"), ("B7", "AC-003-1")])

class YamlMiniTest(unittest.TestCase):
    def test_fallback_parser_matches_config(self):
        real_import = builtins.__import__
        def no_yaml(name, *a, **k):
            if name == "yaml": raise ImportError
            return real_import(name, *a, **k)
        builtins.__import__ = no_yaml
        try:
            mini = yamlmini.loads((ROOT / "config.yaml").read_text(encoding="utf-8"))
        finally:
            builtins.__import__ = real_import
        self.assertEqual(mini["tech_boundary"]["layers"], ["Api", "Application", "Domain", "Infrastructure"])
        self.assertEqual(mini["tech_boundary"]["stack"]["language"], "C#")
        self.assertIn("ASP.NET Core", mini["tech_boundary"]["tech_allowlist"])
        self.assertEqual(mini["input"]["mock"]["enabled"], True)
        self.assertTrue(mini["gates"]["S0"].startswith("需求清單"))
        try:
            import yaml
            self.assertEqual(mini, yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8")))
        except ImportError:
            pass

if __name__ == "__main__":
    unittest.main()
