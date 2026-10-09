"""transform.report v1:由 ctx 的 data/boundary/gate/kpis 產生 90-traceability.md 與 boundary-report.md(產生物,不手改)。"""
LAYERS = ["Api", "Application", "Domain", "Infrastructure"]
KINDS = ["unit", "integration", "contract", "e2e"]

def traceability_md(tr, boundary, g, k):
    cmps = {c["id"]: c for c in tr["components"]}
    ac_owner = {ac: r["id"] for r in tr["requirements"] for ac in r["acs"]}
    by_req = {}
    for l in tr["ac_links"]:
        rid = ac_owner.get(l["ac"])
        if rid: by_req.setdefault(rid, set()).add(l["component"])
    for r in tr["requirements"]:
        for b in r.get("binds", []):
            if b in cmps: by_req.setdefault(r["id"], set()).add(b)
    fail_ids = {i for x in g if x["level"] == "FAIL" for i in x["ids"]}
    warn_ids = {i for x in g if x["level"] == "WARN" for i in x["ids"]} | {i for b in boundary if b["status"] == "WARN" for i in b["ids"]}
    lines = [f"# {tr['title']} — 追溯矩陣", "", "<!-- 由 spec-dev.py check 產生,不要手改 -->", "",
             f"需求 {k['req_count']} · 技術元件 {k['component_count']} · 測試元件 {k['test_count']} · 技術邊界 PASS {k['boundary_pass']}/{k['boundary_total']} · 未覆蓋需求 {k['uncovered_req']}", "",
             "## 需求 × 技術元件 × 測試元件", "",
             "| REQ | " + " | ".join(LAYERS) + " | " + " | ".join(KINDS) + " | 狀態 |",
             "|---|" + "---|" * (len(LAYERS) + len(KINDS) + 1)]
    for r in tr["requirements"]:
        cs = by_req.get(r["id"], set())
        ts = [t for t in tr["tests"] if set(t["acs"]) & set(r["acs"])]
        st = "✗" if (r["id"] in fail_ids or any(a in fail_ids for a in r["acs"])) else ("⚠" if (r["id"] in warn_ids or cs & warn_ids) else "✓")
        row = [r["id"]] + [", ".join(sorted(c for c in cs if cmps.get(c, {}).get("layer") == L)) or "·" for L in LAYERS] \
              + [", ".join(t["id"] for t in ts if t["kind"] == K) or "·" for K in KINDS] + [st]
        lines.append("| " + " | ".join(row) + " |")
    lines += ["", "## AC → 技術元件 → 測試", "", "| AC | REQ | CMP(職責) | TST |", "|---|---|---|---|"]
    for ac, rid in ac_owner.items():
        ls = [f"{l['component']}({l['role']})" if l["role"] else l["component"] for l in tr["ac_links"] if l["ac"] == ac]
        ts = [t["id"] for t in tr["tests"] if ac in t["acs"]]
        lines.append(f"| {ac} | {rid} | {', '.join(ls) or '✗'} | {', '.join(ts) or '✗'} |")
    lines += ["", "## Gate 問題", "", "| 等級 | 規則 | 訊息 |", "|---|---|---|"]
    lines += [f"| {x['level']} | {x['rule']} | {x['msg']} |" for x in g] or ["| — | — | 無 |"]
    return "\n".join(lines) + "\n"

def boundary_md(tr, boundary):
    lines = [f"# {tr['title']} — 技術邊界核對報告", "", "<!-- 由 spec-dev.py check 產生,不要手改 -->", "",
             "| 規則 | 目標 | 狀態 | 證據 | 處置 |", "|---|---|---|---|---|"]
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    for b in sorted(boundary, key=lambda b: (order[b["status"]], b["rule"], b["target"])):
        lines.append(f"| {b['rule']} | {b['target']} | {b['status']} | {b['evidence']} | {b['action']} |")
    return "\n".join(lines) + "\n"


def run(ctx: dict) -> dict:
    d, tr = ctx["dir"], ctx["data"]
    from tools.check.engine_v1 import run_gate
    run_gate(ctx)
    boundary, g, k = ctx.get("boundary") or [], ctx["gate"], ctx["kpis"]
    (d / "boundary-report.md").write_text(boundary_md(tr, boundary), encoding="utf-8")
    (d / "90-traceability.md").write_text(traceability_md(tr, boundary, g, k), encoding="utf-8")
    return ctx
