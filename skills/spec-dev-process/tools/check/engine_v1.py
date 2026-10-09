"""規則引擎 v1:載入 rules/*.yaml,呼叫 predicate,把 outcome 對到狀態與訊息。引擎不含任何規則知識。"""
from . import predicates_v1 as P

STATUSES = ("PASS", "WARN", "FAIL", "INFO")

def _fmt(tpl: str, vars: dict) -> str:
    try:
        return tpl.format(**vars)
    except (KeyError, IndexError):
        return tpl

def evaluate(rule: dict, data: dict, ctx: dict, predicates=P) -> list:
    fn = getattr(predicates, rule["predicate"], None)
    if fn is None:
        raise AttributeError(f"規則 {rule['id']} 的 predicate '{rule['predicate']}' 不存在於 {predicates.__name__}")
    out = []
    for f in fn(data, rule.get("params") or {}, ctx):
        oc = (rule.get("outcomes") or {}).get(f["outcome"])
        if oc is None:
            raise KeyError(f"規則 {rule['id']} 的 predicate 回傳未定義 outcome '{f['outcome']}'")
        if oc.get("status") not in STATUSES:
            raise ValueError(f"規則 {rule['id']} outcome {f['outcome']} 的 status 不合法:{oc.get('status')}")
        v = dict(f.get("vars") or {}); v.setdefault("target", f.get("target", ""))
        out.append({"rule": rule["id"], "rule_version": rule.get("version", 1), "outcome": f["outcome"],
                    "target": f.get("target", ""), "status": oc["status"],
                    "evidence": _fmt(oc.get("message", ""), v), "action": _fmt(oc.get("action", ""), v),
                    "ids": list(f.get("ids") or [f.get("target", "")])})
    return out

def run_rules(rules: dict, category: str, data: dict, ctx: dict) -> list:
    out = []
    for rule in sorted(rules.values(), key=lambda r: r["_order"]):
        if rule["category"] == category:
            out.extend(evaluate(rule, data, ctx))
    return out

def _ctx(ctx: dict) -> dict:
    log = ctx.get("log") or []
    superseded = {e["supersedes"] for e in log if "supersedes" in e}
    return {**ctx, "log": log, "live_log": [e for e in log if e.get("seq") not in superseded]}

# ---- tool 介面 ----
def run_boundary(ctx: dict) -> dict:
    ctx["boundary"] = run_rules(ctx["rules"], "boundary", ctx["data"], _ctx(ctx))
    ctx["data"]["boundary_checks"] = ctx["boundary"]
    return ctx

def evaluate_gates(ctx: dict, ids=None) -> list:
    """純函式:跑 gate 規則(ids 為 None 則全部),回傳 gate 形式 {level, rule, ids, msg, action};不改 ctx。"""
    rules = ctx["rules"] if ids is None else {k: v for k, v in ctx["rules"].items() if k in set(ids)}
    c = _ctx(ctx); c["boundary"] = ctx.get("boundary") or []
    return [{"level": r["status"], "rule": r["rule"], "ids": r["ids"], "msg": r["evidence"], "action": r["action"]}
            for r in run_rules(rules, "gate", ctx["data"], c)]

def run_gate(ctx: dict) -> dict:
    """tool 介面:全量 Gate(含契約發現)+ KPI,寫回 ctx 與 data。"""
    gate = list(ctx.get("contract_findings") or []) + evaluate_gates(ctx)
    ctx["gate"] = gate
    ctx["kpis"] = kpis(ctx["data"], ctx.get("boundary") or [], gate)
    ctx["data"]["gate"], ctx["data"]["kpis"] = gate, ctx["kpis"]
    return ctx

def kpis(tr: dict, boundary: list, g: list) -> dict:
    fail_ids = {i for x in g if x["level"] == "FAIL" for i in x["ids"]}
    uncovered = [r["id"] for r in tr["requirements"] if r["id"] in fail_ids or any(a in fail_ids for a in r["acs"])]
    return {"req_count": len(tr["requirements"]), "component_count": len(tr["components"]), "test_count": len(tr["tests"]),
            "boundary_pass": sum(b["status"] == "PASS" for b in boundary), "boundary_total": len(boundary),
            "boundary_fail": sum(b["status"] == "FAIL" for b in boundary), "boundary_warn": sum(b["status"] == "WARN" for b in boundary),
            "uncovered_req": len(uncovered), "uncovered_ids": uncovered,
            "open_gaps": len(tr.get("gaps", [])), "assumed": sum(1 for x in g if "assumed" in x["msg"])}
