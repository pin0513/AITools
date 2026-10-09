"""執行工具 v1:依 process/pipeline.yaml 跑 stage。llm stage → 契約檢查;tool stage → 依 registry 執行工具;每個 stage 後跑它的 gates。"""
import json, pathlib
from core import config as C
from tools.check import engine_v1 as E, contract_v1 as CT

def make_ctx(d: pathlib.Path, cfg: dict, offline=False) -> dict:
    return {"dir": d, "config": cfg, "rules": C.load_rules(cfg), "contracts": C.load_contracts(),
            "registry": C.load_registry(), "offline": offline, "data": None, "log": [], "boundary": [], "gate": [],
            "contract_findings": [], "kpis": {}, "trace": []}

def run_stage(ctx: dict, stage: dict) -> dict:
    ctx["trace"].append(f"== {stage['id']} {stage['name']} ({stage['owner']})")
    if stage["owner"] == "llm":
        CT.run(ctx, stage)
        for f in ctx["contract_findings"]: ctx["trace"].append(f"  [{f['level']}] {f['rule']} {f['msg']}")
        if not ctx["contract_findings"]: ctx["trace"].append(f"  contract OK: {', '.join(stage['outputs'])}")
    else:
        for ref in stage.get("tools") or []:
            fn, ver = C.resolve_tool(ref, ctx["registry"])
            ctx = fn(ctx)
            ctx["trace"].append(f"  ran {ref.split('@')[0]}@{ver}")
    if stage.get("gates") and ctx.get("data") is not None:
        E.run_gate(ctx, stage)
        for g in ctx["gate"]: ctx["trace"].append(f"  [{g['level']}] {g['rule']} {g['msg']}")
    elif stage["owner"] == "llm":
        ctx["gate"] = list(ctx["contract_findings"])
    stop_on = stage.get("stop_on", "FAIL")
    ctx["stage_status"] = "FAIL" if any(g["level"] == "FAIL" for g in ctx["gate"]) else ("WARN" if any(g["level"] == "WARN" for g in ctx["gate"]) else "PASS")
    ctx["stopped"] = stop_on != "NONE" and ctx["stage_status"] == "FAIL"
    return ctx

def run_pipeline(ctx: dict, to: str = "S6", only: str = None, no_stop=False) -> dict:
    pipe = C.load_pipeline(); ctx["pipeline_version"] = pipe["version"]
    for st in pipe["stages"]:
        if only and st["id"] != only: continue
        ctx = run_stage(ctx, st)
        ctx["last_stage"] = st["id"]
        if ctx.get("stopped") and not no_stop:
            ctx["trace"].append(f"  stop at {st['id']} (stop_on={st.get('stop_on')})"); break
        if st["id"] == to: break
    if ctx.get("data") is not None:
        # 最終把 gate 與 kpi 全量重算一次,確保 json 與面板一致
        E.run_gate(ctx)
        (ctx["dir"] / "traceability.json").write_text(json.dumps(ctx["data"], ensure_ascii=False, indent=2), encoding="utf-8")
    return ctx

def init(d: pathlib.Path, title: str) -> list:
    d.mkdir(parents=True, exist_ok=True); done = []
    for src in sorted((C.PATHS["templates"] / "rd-spec").glob("*.md")):
        dst = d / src.name
        if dst.exists(): done.append(f"skip {dst.name}"); continue
        dst.write_text(src.read_text(encoding="utf-8").replace("{feature-title}", title), encoding="utf-8"); done.append(f"created {dst.name}")
    log = d / "method-log.jsonl"
    if not log.exists(): log.write_text("", encoding="utf-8"); done.append("created method-log.jsonl")
    return done
