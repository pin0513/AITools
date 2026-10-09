"""rules:資料驅動。tests/rules/cases/<RULE>.yaml 每個 case 給 data/log 片段與期望 (outcome, target) 集合;引擎真的跑規則 YAML。"""
import pathlib, unittest
from core import config as C, yamlmini
from tools.check import engine_v1 as E

CASES = pathlib.Path(__file__).resolve().parent / "cases"

def base_data():
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

def apply(data, patch):
    """patch: {"set": {"components[2].depends": [...]}, "append": {"requirements": {...}}, "replace": {"tests": [...]}}"""
    import re
    for path, val in (patch.get("set") or {}).items():
        obj = data; parts = re.findall(r"([a-z_]+)(?:\[(\d+)\])?", path)
        for i, (key, idx) in enumerate(parts):
            last = i == len(parts) - 1
            if idx == "":
                if last: obj[key] = val
                else: obj = obj[key]
            else:
                if last: obj[key][int(idx)] = val
                else: obj = obj[key][int(idx)]
    for key, val in (patch.get("append") or {}).items():
        data[key].append(val)
    for key, val in (patch.get("replace") or {}).items():
        data[key] = val
    return data

class RuleCasesTest(unittest.TestCase):
    pass

def _make(rule_id, case):
    def test(self):
        rules = C.load_rules({})
        self.assertIn(rule_id, rules, f"{rule_id} 不在 rulesets.default")
        data = apply(base_data(), case.get("patch") or {})
        log = case.get("log") or []
        ctx = {"log": log, "live_log": log, "boundary": case.get("boundary") or [], "config": case.get("config") or {"tech_boundary": {"stack": {"runtime": ".NET"}, "tech_allowlist": ["EF Core"]}},
               "contracts": C.load_contracts()}
        for k, v in (case.get("ctx") or {}).items():
            ctx[k] = (C.ROOT / v) if k == "project_root" else v
        got = {(r["outcome"], r["target"]) for r in E.evaluate(rules[rule_id], data, ctx)}
        exp = {(o["outcome"], o["target"]) for o in case["expect"]}
        if case.get("exact", True): self.assertEqual(got, exp)
        else: self.assertTrue(exp <= got, f"missing {exp - got}; got {got}")
        for o in case["expect"]:
            status = rules[rule_id]["outcomes"][o["outcome"]]["status"]
            if "status" in o: self.assertEqual(status, o["status"], f"{rule_id}.{o['outcome']} status")
    return test

for f in sorted(CASES.glob("*.yaml")):
    spec = yamlmini.load(f)
    for case in spec["cases"]:
        setattr(RuleCasesTest, f"test_{spec['rule']}_{case['name']}", _make(spec["rule"], case))
