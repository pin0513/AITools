#!/usr/bin/env python3
"""spec-dev-process CLI(薄殼):讀 process/pipeline.yaml,交給 tools/execute 跑。

用法:
  spec-dev.py init    <dir> --title "功能名稱"        由 process/templates 建 RD spec 骨架
  spec-dev.py run     <dir> [--to S6] [--stage S3] [--no-stop] [--offline]   依 pipeline 跑 stage,遇 FAIL 依 stop_on 停
  spec-dev.py check   <dir>                            = run --to S5 --no-stop(extract → B1–B8 → gate → 報告)
  spec-dev.py all     <dir> [--offline]                = run --to S6 --no-stop(再加面板與 html)
  spec-dev.py extract <dir>                            只抽 traceability.json
  spec-dev.py panel   <dir> [--offline]                = all
  spec-dev.py render  <dir> [--offline]                只渲染 md → html/
  spec-dev.py glossary <dir>                           只抽跨 spec 詞彙表與分層命名對照表
  spec-dev.py matrix  <matrix-root> [--offline]        測試矩陣驗收:每份 baseline + 3 突變版 → acceptance.json、_board/
  spec-dev.py rules                                    列出啟用規則與版本
  spec-dev.py tools                                    列出工具與版本
  選項:--config <path> 指定 .spec-dev.yaml;--offline 內嵌 vendor/mermaid.min.js;--verbose 總表列出每筆 INFO
退出碼:0 無 FAIL;1 有 FAIL(檔案仍會產生);2 用法錯誤。
"""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from core import config as C  # noqa: E402

def _opt(argv, name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default

def summary(ctx, verbose=False):
    k = ctx.get("kpis") or {}
    if k:
        print(f"  REQ {k['req_count']} · CMP {k['component_count']} · TST {k['test_count']} · boundary PASS {k['boundary_pass']}/{k['boundary_total']} (FAIL {k['boundary_fail']}, WARN {k['boundary_warn']}) · 未覆蓋 {k['uncovered_req']} {k['uncovered_ids']}")
    print("總表(每筆發現只列一次):")
    info = {}
    for g in ctx.get("gate") or []:
        if g["level"] == "INFO" and not verbose:
            info[g["rule"]] = info.get(g["rule"], 0) + 1; continue
        print(f"  [{g['level']}] {g['rule']:<14} {g['msg']}")
    for rule, n in info.items():
        print(f"  [INFO] {rule:<14} {n} 筆通過(加 --verbose 看明細)")
    for b in ctx.get("boundary") or []:
        if b["status"] == "WARN": print(f"  [WARN] {b['rule']:<14} {b['target']}: {b['evidence']}")

def main(argv):
    if len(argv) < 2: print(__doc__); return 2
    cmd = argv[1]
    if cmd == "rules":
        for r in sorted(C.load_rules({}).values(), key=lambda r: r["_order"]):
            print(f"  {r['id']:<14} v{r['version']}  {r['category']:<9} {r['name']}  → {r['predicate']}")
        return 0
    if cmd == "tools":
        for name, e in C.load_registry()["tools"].items():
            print(f"  {name:<18} latest=v{e['latest']}  versions={sorted(e['versions'])}")
        return 0
    if len(argv) < 3 or cmd not in ("init", "run", "check", "all", "extract", "panel", "render", "glossary", "matrix"): print(__doc__); return 2
    d = pathlib.Path(argv[2]); offline = "--offline" in argv
    from tools.execute import runner_v1 as R
    if cmd == "matrix":
        from tools.execute import matrix_v1 as MX
        out = MX.run_matrix(d, offline); s = out["summary"]
        for r in out["results"]:
            print(f'  {"PASS" if r["accepted"] else "FAIL"}  {r["id"]:<22} baseline FAIL={r["baseline"]["fail"]} mutants={sum(m["caught"] for m in r["mutants"])}/{len(r["mutants"])} '
                  f'survey={r["survey"]["verified"]}/{r["survey"]["expected"]} recall={r["lexicon"]["recall"]:.0%} missing={r["lexicon"]["missing"]}')
        print(f'accepted {s["accepted"]}/{s["cases"]} · baseline clean {s["baseline_clean"]}/{s["cases"]} · mutants caught {s["mutants_caught"]}/{s["mutants"]} · recall {s["recall_by_lang"]}')
        print(f"board: {d / '_board' / 'index.html'}")
        return 0 if s["accepted"] == s["cases"] else 1
    if cmd == "init":
        for line in R.init(d, _opt(argv, "--title", d.name), C.load_config(d, _opt(argv, "--config"))): print(line)
        return 0
    if not d.is_dir(): print(f"找不到目錄 {d}"); return 2
    cfg = C.load_config(d, _opt(argv, "--config"))
    if cfg.get("_config_override"): print("config override:", cfg["_config_override"])
    ctx = R.make_ctx(d, cfg, offline)
    if cmd == "render":
        fn, _ = C.resolve_tool("transform.render", ctx["registry"]); ctx = fn(ctx); print("rendered:", ", ".join(ctx.get("rendered", []))); return 0
    if cmd == "glossary":
        fx, _ = C.resolve_tool("analyze.extract", ctx["registry"]); ctx = fx(ctx)
        fn, _ = C.resolve_tool("analyze.glossary", ctx["registry"]); ctx = fn(ctx)
        g = ctx["glossary"]; print(f"wrote {g['path']}: {len(g['terms'])} 詞, {len(g['conflicts'])} 衝突")
        for c in g["conflicts"]: print(f"  [CONFLICT] {c['term']}: {c['symbol_a']} ({c['source_a']}) vs {c['symbol_b']} ({c['source_b']})")
        return 1 if g["conflicts"] else 0
    if cmd == "extract":
        fn, _ = C.resolve_tool("analyze.extract", ctx["registry"]); ctx = fn(ctx)
        import json; (d / "traceability.json").write_text(json.dumps(ctx["data"], ensure_ascii=False, indent=2), encoding="utf-8")
        t = ctx["data"]; print(f"wrote traceability.json: REQ {len(t['requirements'])}, CMP {len(t['components'])}, TST {len(t['tests'])}, artifacts {len(t['artifacts'])}")
        for e in t["extract_errors"]: print(f"  [{e['level']}] {e['msg']}")
        return 1 if any(e["level"] == "FAIL" for e in t["extract_errors"]) else 0
    to = {"check": "S5", "all": "S6", "panel": "S6"}.get(cmd) or _opt(argv, "--to", "S6")
    ctx = R.run_pipeline(ctx, to=to, only=_opt(argv, "--stage"), no_stop=("--no-stop" in argv) or cmd in ("check", "all", "panel"))
    for line in ctx["trace"]: print(line)
    rd = ctx["review_dir"]; print(f"wrote ({rd}):", ", ".join(sorted(p.name for p in rd.iterdir() if p.name in ("traceability.json", "90-traceability.md", "boundary-report.md", "check-panel.html", "html", "survey-candidates.md"))))
    summary(ctx, "--verbose" in argv)
    failed = ctx.get("stopped") or any(g["level"] == "FAIL" for g in (ctx.get("gate") or []) + (ctx.get("stage_findings") or []))
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
