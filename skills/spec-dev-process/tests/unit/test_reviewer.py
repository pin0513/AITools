"""unit:spec-reviewer 子系統——mermaid 解析、核對函式、自動圖、審計(來源/過程/目標/hash)、簽核 hash 防護與過期。"""
import copy, json, pathlib, shutil, tempfile, unittest
from tools.review import mermaid_v1 as MM, checks_v1 as K, diagrams_v1 as D, audit_v1 as A, signoff_v1 as SO
from tests.rules.test_rule_cases import base_data

SEQ_OK = """sequenceDiagram
  actor U as Applicant
  participant Ctl as Ctl
  participant H as Handler
  participant R as IRepo
  U->>Ctl: Submit
  Ctl->>H: Handle
  H->>R: Save
  R-->>H: ok
  H-->>Ctl: id"""

class MermaidParserTest(unittest.TestCase):
    def test_kinds(self):
        for code, k in (("sequenceDiagram\n", "sequence"), ("stateDiagram-v2\n", "state"), ("classDiagram\n", "class"), ("erDiagram\n", "erd"),
                        ("C4Component\n", "c4-component"), ("flowchart LR\n", "flowchart"), ("%% c\ngraph TD\n", "flowchart"), ("pie\n", "other")):
            self.assertEqual(MM.kind_of(code), k)

    def test_sequence_participants_actors_calls_replies(self):
        p = MM.parse(SEQ_OK)
        self.assertEqual(p["actors"], {"U"}); self.assertEqual(p["participants"]["R"], "IRepo")
        self.assertEqual([(c["from"], c["to"], c["reply"]) for c in p["calls"]][:3], [("U", "Ctl", False), ("Ctl", "H", False), ("H", "R", False)])
        self.assertTrue(p["calls"][3]["reply"])

    def test_state_event_name(self):
        p = MM.parse("stateDiagram-v2\n  [*] --> Draft\n  Draft --> Submitted : Submit(form)\n  Submitted --> [*]")
        self.assertEqual(p["states"], {"Draft", "Submitted"})
        self.assertEqual([t["event_name"] for t in p["transitions"]], ["", "Submit", ""])

    def test_class_and_er(self):
        self.assertEqual(MM.parse("classDiagram\n  class Form\n  Form \"1\" --> \"*\" Field")["classes"], {"Form", "Field"})
        self.assertEqual(MM.parse("erDiagram\n  FORM ||--o{ FIELD : has\n  FORM {\n  int id\n  }")["entities"], {"FORM", "FIELD"})

class ChecksTest(unittest.TestCase):
    def setUp(self): self.d = base_data()

    def test_seq_follows_dependencies_passes_and_catches_skip(self):
        self.assertEqual(K.seq_calls_follow_dependencies({}, MM.parse(SEQ_OK), self.d, {}), [])
        bad = SEQ_OK.replace("Ctl->>H: Handle", "Ctl->>R: Save")   # Api 直接呼叫 Repository:CMP-001 沒有依賴 CMP-004
        out = K.seq_calls_follow_dependencies({}, MM.parse(bad), self.d, {})
        self.assertIn("seq_no_dependency", [o for o, _ in out])

    def test_seq_unknown_participant(self):
        out = K.seq_calls_follow_dependencies({}, MM.parse(SEQ_OK.replace("participant R as IRepo", "participant R as Ghost")), self.d, {})
        self.assertIn(("seq_unknown_participant", {"participant": "Ghost"}), out)

    def test_interface_with_annotation_maps(self):
        self.d["components"][3]["interface"] = "IRepo(modify)"
        self.assertEqual(K.seq_calls_follow_dependencies({}, MM.parse(SEQ_OK), self.d, {}), [])

    def test_trace_and_tables(self):
        self.assertEqual(K.trace_has_edges({"edges": 0, "req": "REQ-001"}, {}, self.d, {}), [("trace_empty", {"req": "REQ-001"})])
        self.assertEqual(K.req_refs_exist({"對應 REQ": "REQ-404", "動作": "Submit"}, self.d, {}), [("req_missing", {"req": "REQ-404"})])
        self.assertEqual(K.action_has_symbol({"動作": "送出表單"}, self.d, {})[0][0], "action_symbol_missing")
        self.assertEqual(K.symbols_present({"實體": "表單", "英文": ""}, self.d, {})[0][0], "symbol_missing")

