"""技術邊界規則 B1–B8 與 Gate 檢查,全部由資料機械計算。LLM 只負責產生資料與 action。
每筆結果:{rule, target, status, evidence, action, ids}。"""
from collections import Counter

LAYER_RANK = {"Api": 0, "Application": 1, "Domain": 2, "Infrastructure": 3}
# 允許的依賴方向 (from → to);其餘依 _b2 判定
ALLOWED = {("Api", "Application"), ("Api", "Domain"), ("Application", "Domain"),
           ("Infrastructure", "Domain"), ("Infrastructure", "Application")}

def _r(rule, target, status, evidence, action="", ids=None):
    return {"rule": rule, "target": target, "status": status, "evidence": evidence, "action": action, "ids": ids or [target]}

def run(tr: dict, log: list, cfg: dict):
    out = []
    reqs = {r["id"]: r for r in tr["requirements"]}
    cmps = {c["id"]: c for c in tr["components"]}
    tests = tr["tests"]
    ac_owner = {ac: r["id"] for r in reqs.values() for ac in r["acs"]}
    ac_links = tr["ac_links"]
    links_by_req = {}
    for l in ac_links:
        rid = ac_owner.get(l["ac"])
        if rid: links_by_req.setdefault(rid, set()).add(l["component"])
    for r in reqs.values():
        for b in r.get("binds", []):
            if b in cmps: links_by_req.setdefault(r["id"], set()).add(b)
            for a in tr["apis"]:
                if a["id"] == b:
                    for c in a["component"]: links_by_req.setdefault(r["id"], set()).add(c)
    tb = cfg.get("tech_boundary", {})
    layers = set(tb.get("layers") or LAYER_RANK)
    whitelist = {str(v).lower() for v in (tb.get("stack") or {}).values()} | {str(x).lower() for x in (tb.get("tech_allowlist") or [])}
    def allowed(tech: str) -> bool:
        t = tech.lower()
        return any(t == w or t.startswith(w + ".") or t.startswith(w + " ") for w in whitelist)
    superseded = {e["supersedes"] for e in log if "supersedes" in e}
    live = [e for e in log if e.get("seq") not in superseded]

    # B1
    for rid, r in reqs.items():
        cs = links_by_req.get(rid, set())
        if not cs:
            out.append(_r("B1", rid, "FAIL", "無任何 AC→CMP link(或 NFR 綁定)", "在 30-architecture-c4.md 的追溯表補 AC→CMP", [rid]))
            continue
        bad = [c for c in cs if c not in cmps or not cmps[c]["layer"] or not cmps[c]["context"]]
        if bad: out.append(_r("B1", rid, "FAIL", f"link 到的 CMP 不存在或缺 layer/context: {', '.join(bad)}", "補 Component 表格", [rid] + bad))
        else: out.append(_r("B1", rid, "PASS", f"link → {', '.join(sorted(cs))}", "", [rid] + sorted(cs)))
        for ac in r["acs"]:
            if not any(l["ac"] == ac for l in ac_links) and not r.get("binds"):
                out.append(_r("B1", ac, "WARN", f"{ac} 未指定由哪個 CMP 強制", "追溯表補 AC→CMP 與職責", [ac, rid]))
    # B2 / B3
    for cid, c in cmps.items():
        if c["layer"] not in layers:
            out.append(_r("B2", cid, "FAIL", f"layer '{c['layer']}' 不在 {sorted(layers)}", "修正 Layer 欄", [cid])); continue
        for dep in c["depends"]:
            t = cmps.get(dep)
            if not t:
                out.append(_r("B2", cid, "FAIL", f"depends 指向不存在的 {dep}", "修正 depends", [cid, dep])); continue
            if t["context"] != c["context"]:
                if t["layer"] in ("Infrastructure", "Domain"):
                    out.append(_r("B3", cid, "FAIL", f"跨 context 直接依賴 {dep} ({t['context']}/{t['layer']})", "改經 API/Event 契約", [cid, dep]))
                else:
                    out.append(_r("B3", cid, "WARN", f"跨 context 依賴 {dep} ({t['context']}/{t['layer']}),需有 API/Event 定義", "在 40-api-contracts.md 定義契約", [cid, dep]))
                continue
            fl, tl = c["layer"], t["layer"]
            if fl == tl:
                out.append(_r("B2", cid, "PASS", f"→ {dep} 同層 {fl}", "", [cid, dep]))
            elif (fl, tl) in ALLOWED:
                out.append(_r("B2", cid, "PASS", f"{fl} → {dep} ({tl})", "", [cid, dep]))
            elif fl == "Application" and tl == "Infrastructure":
                if t.get("interface"):
                    out.append(_r("B2", cid, "PASS", f"Application → {dep} 經介面 {t['interface']}", "", [cid, dep]))
                else:
                    out.append(_r("B2", cid, "WARN", f"Application 依賴 Infrastructure 具體類別 {dep}", f"為 {t['name']} 定義介面(名稱欄寫 'Impl : IFoo'),Handler 改依賴介面", [cid, dep]))
            elif fl == "Api" and tl == "Infrastructure":
                out.append(_r("B2", cid, "WARN", f"Api 直接依賴 Infrastructure {dep}", "經 Application 或 DI 組態", [cid, dep]))
            else:
                out.append(_r("B2", cid, "FAIL", f"反向依賴:{fl} → {dep} ({tl})", f"在 {fl if fl=='Domain' else 'Domain'} 定義介面,由 {tl} 實作", [cid, dep]))
    # B4
    fm_index = {(f["system"], c) for f in tr["failure_modes"] for c in f["component"]}
    for cid, c in cmps.items():
        for ext in c["external"]:
            if c["layer"] != "Infrastructure":
                out.append(_r("B4", cid, "FAIL", f"外部系統 {ext} 呼叫出現在 {c['layer']} 層", "移到 Infrastructure Adapter", [cid]))
            elif (ext, cid) not in fm_index:
                out.append(_r("B4", cid, "WARN", f"{ext} 呼叫在 Infrastructure,但 40-api-contracts.md 無失敗模式列", "補逾時/重試/降級/補償", [cid]))
            else:
                out.append(_r("B4", cid, "PASS", f"{ext} 在 Infrastructure 且有失敗模式", "", [cid]))
    # B5
    own = Counter(o["table"] for o in tr["ownership"] if o["owner"])
    for t in tr["erd_entities"]:
        n = own.get(t, 0)
        if n == 0: out.append(_r("B5", t, "FAIL", "erDiagram 有此表但擁有權表無 owner", "50-data-model.md 擁有權表補列", [t]))
        elif n > 1: out.append(_r("B5", t, "FAIL", f"多 owner({n})", "只留一個 owner", [t]))
        else: out.append(_r("B5", t, "PASS", f"owner = {next(o['owner'] for o in tr['ownership'] if o['table']==t)}", "", [t]))
    for o in tr["ownership"]:
        if o["table"] not in tr["erd_entities"]:
            out.append(_r("B5", o["table"], "WARN", "擁有權表有列但 erDiagram 無此實體", "補 erDiagram 或刪列", [o["table"]]))
    # B6
    api_ids = {a["id"] for a in tr["apis"]}
    for r in reqs.values():
        if "non_functional" not in r["types"]: continue
        binds = r.get("binds", [])
        ok = [b for b in binds if b in cmps or b in api_ids]
        if ok: out.append(_r("B6", r["id"], "PASS", f"綁定 {', '.join(ok)}", "", [r["id"]] + ok))
        else: out.append(_r("B6", r["id"], "WARN", "未綁定任何 CMP/API", "NFR 表「綁定 CMP/API」欄填入", [r["id"]]))
        if not any(f["nfr"] == r["id"] for f in tr["fitness"]):
            out.append(_r("B6", r["id"], "WARN", "無 Fitness Function", "60-test-design.md 補量測方式與門檻", [r["id"]]))
    # B7
    tested_cmp = {c for t in tests for c in t["components"]}
    tested_ac = {a for t in tests for a in t["acs"]}
    for cid in cmps:
        if cid not in tested_cmp: out.append(_r("B7", cid, "WARN", "無測試元件", f"新增 {cmps[cid]['name'].split(':')[0].strip()}Tests", [cid]))
    for ac, rid in ac_owner.items():
        if ac not in tested_ac: out.append(_r("B7", ac, "FAIL", f"{ac}({rid})無測試元件", "60-test-design.md 補對應", [ac, rid]))
        else: out.append(_r("B7", ac, "PASS", f"→ {', '.join(t['id'] for t in tests if ac in t['acs'])}", "", [ac]))
    # B8
    for cid, c in cmps.items():
        bad = [t for t in c["tech"] if not allowed(t)]
        if not bad: continue
        spike = [e for e in live if str(e.get("method", "")).lower().startswith("spike") and cid in str(e.get("in", ""))]
        if not spike: out.append(_r("B8", cid, "FAIL", f"技術 {', '.join(bad)} 不在白名單且無 Spike 記錄", "加入 tech_allowlist 或開 Spike(method-log method=Spike.*)", [cid]))
        elif any(str(e.get("out", "")).upper().startswith(("PASS", "ACCEPT", "採用")) for e in spike):
            out.append(_r("B8", cid, "PASS", f"{', '.join(bad)} 經 Spike 採用", "", [cid]))
        else: out.append(_r("B8", cid, "WARN", f"{', '.join(bad)} 有 Spike 但未結案", "Spike 結案後 out 寫 PASS/採用", [cid]))
    return out

