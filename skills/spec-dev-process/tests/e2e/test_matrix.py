"""e2e:測試矩陣。(1) 產生器可重現:重產結果與 examples/matrix 一致;(2) 15 份全部驗收:baseline 0 FAIL、45 個突變版全被指定規則抓到。"""
import filecmp, json, pathlib, shutil, tempfile, unittest
from core import config as C
from tests.matrix import gen_matrix as G, scenarios as SC
from tools.execute import matrix_v1 as MX

ROOT = C.ROOT; MATRIX = ROOT / "examples" / "matrix"
GENERATED_ONLY_BY_REVIEW = {"html", "check-panel.html", "traceability.json", "90-traceability.md", "boundary-report.md", "survey-candidates.md",
                            "lexicon.json", "00-lexicon.md", "glossary.md", "naming-map.md"}

class MatrixTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = pathlib.Path(tempfile.mkdtemp())
        G.main(cls.tmp)
        cls.out = MX.run_matrix(cls.tmp)

    @classmethod
    def tearDownClass(cls): shutil.rmtree(cls.tmp)

    def test_pairwise_covers_every_pair(self):
        cases = SC.pairwise(); self.assertEqual(len(cases), 15)
        for a, b in ((0, 1), (0, 2), (1, 2)):
            pairs = {(c[a], c[b]) for c in cases}
            dims = [SC.SHAPES, SC.LANGS, sorted(SC.SCENARIOS)]
            self.assertEqual(len(pairs), len(dims[a]) * len(dims[b]), (a, b))

    def test_generator_is_reproducible(self):
        """examples/matrix 必須等於重產結果(review 產生物除外)。"""
        diffs = []
        def walk(a: pathlib.Path, b: pathlib.Path):
            for p in sorted(a.iterdir()):
                if p.name in GENERATED_ONLY_BY_REVIEW or p.name.startswith("_") or p.name in ("acceptance.json",): continue
                q = b / p.name
                if p.is_dir(): walk(p, q)
                elif not q.exists() or not filecmp.cmp(p, q, shallow=False): diffs.append(str(p.relative_to(self.tmp)))
        for case in sorted(self.tmp.glob("*/expected.json")): walk(case.parent, MATRIX / case.parent.name)
        self.assertEqual(diffs, [], "examples/matrix 與產生器不一致,請跑 tests/matrix/gen_matrix.py")

    def test_all_cases_accepted(self):
        s = self.out["summary"]
        bad = [(r["id"], r["baseline"]["fail_rules"], [m["name"] for m in r["mutants"] if not m["caught"]]) for r in self.out["results"] if not r["accepted"]]
        self.assertEqual(bad, []); self.assertEqual(s["accepted"], 15); self.assertEqual(s["mutants_caught"], s["mutants"]); self.assertEqual(s["mutants"], 15 * 3 + 12)

    def test_each_mutant_caught_by_its_intended_rule(self):
        for r in self.out["results"]:
            for m in r["mutants"]:
                with self.subTest(case=r["id"], mutant=m["name"]):
                    self.assertTrue(m["applied"]); self.assertIn(m["expect_rule"], m["fail_rules"])

    def test_shapes_have_the_right_layers(self):
        by = {r["id"]: r for r in self.out["results"]}
        for r in self.out["results"]:
            L = set(r["layers"])
            if r["shape"] == "fe-only": self.assertFalse(L & {"Api", "Application", "Domain", "Infrastructure"}, r["id"])
            if r["shape"] == "be-only": self.assertFalse(L & {"Page", "Component", "Store", "ApiClient"}, r["id"])
            if r["shape"] == "fs-front": self.assertNotIn("Domain", L, r["id"]); self.assertIn("Store", L)
            if r["shape"] == "fs-back": self.assertIn("Domain", L); self.assertNotIn("Store", L)
            if r["shape"] == "fs-balance": self.assertTrue({"Domain", "Store"} <= L)

    def test_layered_spec_structure(self):
        for case in self.tmp.glob("*/expected.json"):
            e = json.loads(case.read_text(encoding="utf-8")); spec = case.parent / e["spec"]
            self.assertEqual((spec / "ui" / "41-ui-spec.md").exists(), e["shape"] != "be-only", e["id"])
            self.assertTrue((spec / "api" / "40-api-contracts.md").exists(), e["id"])
            self.assertEqual((spec / "api" / "50-data-model.md").exists(), e["shape"] != "fe-only", e["id"])
            self.assertTrue((case.parent / "specs" / "naming-map.md").exists(), e["id"])

    def test_board_written(self):
        board = self.tmp / "_board"
        self.assertTrue((board / "index.html").exists()); self.assertTrue((board / "page.html").read_text(encoding="utf-8").startswith("<title>"))
        self.assertEqual(len(list((board / "tc").glob("*.html"))), 15)
