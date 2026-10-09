#!/usr/bin/env python3
"""spec-dev-process CLI — PM spec → RD spec 工作流程的核對工具(零第三方相依)。

用法:
  spec-dev.py init    <rd-spec-dir> --title "功能名稱"     由模板建立 RD spec 骨架
  spec-dev.py extract <rd-spec-dir>                         md(唯一事實來源)→ traceability.json
  spec-dev.py check   <rd-spec-dir>                         extract + B1–B8 + Gate → boundary-report.md, 90-traceability.md
  spec-dev.py panel   <rd-spec-dir> [--offline]             check + 產生 check-panel.html(--offline 內嵌 mermaid)
  spec-dev.py render  <rd-spec-dir> [--offline]             每個 md → html/<name>.html
  spec-dev.py all     <rd-spec-dir> [--offline]             extract → check → panel → render
  選項:--config <path> 指定設定檔(預設:<rd-spec-dir>/../../.spec-dev.yaml 或套件 config.yaml)
退出碼:0 無 FAIL;1 有 FAIL(檔案仍會產生);2 用法錯誤。
"""
import json, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from specdev import extract as X, rules as R, report as RP, panel as P, render as RD, yamlmini  # noqa: E402

VENDOR_MERMAID = ROOT / "vendor" / "mermaid.min.js"

def load_config(d: pathlib.Path, explicit=None) -> dict:
    base = yamlmini.load(ROOT / "config.yaml")
    cands = [pathlib.Path(explicit)] if explicit else [p / ".spec-dev.yaml" for p in [d, *d.parents]]
    for c in cands:
        if c.exists():
            over = yamlmini.load(c) or {}
            for k, v in over.items():
                if isinstance(v, dict) and isinstance(base.get(k), dict):
                    base[k].update(v)
                else:
                    base[k] = v
            base["_config_override"] = str(c)
            break
    return base

def cmd_init(d: pathlib.Path, title: str):
    d.mkdir(parents=True, exist_ok=True)
    for src in sorted((ROOT / "templates" / "rd-spec").glob("*.md")):
        dst = d / src.name
        if dst.exists():
            print("skip (exists)", dst.name); continue
        dst.write_text(src.read_text(encoding="utf-8").replace("{feature-title}", title), encoding="utf-8")
        print("created", dst.name)
    log = d / "method-log.jsonl"
    if not log.exists():
        log.write_text("", encoding="utf-8"); print("created method-log.jsonl")

def run_check(d: pathlib.Path, cfg: dict):
    tr = X.extract(d)
    log = X.load_log(d)
    boundary = R.run(tr, log, cfg)
    g = R.gate(tr, log, boundary)
    k = R.kpis(tr, boundary, g)
    tr["boundary_checks"], tr["gate"], tr["kpis"] = boundary, g, k
    (d / "traceability.json").write_text(json.dumps(tr, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "90-traceability.md").write_text(RP.traceability_md(tr, boundary, g, k), encoding="utf-8")
    (d / "boundary-report.md").write_text(RP.boundary_md(tr, boundary), encoding="utf-8")
    return tr, log, boundary, g, k

def summary(k, g, boundary):
    print(f"  REQ {k['req_count']} · CMP {k['component_count']} · TST {k['test_count']} · boundary PASS {k['boundary_pass']}/{k['boundary_total']} (FAIL {k['boundary_fail']}, WARN {k['boundary_warn']}) · 未覆蓋 {k['uncovered_req']} {k['uncovered_ids']}")
    for x in g:
        print(f"  [{x['level']}] {x['rule']:<4} {x['msg']}")
    for b in boundary:
        if b["status"] == "WARN":
            print(f"  [WARN] {b['rule']:<4} {b['target']}: {b['evidence']}")

def main(argv):
    if len(argv) < 3 or argv[1] not in ("init", "extract", "check", "panel", "render", "all"):
        print(__doc__); return 2
    cmd, d = argv[1], pathlib.Path(argv[2])
    offline = "--offline" in argv
    cfg_path = argv[argv.index("--config") + 1] if "--config" in argv else None
    if cmd == "init":
        title = argv[argv.index("--title") + 1] if "--title" in argv else d.name
        cmd_init(d, title); return 0
    if not d.is_dir():
        print(f"找不到目錄 {d}"); return 2
    cfg = load_config(d, cfg_path)
    if cfg.get("_config_override"): print("config override:", cfg["_config_override"])
    if cmd == "extract":
        tr = X.extract(d)
        (d / "traceability.json").write_text(json.dumps(tr, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"wrote {d/'traceability.json'}: REQ {len(tr['requirements'])}, CMP {len(tr['components'])}, TST {len(tr['tests'])}, artifacts {len(tr['artifacts'])}")
        for e in tr["extract_errors"]: print(f"  [{e['level']}] {e['msg']}")
        return 1 if any(e["level"] == "FAIL" for e in tr["extract_errors"]) else 0
    if cmd == "render":
        done = RD.render_dir(d, VENDOR_MERMAID if offline else None)
        print("rendered:", ", ".join(done)); return 0
    tr, log, boundary, g, k = run_check(d, cfg)
    print(f"wrote traceability.json, 90-traceability.md, boundary-report.md")
    if cmd in ("panel", "all"):
        out = P.build(d, tr, log, boundary, g, k, VENDOR_MERMAID if offline else None)
        print(f"wrote {out.name}{' (offline, mermaid 內嵌)' if offline else ' (mermaid 走 CDN)'}")
    if cmd == "all":
        print("rendered:", ", ".join(RD.render_dir(d, VENDOR_MERMAID if offline else None)))
    summary(k, g, boundary)
    return 1 if any(x["level"] == "FAIL" for x in g) else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