class AutoDiagramTest(unittest.TestCase):
    def test_every_requirement_gets_trace_and_dependency_ordered_sequence(self):
        d = base_data(); ctx = {"data": d}
        D.run(ctx)
        ids = [a["id"] for a in d["auto_diagrams"]]
        self.assertIn("AUTO-TRACE-REQ-001", ids); self.assertIn("AUTO-SEQ-REQ-001", ids)
        seq = next(a for a in d["auto_diagrams"] if a["id"] == "AUTO-SEQ-REQ-001")
        self.assertEqual(K.seq_calls_follow_dependencies(seq, MM.parse(seq["mermaid"]), d, {}), [], "自動循序圖只沿著依賴走")
        tr = next(a for a in d["auto_diagrams"] if a["id"] == "AUTO-TRACE-REQ-001")
        self.assertGreater(tr["edges"], 0)

class AuditAndSignoffTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp()); self.d = base_data()
        self.d["artifacts"] = [{"id": "SEQ-001", "kind": "sequence", "file": "30-architecture-c4.md", "line": 10, "heading": "SEQ-001 (REQ-001)", "req": "REQ-001", "mermaid": SEQ_OK},
                               {"id": "SEQ-002", "kind": "sequence", "file": "30-architecture-c4.md", "line": 30, "heading": "SEQ-002 (REQ-404)", "req": "REQ-404", "mermaid": SEQ_OK}]
        self.log = [{"seq": 1, "stage": "S3", "method": "UML Sequence", "in": "UC-001", "out": "SEQ-001", "req": "REQ-001"}]

    def tearDown(self): shutil.rmtree(self.tmp)

    def ctx(self):
        c = {"data": copy.deepcopy(self.d), "review_dir": self.tmp, "project_root": self.tmp, "log": self.log, "methodology": {}, "config": {}}
        D.run(c); A.run(c); return c

    def item(self, c, i): return next(x for x in c["data"]["audit"]["items"] if x["id"] == i)

    def test_source_process_target_hash(self):
        c = self.ctx(); s1, s2 = self.item(c, "SEQ-001"), self.item(c, "SEQ-002")
        self.assertEqual(s1["source"], "30-architecture-c4.md:10"); self.assertEqual(s1["process"][0]["seq"], 1)
        self.assertEqual(s1["findings"], []); self.assertRegex(s1["hash"], r"^[0-9a-f]{12}$")
        self.assertEqual({f["outcome"] for f in s2["findings"]}, {"target_missing", "process_none"})
        self.assertEqual(self.item(c, "AUTO-SEQ-REQ-001")["process"], [{"tool": "review.diagrams@1"}])
        self.assertTrue((self.tmp / "audit" / "signoff.md").exists())

    def test_signoff_hash_guard_reject_note_and_stale(self):
        c = self.ctx(); cur = self.item(c, "SEQ-001")["hash"]
        self.assertEqual(self.item(c, "SEQ-001")["duties"], ["buildable", "testable"])
        with self.assertRaises(SO.Refused): SO.apply(self.tmp, "SEQ-001", "Paul", "approved", "deadbeef0000", duty="buildable")
        with self.assertRaises(SO.Refused): SO.apply(self.tmp, "SEQ-001", "Paul", "rejected", duty="buildable")
        with self.assertRaises(SO.Refused): SO.apply(self.tmp, "SEQ-001", "Paul", "n/a", cur, duty="testable")
        with self.assertRaises(SO.Refused): SO.apply(self.tmp, "SEQ-001", "Paul", "approved", cur, duty="intent")   # 這張圖沒有這個確認事項
        SO.apply(self.tmp, "SEQ-001", "Paul", "approved", cur, duty="buildable")
        self.assertEqual(self.item(self.ctx(), "SEQ-001")["signoff"], "pending", "還有一項沒做")
        SO.apply(self.tmp, "SEQ-001", "Paul", "n/a", cur, "只有讀取,無新路徑", duty="testable")   # 同一個人做完另一項;不需要也算做完
        self.assertEqual(self.item(self.ctx(), "SEQ-001")["signoff"], "approved")
        self.d["artifacts"][0]["mermaid"] = SEQ_OK + "\n  Ctl-->>U: done"     # 圖改了 → 過期
        self.assertEqual(self.item(self.ctx(), "SEQ-001")["signoff"], "stale")
        self.assertIn("approved", (self.tmp / "audit" / "signoff.md").read_text(encoding="utf-8"), "工具不會改人的決定")

    def test_history_appends_only_on_change(self):
        self.ctx(); self.ctx()
        hist = (self.tmp / "audit" / "history.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(hist), 1)
        self.d["artifacts"][0]["mermaid"] = SEQ_OK + "\n  Ctl-->>U: done"; c = self.ctx()
        self.assertEqual(c["data"]["audit"]["summary"]["changed_since_last"], ["SEQ-001"])
        self.assertEqual(len((self.tmp / "audit" / "history.jsonl").read_text(encoding="utf-8").splitlines()), 2)

class VersionsUnitTest(unittest.TestCase):
    """review.versions:段落指紋、上游鍵、有變才記版、diff 與上游鍵變更紀錄。"""
    def test_sections_split_and_duplicate_headings(self):
        from tools.review import versions_v1 as V
        s = V.sections("前言\n# A\nx\n## B\ny\n## B\nz\n")
        self.assertEqual(list(s), ["(開頭)", "A", "B", "B (2)"]); self.assertNotEqual(s["B"], s["B (2)"])

    def test_upstream_keys_follow_pm_section_and_ac_text(self):
        from tools.review import versions_v1 as V
        d = base_data(); d["sources"] = {"pm_spec": {"sections": [{"anchor": "PM§1", "title": "t", "text": "原文"}]}}; d["ac_text"] = {"AC-001-1": {"text": "Given A"}}
        k1 = V.upstream_keys(d); d["sources"]["pm_spec"]["sections"][0]["text"] = "改過"; k2 = V.upstream_keys(d)
        self.assertNotEqual(k1["pm:REQ-001"], k2["pm:REQ-001"]); self.assertEqual(k1["req:REQ-001"], k2["req:REQ-001"])
        d["ac_text"]["AC-001-1"]["text"] = "Given B"; self.assertNotEqual(V.upstream_keys(d)["req:REQ-001"], k2["req:REQ-001"])

    def test_snapshot_only_on_change_with_diff(self):
        from tools.review import versions_v1 as V
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            spec = tmp / "spec"; spec.mkdir(); (spec / "10-requirements.md").write_text("# R\nREQ-001 a\n", encoding="utf-8")
            ctx = {"data": base_data(), "project_root": tmp, "dir": spec, "review_dir": spec}
            ctx["data"]["ac_text"] = {}
            self.assertEqual(V.snapshot(ctx)["current"], 1); self.assertEqual(V.snapshot(ctx)["current"], 1)
            (spec / "10-requirements.md").write_text("# R\nREQ-001 b\n", encoding="utf-8")
            s = V.snapshot(ctx); self.assertEqual(s["current"], 2)
            ch = s["timeline"][0]["changed"][0]; self.assertEqual((ch["path"], ch["sections"], ch["add"], ch["dele"]), ("spec/10-requirements.md", ["R"], 1, 1))
            self.assertIn("+REQ-001 b", s["diffs"]["2:spec/10-requirements.md"]["lines"])
        finally: shutil.rmtree(tmp)

