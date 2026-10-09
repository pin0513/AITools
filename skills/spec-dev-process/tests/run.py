#!/usr/bin/env python3
"""測試分快慢兩組。
  python3 tests/run.py fast   單元、規則案例(含固定對照組)、契約、testcase1、版本追蹤 —— 約 20 秒,install.sh 只跑這組
  python3 tests/run.py slow   CLI、測試矩陣(產生 15 份專案)、真瀏覽器 —— 數分鐘,需要 node + playwright 的會自動 skip
  python3 tests/run.py all    全部(改版前跑)"""
import pathlib, sys, time, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
FAST = ["tests.unit.test_core", "tests.unit.test_lexicon", "tests.unit.test_reviewer", "tests.rules.test_rule_cases",
        "tests.contract.test_contracts", "tests.e2e.test_testcase1", "tests.e2e.test_versions"]
SLOW = ["tests.e2e.test_cli", "tests.e2e.test_matrix", "tests.e2e.test_panel_browser"]

def main(argv):
    group = argv[1] if len(argv) > 1 else "fast"
    names = {"fast": FAST, "slow": SLOW, "all": FAST + SLOW}.get(group)
    if names is None: print(__doc__); return 2
    known = {str(p.relative_to(ROOT).with_suffix("")).replace("/", ".") for p in (ROOT / "tests").rglob("test_*.py")}
    missing = known - set(FAST + SLOW)
    if missing: print(f"這些測試檔沒有分組,請加進 FAST 或 SLOW:{sorted(missing)}"); return 2
    t0 = time.time()
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in names)
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"[{group}] {res.testsRun} tests · {time.time() - t0:.1f}s")
    return 0 if res.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
