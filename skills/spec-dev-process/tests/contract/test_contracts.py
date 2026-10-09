"""contract:四層之間的引用一致 — pipeline ↔ registry ↔ rules ↔ predicates ↔ contracts ↔ templates ↔ docs。"""
import pathlib, re, unittest
from core import config as C, mdtables as M, yamlmini
from tools.check import predicates_v1 as P, contract_v1 as CT

ROOT = C.ROOT

class PipelineContractTest(unittest.TestCase):
    def setUp(self):
        self.pipe = C.load_pipeline(); self.reg = C.load_registry(); self.rules = C.load_rules({}); self.contracts = C.load_contracts()

    def test_stage_ids_ordered_and_unique(self):
        ids = [s["id"] for s in self.pipe["stages"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids[0], "S0"); self.assertEqual(ids[-1], "S6")
        self.assertLess(ids.index("SA"), ids.index("SV")); self.assertLess(ids.index("SV"), ids.index("S1"))

    def test_every_tool_ref_resolves(self):
        for s in self.pipe["stages"]:
            for ref in s.get("tools") or []:
                with self.subTest(stage=s["id"], tool=ref):
                    fn, _ = C.resolve_tool(ref, self.reg); self.assertTrue(callable(fn))
            self.assertIn(s["owner"], ("llm", "tool", "tool+llm"))
            if s["owner"] in ("tool", "tool+llm"): self.assertTrue(s.get("tools"), f"{s['id']} 是 {s['owner']} stage 但沒有 tools")
            else: self.assertFalse(s.get("tools"), f"{s['id']} 是 llm stage 不該有 tools")

    def test_every_gate_ref_is_a_gate_rule(self):
        for s in self.pipe["stages"]:
            for g in s.get("gates") or []:
                with self.subTest(stage=s["id"], gate=g):
                    self.assertIn(g, self.rules); self.assertEqual(self.rules[g]["category"], "gate")

    def test_every_gate_rule_used_by_some_stage(self):
        used = {g for s in self.pipe["stages"] for g in s.get("gates") or []}
        for rid, r in self.rules.items():
            if r["category"] == "gate": self.assertIn(rid, used, f"{rid} 沒有任何 stage 使用")

    def test_llm_stage_outputs_have_contracts(self):
        for s in self.pipe["stages"]:
            if s["owner"] != "llm" or s.get("methodology"): continue
            for out in s["outputs"]:
                self.assertIn(out.split("#")[0], self.contracts["files"], f"{s['id']} 產物 {out} 沒有 io-contract")

    def test_registry_modules_importable(self):
        for name, e in self.reg["tools"].items():
            for ver in e["versions"]:
                with self.subTest(tool=name, ver=ver): C.resolve_tool(f"{name}@{ver}", self.reg)

class RulesContractTest(unittest.TestCase):
    def test_every_rule_predicate_exists_and_outcomes_valid(self):
        for rid, r in C.load_rules({}).items():
            with self.subTest(rule=rid):
                self.assertTrue(hasattr(P, r["predicate"]), f"{rid}.predicate {r['predicate']} 不存在")
                for k, oc in r["outcomes"].items(): self.assertIn(oc["status"], ("PASS", "WARN", "FAIL", "INFO"), f"{rid}.{k}")
                self.assertEqual(r["id"], rid)

    def test_every_rule_has_cases(self):
        cases = {yamlmini.load(f)["rule"] for f in (ROOT / "tests" / "rules" / "cases").glob("*.yaml")}
        for rid in C.load_rules({}): self.assertIn(rid, cases, f"{rid} 沒有 tests/rules/cases")

    def test_predicate_outcomes_are_declared(self):
        """靜態掃 predicates 原始碼中 _f("xxx" 的 outcome 名稱,都要在對應規則 YAML 宣告。"""
        src = (ROOT / "tools" / "check" / "predicates_v1.py").read_text(encoding="utf-8")
        rules = C.load_rules({})
        by_pred = {r["predicate"]: r for r in rules.values()}
        for m in re.finditer(r"def (\w+)\(data, params, ctx\):(.*?)(?=\ndef |\Z)", src, re.S):
            name, body = m.group(1), m.group(2)
            if name not in by_pred: continue
            declared = set(by_pred[name]["outcomes"])
            used = set(re.findall(r'_f\(\s*"(\w+)"', body)) | set(re.findall(r'_f\("(\w+)" if', body)) | set(re.findall(r'else "(\w+)",', body))
            with self.subTest(predicate=name): self.assertTrue(used <= declared, f"{name} 用了未宣告 outcome {used - declared}")

    def test_routing_methods_match_methodology_doc(self):
        routing = yamlmini.load(ROOT / "rules" / "methodology" / "routing.yaml")
        doc = (ROOT / "references" / "methodology-map.md").read_text(encoding="utf-8")
        for mid in routing["methods"]: self.assertIn(f"({mid})", doc, f"{mid} 不在 references/methodology-map.md")
        for t, spec in routing["types"].items():
            for mid in spec["methods"]: self.assertIn(mid, routing["methods"])

class MethodologyContractTest(unittest.TestCase):
    def test_sa_methodology_steps_have_contracts(self):
        contracts = C.load_contracts()
        for f in (ROOT / "rules" / "methodology" / "sa").glob("*.yaml"):
            m = yamlmini.load(f)
            if "steps" not in m: continue          # lexicon-zh.yaml 等詞典資料,不是方法論
            self.assertEqual(m["id"], f.stem)
            for st in m["steps"]:
                with self.subTest(methodology=m["id"], step=st["id"]):
                    spec = contracts["files"].get(st["output"]); self.assertIsNotNone(spec, f"{st['output']} 無 io-contract")
                    self.assertEqual(spec.get("dir"), "review")
                    for sec in st.get("sections", []): self.assertIn(sec, spec.get("sections", []))
                    for pre in st.get("diagrams", []): self.assertTrue(pre.startswith(tuple(contracts["artifacts"]["heading_prefixes"])), f"{pre} 不在 heading_prefixes")

    def test_sa_templates_satisfy_contracts(self):
        contracts = C.load_contracts(); tdir = C.PATHS["templates"] / "sa"
        files = [f for f in contracts["files"] if contracts["files"][f].get("dir") == "review"]
        import tempfile, shutil, pathlib
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            (tmp / "sa").mkdir()
            for src in tdir.glob("*.md"): shutil.copy(src, (tmp / "sa" / src.name) if src.name[0].isdigit() else (tmp / src.name))
            findings = CT.check_files(tmp, contracts, files, review_dir=tmp)
            self.assertEqual([f for f in findings if f["level"] == "FAIL"], [], findings)
        finally: shutil.rmtree(tmp)

class TemplateContractTest(unittest.TestCase):
    def test_templates_satisfy_io_contracts(self):
        contracts = C.load_contracts(); d = C.PATHS["templates"] / "rd-spec"
        findings = CT.check_files(d, contracts, [f for f in contracts["files"] if f.endswith(".md")])
        self.assertEqual([f for f in findings if f["level"] == "FAIL"], [], findings)

    def test_template_tables_classify_to_every_declared_table(self):
        contracts = C.load_contracts(); sig = {k: v["signature"] for k, v in contracts["tables"].items()}
        found = set()
        for f in list((C.PATHS["templates"] / "rd-spec").rglob("*.md")) + list((C.PATHS["templates"] / "sa").glob("*.md")):
            for t in M.parse(f.name, f.read_text(encoding="utf-8")).tables:
                n = M.classify(t, sig)
                if n: found.add(n)
        generated_only = {"candidates", "glossary_project", "glossary_conflicts", "lexicon", "naming_map"}   # 由工具產生,沒有模板
        self.assertEqual(found, set(contracts["tables"]) - generated_only, f"模板缺表格 {set(contracts['tables']) - generated_only - found}")

    def test_template_mermaid_headings_match_prefixes(self):
        prefixes = tuple(C.load_contracts()["artifacts"]["heading_prefixes"])
        for f in (C.PATHS["templates"] / "rd-spec").rglob("*.md"):
            for mm in M.parse(f.name, f.read_text(encoding="utf-8")).mermaid:
                self.assertTrue(mm.heading.startswith(prefixes), f"{f.name}:{mm.line} mermaid 掛在 '{mm.heading}',不是 artifact 前綴")

    def test_docs_reference_existing_paths(self):
        for doc in [ROOT / "SKILL.md", ROOT / "README.md", *(ROOT / "references").glob("*.md"), ROOT / "rules" / "README.md"]:
            text = doc.read_text(encoding="utf-8")
            for ref in set(re.findall(r"`((?:process|tools|rules|core|tests|examples|vendor)/[\w./-]+?)`", text)):
                path = ROOT / ref.rstrip("/")
                with self.subTest(doc=doc.name, ref=ref):
                    self.assertTrue(path.exists() or any(path.parent.glob(path.name.replace("*", "*"))), f"{doc.name} 引用不存在的 {ref}")
