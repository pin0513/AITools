"""執行工具 v1:依 process/pipeline.yaml 跑 stage。llm stage → 契約檢查;tool stage → 依 registry 執行工具;每個 stage 後跑它的 gates。"""
import json, pathlib
from core import config as C
from tools.check import engine_v1 as E, contract_v1 as CT

def make_ctx(d: pathlib.Path, cfg: dict, offline=False) -> dict:
    d = d.resolve()
    review = (d / ((cfg.get("output") or {}).get("review_dir") or ".")).resolve()
    review.mkdir(parents=True, exist_ok=True)
    override = cfg.get("_config_override")
    root = pathlib.Path(override).parent if override else d
    meth_name = (cfg.get("sa_modeling") or {}).get("methodology")
    meth = C.load_methodology(meth_name) if meth_name and meth_name != "none" else {}
    return {"dir": d, "review_dir": review, "project_root": root, "spec_name": d.parent.name if d.name == "spec" else d.name, "config": cfg, "rules": C.load_rules(cfg), "contracts": C.load_contracts(),
            "registry": C.load_registry(), "methodology": meth, "offline": offline, "data": None, "log": [], "boundary": [], "gate": [],
            "contract_findings": [], "kpis": {}, "trace": []}

def run_stage(ctx: dict, stage: dict) -> dict:
    ctx["trace"].append(f"== {stage['id']} {stage['name']} ({stage['owner']})")
    ctx["stage_id"] = stage["id"]
    if (stage.get("methodology") or stage.get("requires") == "sa_modeling") and not ctx.get("methodology"):
        ctx["trace"].append("  skipped: sa_modeling.methodology = none"); ctx["stage_findings"] = []; ctx["stage_status"] = "PASS"; ctx["stopped"] = False
        return ctx
    if stage.get("methodology") and ctx.get("methodology"):
        stage = dict(stage, outputs=[st["output"] for st in ctx["methodology"].get("steps") or []])
        ctx["trace"].append(f"  methodology {ctx['methodology']['id']} v{ctx['methodology'].get('version', 1)}: {len(stage['outputs'])} outputs")
    for ref in stage.get("pre_tools") or []:
        fn, ver = C.resolve_tool(ref, ctx["registry"]); ctx = fn(ctx); ctx["trace"].append(f"  pre  {ref.split('@')[0]}@{ver}")
    if stage.get("pre_tools") and ctx.get("data") is not None:
        from tools.analyze import extract_v1 as X
        X.run(ctx)   # pre_tools 可能產生 review_dir 檔案,重抽讓 gate 看到
    if stage["owner"] in ("llm", "tool+llm") and stage["owner"] != "tool":
        CT.run(ctx, stage)
        if not ctx["contract_findings"]: ctx["trace"].append(f"  contract OK: {', '.join(stage['outputs'])}")
        elif not stage.get("gates"):
            for f in ctx["contract_findings"]: ctx["trace"].append(f"  [{f['level']}] {f['rule']} {f['msg']}")
    if stage["owner"] == "tool+llm" and ctx.get("data") is None:
        from tools.analyze import extract_v1 as X
        X.run(ctx)
    if stage["owner"] in ("tool", "tool+llm"):
        for ref in stage.get("tools") or []:
            fn, ver = C.resolve_tool(ref, ctx["registry"])
            ctx = fn(ctx)
            ctx["trace"].append(f"  ran {ref.split('@')[0]}@{ver}")
    if stage.get("gates") and ctx.get("data") is None and stage["owner"] != "tool":
        # SA/SV 等 llm stage 也要能跑 gate:先抽一次資料(不寫檔)
        from tools.analyze import extract_v1 as X
        X.run(ctx)
    if stage.get("gates") and ctx.get("data") is not None:
        stage_findings = list(ctx["contract_findings"]) + E.evaluate_gates(ctx, stage["gates"])
        for g in stage_findings: ctx["trace"].append(f"  [{g['level']}] {g['rule']} {g['msg']}")
    elif stage["owner"] != "tool":
        stage_findings = list(ctx["contract_findings"])
        for g in stage_findings: ctx["trace"].append(f"  [{g['level']}] {g['rule']} {g['msg']}")
    else:
        stage_findings = []
    ctx["stage_findings"] = stage_findings
    stop_on = stage.get("stop_on", "FAIL")
    ctx["stage_status"] = "FAIL" if any(g["level"] == "FAIL" for g in stage_findings) else ("WARN" if any(g["level"] == "WARN" for g in stage_findings) else "PASS")
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
    ctx["stage_id"] = None
    if ctx.get("data") is not None:
        # 最終全量 Gate + KPI,寫 traceability.json(面板與報告也都用全量)
        E.run_gate(ctx)
        (ctx["review_dir"] / "traceability.json").write_text(json.dumps(ctx["data"], ensure_ascii=False, indent=2), encoding="utf-8")
    return ctx

def init(d: pathlib.Path, title: str, cfg: dict = None) -> list:
    d.mkdir(parents=True, exist_ok=True); done = []
    def copy(src, dst):
        if dst.exists(): done.append(f"skip {dst.relative_to(d.parent)}"); return
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(src.read_text(encoding="utf-8").replace("{feature-title}", title), encoding="utf-8"); done.append(f"created {dst.relative_to(d.parent)}")
    for src in sorted((C.PATHS["templates"] / "rd-spec").glob("*.md")):
        copy(src, d / src.name)
    cfg = cfg or {}
    if (cfg.get("sa_modeling") or {}).get("methodology", "uml-wordbreak") not in (None, "none"):
        review = (d / ((cfg.get("output") or {}).get("review_dir") or ".")).resolve()
        for src in sorted((C.PATHS["templates"] / "sa").glob("*.md")):
            copy(src, (review / "sa" / src.name) if src.name[0].isdigit() else (review / src.name))
    log = d / "method-log.jsonl"
    if not log.exists(): log.write_text("", encoding="utf-8"); done.append("created method-log.jsonl")
    return done