def gate(tr: dict, log: list, boundary: list):
    """S0–S6 Gate:孤兒、0 筆方法論需求、assumed 證據、UC 缺後置條件。"""
    g = list(tr.get("extract_errors", []))
    reqs = {r["id"] for r in tr["requirements"]}
    cmps = {c["id"] for c in tr["components"]}
    ac_owner = {ac: r["id"] for r in tr["requirements"] for ac in r["acs"]}
    superseded = {e["supersedes"] for e in log if "supersedes" in e}
    live = [e for e in log if e.get("seq") not in superseded]
    logged = {e["req"] for e in live if e.get("stage") in ("S1", "S2")}
    for rid in reqs:
        if rid not in logged: g.append({"level": "FAIL", "rule": "M*", "ids": [rid], "msg": f"{rid} 在 S1/S2 無方法論 log(0 筆)"})
    for l in tr["ac_links"]:
        if l["ac"] not in ac_owner: g.append({"level": "FAIL", "rule": "S5", "ids": [l["ac"]], "msg": f"追溯表 AC {l['ac']} 不存在於需求清單"})
        if l["component"] not in cmps: g.append({"level": "FAIL", "rule": "S5", "ids": [l["component"]], "msg": f"追溯表 CMP {l['component']} 不存在"})
    for t in tr["tests"]:
        if not t["acs"]: g.append({"level": "FAIL", "rule": "S5", "ids": [t["id"]], "msg": f"{t['id']} 未對應任何 AC(孤兒測試)"})
        for c in t["components"]:
            if c not in cmps: g.append({"level": "FAIL", "rule": "S5", "ids": [t["id"], c], "msg": f"{t['id']} 對應不存在的 {c}"})
    for e in live:
        if e.get("evidence") == "assumed":
            g.append({"level": "WARN", "rule": "M*", "ids": [e["req"]], "msg": f"{e['req']} {e['stage']} {e['method']} 證據=assumed:{'; '.join(e.get('gaps') or []) or e.get('note','')}"})
    for uc in tr.get("use_cases", []):
        if not uc["has_post"]: g.append({"level": "WARN", "rule": "M1", "ids": [uc["id"]], "msg": f"{uc['id']} 缺後置條件(不變量與測試斷言的來源)"})
    bf = [b for b in boundary if b["status"] == "FAIL"]
    for b in bf: g.append({"level": "FAIL", "rule": b["rule"], "ids": b["ids"], "msg": f"{b['target']}: {b['evidence']}"})
    return g

def kpis(tr, boundary, g):
    fail_ids = {i for x in g if x["level"] == "FAIL" for i in x["ids"]}
    uncovered = [r["id"] for r in tr["requirements"] if r["id"] in fail_ids or any(a in fail_ids for a in r["acs"])]
    return {"req_count": len(tr["requirements"]), "component_count": len(tr["components"]), "test_count": len(tr["tests"]),
            "boundary_pass": sum(b["status"] == "PASS" for b in boundary), "boundary_total": len(boundary),
            "boundary_fail": sum(b["status"] == "FAIL" for b in boundary), "boundary_warn": sum(b["status"] == "WARN" for b in boundary),
            "uncovered_req": len(uncovered), "uncovered_ids": uncovered,
            "open_gaps": len(tr.get("gaps", [])), "assumed": sum(1 for x in g if "assumed" in x["msg"])}
