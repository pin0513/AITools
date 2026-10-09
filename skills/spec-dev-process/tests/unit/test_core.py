"""unit:core(md 解析、YAML 子集)與規則引擎本體。"""
import builtins, pathlib, unittest
from core import mdtables as M, yamlmini, config as C
from tools.check import engine_v1 as E

ROOT = C.ROOT
SIG = {"ac_links": ["AC", "CMP"], "components": ["ID", "名稱", "Layer"]}

class MdTablesTest(unittest.TestCase):
    def test_classify_by_signature_prefix(self):
        d = M.parse("x.md", "## 追溯\n| AC | CMP | via | 職責 |\n|---|---|---|---|\n| AC-1-1 | CMP-001 | SEQ-001 | 檢查 |\n")
        self.assertEqual(M.classify(d.tables[0], SIG), "ac_links")
        self.assertEqual(d.tables[0].rows[0]["CMP"], "CMP-001")
        self.assertEqual(d.tables[0].section, "追溯")
        self.assertIsNone(M.classify(M.parse("x.md", "| a | b |\n|---|---|\n| 1 | 2 |\n").tables[0], SIG))

    def test_table_without_separator_is_ignored(self):
        self.assertEqual(M.parse("x.md", "| a | b |\n| 1 | 2 |\n").tables, [])

    def test_mermaid_attaches_to_nearest_h3(self):
        d = M.parse("x.md", "## S\n### SEQ-001 上傳(UC-001 / REQ-001)\n```mermaid\nsequenceDiagram\nA->>B: x\n```\n### other\n```python\nx=1\n```\n")
        self.assertEqual(len(d.mermaid), 1)
        self.assertEqual(d.mermaid[0].heading, "SEQ-001 上傳(UC-001 / REQ-001)")

    def test_split_ids(self):
        self.assertEqual(M.split_ids("CMP-001, CMP-002 (via IFoo); AC-001-2"), ["CMP-001", "CMP-002", "AC-001-2"])

class YamlMiniTest(unittest.TestCase):
    def _mini(self, text):
        real = builtins.__import__
        def no_yaml(name, *a, **k):
            if name == "yaml": raise ImportError
            return real(name, *a, **k)
        builtins.__import__ = no_yaml
        try: return yamlmini.loads(text)
        finally: builtins.__import__ = real

    def test_fallback_matches_pyyaml_on_all_package_yaml(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML 不在,無法交叉比對")
        files = [C.PATHS["config"], C.PATHS["pipeline"], C.PATHS["contracts"], C.PATHS["registry"], C.PATHS["rulesets"]] + sorted((ROOT / "rules").rglob("*.yaml"))
        for f in files:
            text = f.read_text(encoding="utf-8")
            with self.subTest(file=f.name):
                self.assertEqual(self._mini(text), yaml.safe_load(text))

    def test_scalars_and_inline_lists(self):
        d = self._mini('a: 1\nb: "x: y"\nc: [p, "q, r", 2]\nd:\n  - u\n  - v\ne: true\n')
        self.assertEqual(d, {"a": 1, "b": "x: y", "c": ["p", "q, r", 2], "d": ["u", "v"], "e": True})

class EngineTest(unittest.TestCase):
    RULE = {"id": "T1", "version": 1, "category": "boundary", "predicate": "p", "params": {}, "_order": 0,
            "outcomes": {"bad": {"status": "FAIL", "message": "x={x} t={target}", "action": "fix {x}"}}}

    def test_outcome_mapped_to_status_and_message(self):
        class P:
            __name__ = "P"
            @staticmethod
            def p(data, params, ctx): return [{"outcome": "bad", "target": "CMP-1", "ids": ["CMP-1"], "vars": {"x": 7}}]
        r = E.evaluate(self.RULE, {}, {}, predicates=P)
        self.assertEqual((r[0]["status"], r[0]["evidence"], r[0]["action"], r[0]["ids"]), ("FAIL", "x=7 t=CMP-1", "fix 7", ["CMP-1"]))

    def test_unknown_outcome_raises(self):
        class P:
            __name__ = "P"
            @staticmethod
            def p(data, params, ctx): return [{"outcome": "nope", "target": "a"}]
        with self.assertRaises(KeyError): E.evaluate(self.RULE, {}, {}, predicates=P)

    def test_missing_predicate_raises(self):
        class P: __name__ = "P"
        with self.assertRaises(AttributeError): E.evaluate(self.RULE, {}, {}, predicates=P)

class ConfigTest(unittest.TestCase):
    def test_rules_load_with_override_and_disable(self):
        rules = C.load_rules({"rules": {"disable": ["B8"], "overrides": {"B2": {"outcomes": {"concrete_infra": {"status": "FAIL"}}}}}})
        self.assertNotIn("B8", rules)
        self.assertEqual(rules["B2"]["outcomes"]["concrete_infra"]["status"], "FAIL")
        self.assertEqual(rules["B2"]["outcomes"]["reverse"]["status"], "FAIL")  # 其他 outcome 不受影響

    def test_resolve_tool_versions(self):
        reg = C.load_registry()
        fn, ver = C.resolve_tool("analyze.extract", reg); self.assertEqual(ver, 1); self.assertTrue(callable(fn))
        fn, ver = C.resolve_tool("check.boundary@1", reg); self.assertEqual(fn.__name__, "run_boundary")
        with self.assertRaises(KeyError): C.resolve_tool("analyze.extract@9", reg)
        with self.assertRaises(KeyError): C.resolve_tool("nope.tool", reg)
