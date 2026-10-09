"""review.diagrams v1:由表格資料自動生成每條需求的圖(在工具層生成,才能被審計):
- AUTO-TRACE-<REQ>:PM 段落 → REQ → AC → 各層元件 → 測試(flowchart)。
- AUTO-SEQ-<REQ>:沿元件表的 depends 走(只走該需求涉及的元件),訊息 = 該元件對此需求 AC 的職責。
每張圖記下輸入來源(檔:行),審計時用。"""
import re

LORD = ["Page", "Component", "Store", "ApiClient", "Api", "Application", "Domain", "Infrastructure"]

def _mid(s): return re.sub(r"[^A-Za-z0-9]", "", str(s))
def _lab(s): return re.sub(r'["<>]', "'", str(s)).replace("|", "/").replace(";", "；").replace("#", "＃").replace("{", "(").replace("}", ")")

def components_of(data: dict, r: dict) -> list:
    cmps = {c["id"] for c in data["components"]}
    out = {l["component"] for l in data["ac_links"] if l["ac"] in r["acs"]}
    for b in r.get("binds") or []:
        if b in cmps: out.add(b)
        for a in data.get("apis") or []:
            if a["id"] == b: out.update(c for c in a["component"] if c in cmps)
    return sorted(c for c in out if c in cmps)

def pm_section(data: dict, anchor: str):
    secs = ((data.get("sources") or {}).get("pm_spec") or {}).get("sections") or []
    key = str(anchor or "").split(" ")[0]
    return next((s for s in secs if s["anchor"] == key), None)

def trace(data: dict, r: dict) -> dict:
    cmp = {c["id"]: c for c in data["components"]}; rid = _mid(r["id"]); inputs = []
    sec = pm_section(data, r.get("source"))
    pm_file = (((data.get("sources") or {}).get("pm_spec")) or {}).get("path", "")
    if sec: inputs.append(f"{pm_file}:{sec['line']}")
    if r.get("line"): inputs.append(f"{r.get('file', '10-requirements.md')}:{r['line']}")
    L = ["flowchart LR", f'  P{rid}["{_lab((sec["anchor"] + " " + sec["title"]) if sec else r.get("source", ""))}"]:::pm --> {rid}["{_lab(r["id"])}"]:::req']
    cs, ts = set(), set()
    for a in r["acs"]:
        aid = _mid(a); L.append(f'  {rid} --> {aid}(["{_lab(a)}"]):::ac')
        acl = (data.get("ac_text") or {}).get(a)
        if acl: inputs.append(f"10-requirements.md:{acl['line']}")
        for l in [x for x in data["ac_links"] if x["ac"] == a]:
            cs.add(l["component"]); L.append(f"  {aid} --> {_mid(l['component'])}")
            if l.get("line"): inputs.append(f"{l.get('file', '30-architecture-c4.md')}:{l['line']}")
        for t in [x for x in data["tests"] if a in x["acs"]]:
            ts.add(t["id"]); L.append(f"  {aid} -.-> {_mid(t['id'])}")
            if t.get("line"): inputs.append(f"{t.get('file', '60-test-design.md')}:{t['line']}")
    for b in r.get("binds") or []:
        if b in cmp: cs.add(b); L.append(f"  {rid} --> {_mid(b)}")
    by = {}
    for c in cs:
        if c in cmp: by.setdefault(cmp[c]["layer"], []).append(c); inputs.append(f"{cmp[c].get('file', '30-architecture-c4.md')}:{cmp[c].get('line')}")
    for layer in LORD + [k for k in by if k not in LORD]:
        if layer not in by: continue
        L.append(f'  subgraph L{_mid(layer)}["{_lab(layer)}"]')
        for c in sorted(by[layer]): L.append(f'    {_mid(c)}["{_lab(c)}<br/>{_lab(cmp[c]["name"].split(" :")[0])}"]:::cmp')
        L.append("  end")
    for t in sorted(ts):
        tt = next(x for x in data["tests"] if x["id"] == t); L.append(f'  {_mid(t)}[/"{_lab(t)} {_lab(tt["kind"])}"/]:::tst')
    L += ["  classDef pm fill:#fff4d6,stroke:#b58900,color:#3d2e00", "  classDef req fill:#e3eefc,stroke:#1f5f8b,color:#0d2a40",
          "  classDef ac fill:#eef7ee,stroke:#2f7a3f,color:#123d1b", "  classDef cmp fill:#f3f0fa,stroke:#6a4fb3,color:#24164a", "  classDef tst fill:#f6f6f6,stroke:#777,color:#222"]
    return {"id": f"AUTO-TRACE-{r['id']}", "kind": "flowchart", "req": r["id"], "reqs": [r["id"]], "file": "(auto)", "line": None,
            "heading": f"追溯圖 {r['id']}", "mermaid": "\n".join(L), "auto": True, "tool": "review.diagrams@1",
            "inputs": sorted(set(i for i in inputs if i and not i.endswith(":None"))), "edges": len(cs) + len(ts)}

def sequence(data: dict, r: dict):
    cmp = {c["id"]: c for c in data["components"]}; cs = [c for c in components_of(data, r)]
    if not cs: return None
    S = set(cs)
    deps = {c: [d for d in cmp[c]["depends"] if d in S] for c in cs}
    pointed = {d for c in cs for d in deps[c]}
    roots = sorted([c for c in cs if c not in pointed], key=lambda c: LORD.index(cmp[c]["layer"]) if cmp[c]["layer"] in LORD else 99)
    role = lambda c: next((l["role"] or l["ac"] for l in data["ac_links"] if l["component"] == c and l["ac"] in r["acs"]), cmp[c]["layer"])
    L = ["sequenceDiagram", "  autonumber", "  actor U as user/system"]
    L += [f"  participant {_mid(c)} as {_lab(cmp[c]['name'].split(' :')[0].split(' (')[0])}" for c in sorted(cs, key=lambda c: LORD.index(cmp[c]['layer']) if cmp[c]['layer'] in LORD else 99)]
    seen, calls = set(), []
    def walk(c):
        for d in deps[c]:
            calls.append(f"  {_mid(c)}->>{_mid(d)}: {_lab(role(d))[:40]}")
            if d not in seen: seen.add(d); walk(d)
    for root in roots:
        calls.append(f"  U->>{_mid(root)}: {_lab(role(root))[:40]}"); seen.add(root); walk(root)
    L += calls + [f"  {_mid(roots[0])}-->>U: {_lab(', '.join(r['acs']) or r['id'])}"] if roots else calls
    inputs = sorted({f"{cmp[c].get('file', '30-architecture-c4.md')}:{cmp[c].get('line')}" for c in cs if cmp[c].get("line")})
    return {"id": f"AUTO-SEQ-{r['id']}", "kind": "sequence", "req": r["id"], "reqs": [r["id"]], "file": "(auto)", "line": None,
            "heading": f"元件循序圖 {r['id']}", "mermaid": "\n".join(L), "auto": True, "tool": "review.diagrams@1", "inputs": inputs}

def run(ctx: dict) -> dict:
    data = ctx["data"]; out = []
    for r in data["requirements"]:
        out.append(trace(data, r))
        s = sequence(data, r)
        if s: out.append(s)
    ctx.setdefault("carry", {})["auto_diagrams"] = out
    data["auto_diagrams"] = out
    return ctx
