"""review.checks v1:圖與表的核對函式庫。每個函式 (item, parsed, data, ctx) -> [(outcome, msg_vars)]。
outcome 的嚴重度在 rules/gates/G-DG-consistency.yaml(圖)與 G-SA-tables.yaml(表)。函式只回報情況。"""
import re

def _ident(name): return re.split(r"\s*[:(]", str(name))[0].strip()

def _cmp_index(data):
    """名稱 / 介面 / ID(去 dash)→ CMP id。"""
    idx = {}
    for c in data.get("components") or []:
        idx[c["id"].lower()] = c["id"]; idx[c["id"].replace("-", "").lower()] = c["id"]
        idx[_ident(c["name"]).lower()] = c["id"]
        if c.get("interface"): idx[_ident(c["interface"]).lower()] = c["id"]
        m = re.match(r"([A-Za-z_]\w*)", c["name"])
        if m: idx.setdefault(m.group(1).lower(), c["id"])
    return idx

def _deps(data): return {c["id"]: set(c["depends"]) for c in data.get("components") or []}

def _action_symbols(data):
    syms = set()
    for r in data.get("sa_roles") or []:
        m = re.match(r"\s*([A-Za-z_]\w*)", r.get("action", ""))
        if m: syms.add(m.group(1).lower())
    for c in data.get("components") or []: syms.add(_ident(c["name"]).lower())
    for n in ((data.get("glossary") or {}).get("naming") or []): syms.add(str(n.get("symbol", "")).lower())
    return syms

def _role_names(data):
    names = {str(r["role"]).lower() for r in data.get("sa_roles") or []}
    for w in (data.get("sa_tables") or {}).get("words") or []:
        for m in re.finditer(r"(?:Actor|actor)\s*[:：]\s*([A-Za-z_]\w*)", w.get("歸類", "")): names.add(m.group(1).lower())
    return names

# ---------- 圖 ----------
def seq_calls_follow_dependencies(item, p, data, ctx):
    idx, deps, out = _cmp_index(data), _deps(data), []
    if not data.get("components"): return out
    to_cmp = {}
    for pid, alias in p.get("participants", {}).items():
        if pid in p.get("actors", set()): continue
        c = idx.get(_ident(alias).lower()) or idx.get(pid.lower())
        if c: to_cmp[pid] = c
        else: out.append(("seq_unknown_participant", {"participant": alias}))
    for call in p.get("calls", []):
        if call["reply"] or call["from"] == call["to"]: continue
        a, b = to_cmp.get(call["from"]), to_cmp.get(call["to"])
        if a and b and b not in deps.get(a, set()):
            out.append(("seq_no_dependency", {"from": f"{call['from']}({a})", "to": f"{call['to']}({b})"}))
    return out

def c4_relations_follow_dependencies(item, p, data, ctx):
    idx, deps, out = _cmp_index(data), _deps(data), []
    m = {k: idx.get(_ident(v).lower()) for k, v in p.get("components", {}).items()}
    for k, v in p.get("components", {}).items():
        if not m[k]: out.append(("c4_unknown_component", {"component": v}))
    if not p.get("components") and p.get("nodes"):      # flowchart 版 C4-L3:節點 ID 即 CMP 去 dash
        m = {k: idx.get(k.lower()) for k in p["nodes"]}
    for a, b in p.get("relations") or p.get("edges") or []:
        ca, cb = m.get(a), m.get(b)
        if ca and cb and cb not in deps.get(ca, set()):
            out.append(("c4_no_dependency", {"from": ca, "to": cb}))
    return out

def class_names_known(item, p, data, ctx):
    known = {str(e.get("en", "")).lower() for e in data.get("sa_entities") or []} | {_ident(c["name"]).lower() for c in data.get("components") or []}
    known |= {str(n.get("symbol", "")).lower() for n in ((data.get("glossary") or {}).get("naming") or [])}
    return [("class_unknown", {"cls": c}) for c in sorted(p.get("classes", [])) if c.lower() not in known]

def class_in_sa_entities(item, p, data, ctx):
    known = {str(e.get("en", "")).lower() for e in data.get("sa_entities") or []}
    return [("class_not_in_sa2", {"cls": c}) for c in sorted(p.get("classes", [])) if c.lower() not in known]

def state_events_are_actions(item, p, data, ctx):
    syms = _action_symbols(data)
    if not syms: return []
    out = []
    for t in p.get("transitions", []):
        ev = (t.get("event_name") or "").lower()
        if ev and not any(ev == s or s.startswith(ev) or ev.startswith(s) for s in syms if s):
            out.append(("state_event_unmapped", {"event": t["event_name"], "edge": f"{t['from']}→{t['to']}"}))
    return out

def state_handoff_subset(item, p, data, ctx):
    ent = re.search(r"([A-Z][A-Za-z0-9]+)\.Status", item.get("heading", ""))
    if not ent: return []
    from tools.review.mermaid_v1 import parse
    out = []
    for a in data.get("sa_artifacts") or []:
        if a["id"].startswith("STM-SA-") and f"{ent.group(1)}.Status" in a.get("heading", ""):
            missing = sorted(parse(a["mermaid"]).get("states", set()) - p.get("states", set()))
            if missing: out.append(("state_handoff_missing", {"sa": a["id"], "states": ", ".join(missing)}))
    return out

def er_entities_owned(item, p, data, ctx):
    owned = {o["table"].lower() for o in data.get("ownership") or []}
    return [("er_unowned", {"entity": e}) for e in sorted(p.get("entities", [])) if e.lower() not in owned]

def trace_has_edges(item, p, data, ctx):
    return [] if (item.get("edges") or 0) > 0 else [("trace_empty", {"req": item.get("req")})]

def ucd_covers_roles(item, p, data, ctx):
    labels = " ".join(list(p.get("nodes", {}).values()) + list(p.get("nodes", {}).keys())).lower()
    return [("ucd_role_missing", {"role": r}) for r in sorted({str(x["role"]) for x in data.get("sa_roles") or []}) if r.lower() not in labels]

def seq_actor_is_role(item, p, data, ctx):
    roles = _role_names(data)
    if not roles: return []
    return [("seq_actor_unknown", {"actor": p["participants"].get(a, a)}) for a in sorted(p.get("actors", []))
            if p["participants"].get(a, a).lower() not in roles and a.lower() not in roles]

# ---------- SA 表 ----------
def anchors_exist(row, data, ctx):
    secs = {s["anchor"] for s in (((data.get("sources") or {}).get("pm_spec") or {}).get("sections") or [])}
    if not secs: return []
    src = row.get("來源", "")
    anchors = re.findall(r"PM§[\w.]+", src)
    return [("anchor_missing", {"anchor": a}) for a in anchors if a not in secs]

def symbols_present(row, data, ctx):
    return [] if re.match(r"[A-Za-z_]\w*", row.get("英文", "") or "") else [("symbol_missing", {"term": row.get("實體", "")})]

def req_refs_exist(row, data, ctx):
    ids = {r["id"] for r in data.get("requirements") or []}
    refs = re.findall(r"\b(?:REQ|NFR)-\d+\b", row.get("對應 REQ", ""))
    return [("req_missing", {"req": x}) for x in refs if x not in ids] + ([] if refs else [("req_unassigned", {"row": row.get("動作", "")})])

def action_has_symbol(row, data, ctx):
    return [] if re.match(r"\s*[A-Z][A-Za-z0-9]+", row.get("動作", "")) else [("action_symbol_missing", {"row": row.get("動作", "")})]
