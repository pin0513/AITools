"""predicate 函式庫 v1。每個函式:(data, params, ctx) -> [{"outcome", "target", "ids", "vars"}]。
只回報「發生哪種情況」,不決定嚴重度、不組訊息(那是 rules/*.yaml)。"""
from collections import Counter

def _f(outcome, target, ids=None, **vars):
    vars.setdefault("target", target)
    return {"outcome": outcome, "target": target, "ids": ids or [target], "vars": vars}

def _links_by_req(data):
    cmps = {c["id"] for c in data["components"]}
    ac_owner = {ac: r["id"] for r in data["requirements"] for ac in r["acs"]}
    by = {}
    for l in data["ac_links"]:
        rid = ac_owner.get(l["ac"])
        if rid: by.setdefault(rid, set()).add(l["component"])
    for r in data["requirements"]:
        for b in r.get("binds", []):
            if b in cmps: by.setdefault(r["id"], set()).add(b)
            for a in data["apis"]:
                if a["id"] == b:
                    for c in a["component"]: by.setdefault(r["id"], set()).add(c)
    return by

# ---------- boundary ----------
def requirement_link(data, params, ctx):
    cmps = {c["id"]: c for c in data["components"]}
    by = _links_by_req(data); out = []
    for r in data["requirements"]:
        cs = by.get(r["id"], set())
        if not cs:
            out.append(_f("no_link", r["id"])); continue
        bad = sorted(c for c in cs if c not in cmps or not cmps[c]["layer"] or not cmps[c]["context"])
        if bad: out.append(_f("bad_component", r["id"], [r["id"]] + bad, bad=", ".join(bad)))
        else: out.append(_f("linked", r["id"], [r["id"]] + sorted(cs), cmps=", ".join(sorted(cs))))
        for ac in r["acs"]:
            if not any(l["ac"] == ac for l in data["ac_links"]) and not r.get("binds"):
                out.append(_f("ac_unassigned", ac, [ac, r["id"]], ac=ac))
    return out

def dependency_direction(data, params, ctx):
    layers = list(params.get("layers") or []); allowed = {tuple(x) for x in params.get("allowed") or []}
    cmps = {c["id"]: c for c in data["components"]}; out = []
    for cid, c in cmps.items():
        if c["layer"] not in layers:
            out.append(_f("bad_layer", cid, layer=c["layer"], layers=layers)); continue
        for dep in c["depends"]:
            t = cmps.get(dep)
            if not t: out.append(_f("missing_dep", cid, [cid, dep], dep=dep)); continue
            if t["context"] != c["context"]: continue  # B3 的事
            fl, tl = c["layer"], t["layer"]; v = dict(dep=dep, dep_name=t["name"].split(":")[0].strip(), from_layer=fl, to_layer=tl, interface=t.get("interface", ""))
            if fl == tl: out.append(_f("same_layer", cid, [cid, dep], **v))
            elif (fl, tl) in allowed: out.append(_f("allowed", cid, [cid, dep], **v))
            elif fl == "Application" and tl == "Infrastructure":
                out.append(_f("via_interface" if t.get("interface") else "concrete_infra", cid, [cid, dep], **v))
            elif fl == "Api" and tl == "Infrastructure": out.append(_f("api_to_infra", cid, [cid, dep], **v))
            else: out.append(_f("reverse", cid, [cid, dep], **v))
    return out

def cross_context(data, params, ctx):
    hard = set(params.get("hard_layers") or []); cmps = {c["id"]: c for c in data["components"]}; out = []
    for cid, c in cmps.items():
        for dep in c["depends"]:
            t = cmps.get(dep)
            if t and t["context"] != c["context"]:
                out.append(_f("direct" if t["layer"] in hard else "soft", cid, [cid, dep], dep=dep, to_context=t["context"], to_layer=t["layer"]))
    return out

def external_calls(data, params, ctx):
    adapter = params.get("adapter_layer", "Infrastructure")
    fm = {(f["system"], c) for f in data["failure_modes"] for c in f["component"]}; out = []
    for c in data["components"]:
        for ext in c["external"]:
            if c["layer"] != adapter: out.append(_f("wrong_layer", c["id"], ext=ext, layer=c["layer"]))
            elif (ext, c["id"]) not in fm: out.append(_f("no_failure", c["id"], ext=ext, layer=c["layer"]))
            else: out.append(_f("ok", c["id"], ext=ext, layer=c["layer"]))
    return out

def data_ownership(data, params, ctx):
    own = Counter(o["table"] for o in data["ownership"] if o["owner"]); out = []
    for t in data["erd_entities"]:
        n = own.get(t, 0)
        if n == 0: out.append(_f("no_owner", t))
        elif n > 1: out.append(_f("multi", t, n=n))
        else: out.append(_f("ok", t, owner=next(o["owner"] for o in data["ownership"] if o["table"] == t)))
    for o in data["ownership"]:
        if o["table"] not in data["erd_entities"]: out.append(_f("no_entity", o["table"]))
    return out

def nfr_binding(data, params, ctx):
    cmps = {c["id"] for c in data["components"]}; apis = {a["id"] for a in data["apis"]}; out = []
    for r in data["requirements"]:
        if "non_functional" not in r["types"]: continue
        ok = [b for b in r.get("binds", []) if b in cmps or b in apis]
        out.append(_f("bound", r["id"], [r["id"]] + ok, binds=", ".join(ok)) if ok else _f("unbound", r["id"]))
        if not any(f["nfr"] == r["id"] for f in data["fitness"]): out.append(_f("no_fitness", r["id"]))
    return out

def test_coverage(data, params, ctx):
    tests = data["tests"]; tested_cmp = {c for t in tests for c in t["components"]}; tested_ac = {a for t in tests for a in t["acs"]}; out = []
    for c in data["components"]:
        if c["id"] not in tested_cmp: out.append(_f("cmp_untested", c["id"], suggest=c["name"].split(":")[0].strip() + "Tests"))
    for r in data["requirements"]:
        for ac in r["acs"]:
            if ac in tested_ac: out.append(_f("ac_tested", ac, tests=", ".join(t["id"] for t in tests if ac in t["acs"])))
            else: out.append(_f("ac_untested", ac, [ac, r["id"]], ac=ac, req=r["id"]))
    return out

def tech_whitelist(data, params, ctx):
    tb = (ctx.get("config") or {}).get("tech_boundary") or {}
    wl = {str(v).lower() for v in (tb.get("stack") or {}).values()} | {str(x).lower() for x in (tb.get("tech_allowlist") or [])} | {str(x).lower() for x in params.get("extra_allowlist") or []}
    allowed = lambda t: any(t.lower() == w or t.lower().startswith(w + ".") or t.lower().startswith(w + " ") for w in wl)
    prefix = str(params.get("spike_method_prefix", "spike")).lower(); closed = tuple(str(x).upper() for x in params.get("closed_outcomes") or ["PASS"])
    out = []
    for c in data["components"]:
        bad = [t for t in c["tech"] if not allowed(t)]
        if not bad: continue
        spikes = [e for e in ctx.get("live_log") or [] if str(e.get("method", "")).lower().startswith(prefix) and c["id"] in str(e.get("in", ""))]
        if not spikes: out.append(_f("no_spike", c["id"], bad=", ".join(bad)))
        elif any(str(e.get("out", "")).upper().startswith(closed) for e in spikes): out.append(_f("accepted", c["id"], bad=", ".join(bad)))
        else: out.append(_f("spike_open", c["id"], bad=", ".join(bad)))
    return out

# ---------- gates ----------
def extract_errors(data, params, ctx):
    """stage 內評估時只看屬於該 stage 的結構錯誤(錯誤的 rule 欄 = 檔案契約的 stage);全量評估時全部。"""
    sid = ctx.get("stage_id")
    errs = [e for e in data.get("extract_errors", []) if not sid or e.get("rule") == sid]
    return [_f("fail" if e["level"] == "FAIL" else "warn", e.get("ids", [""])[0] if e.get("ids") else "", e.get("ids") or [], msg=e["msg"]) for e in errs]

def reference_integrity(data, params, ctx):
    out = []
    for kind, items in (("REQ", data["requirements"]), ("CMP", data["components"]), ("TST", data["tests"])):
        seen = set()
        for x in items:
            if x["id"] in seen: out.append(_f("dup", x["id"], kind=kind, id=x["id"]))
            seen.add(x["id"])
    acs = {ac for r in data["requirements"] for ac in r["acs"]}; cmps = {c["id"] for c in data["components"]}
    for l in data["ac_links"]:
        if l["ac"] not in acs: out.append(_f("missing_ac", l["ac"], id=l["ac"]))
        if l["component"] not in cmps: out.append(_f("missing_cmp", l["component"], where="追溯表", id=l["component"]))
    for t in data["tests"]:
        for c in t["components"]:
            if c not in cmps: out.append(_f("missing_cmp", c, [t["id"], c], where=t["id"], id=c))
    return out

def method_log_presence(data, params, ctx):
    stages = set(params.get("stages") or ["S1", "S2"])
    logged = {e["req"] for e in ctx.get("live_log") or [] if e.get("stage") in stages}
    return [_f("none", r["id"], req=r["id"]) for r in data["requirements"] if r["id"] not in logged]

def usecase_postcondition(data, params, ctx):
    return [_f("missing", uc["id"], uc=uc["id"]) for uc in data.get("use_cases", []) if not uc["has_post"]]

def assumed_evidence(data, params, ctx):
    gap_reqs = {r for g in data.get("gaps", []) for r in g["reqs"]}; out = []
    for e in ctx.get("live_log") or []:
        if e.get("evidence") != "assumed": continue
        v = dict(req=e["req"], stage=e["stage"], method=e["method"], gap="; ".join(e.get("gaps") or []) or e.get("note", ""))
        out.append(_f("listed" if e["req"] in gap_reqs or e["req"] == "*" else "unlisted", e["req"], **v))
    return out

def orphans(data, params, ctx):
    return [_f("orphan_test", t["id"], id=t["id"]) for t in data["tests"] if not t["acs"]]

def boundary_failures(data, params, ctx):
    return [_f("fail", b["target"], b["ids"], evidence=b["evidence"]) for b in ctx.get("boundary") or [] if b["status"] == "FAIL"]


# ---------- SA / Survey ----------
def sa_steps(data, params, ctx):
    meth = ctx.get("methodology") or {}
    arts = data.get("sa_artifacts") or []
    present = set(data.get("sa_files") or [])
    out = []
    for st in meth.get("steps") or []:
        f = st["output"]
        if f not in present:
            out.append(_f("missing_output", st["id"], [st["id"], f], step=st["id"], file=f)); continue
        n = 0
        for prefix in st.get("diagrams") or []:
            k = [a for a in arts if a["file"] == f and a["id"].startswith(prefix)]
            if not k: out.append(_f("missing_diagram", st["id"], [st["id"], f], step=st["id"], file=f, prefix=prefix))
            n += len(k)
        out.append(_f("ok", st["id"], [st["id"], f], step=st["id"], file=f, diagrams=n))
    return out

PATH_LAYER = [(".Application/", "Application"), (".Domain/", "Domain"), (".Infrastructure/", "Infrastructure"), (".Api/", "API"),
              ("src/web/", "UI"), ("src/database/", "DB"), ("/api/", "API")]

def layer_of(path: str):
    return next((g for pat, g in PATH_LAYER if pat in path), None)

def _layer_names(toks: list, ctx: dict, layer) -> list:
    """證據行所在層的名字:基礎符號 + 對照表中「該層」的名字。層不明時只用基礎符號。"""
    import re
    if not layer: return list(toks)
    naming = (ctx.get("glossary") or {}).get("naming") or {}
    low = {k.lower(): v for k, v in naming.items()}
    out = list(toks)
    for t in toks:
        for name in (low.get(t.lower()) or {}).get(layer) or []:
            for ident in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", name):
                if ident not in out: out.append(ident)
    return out

def _with_naming(toks: list, ctx: dict) -> list:
    """查分層命名對照表:符號 → 各層實際名稱(GetOrder → GetOrderQueryHandler、getOrder)。"""
    import re
    naming = (ctx.get("glossary") or {}).get("naming") or {}
    low = {k.lower(): v for k, v in naming.items()}
    out = list(toks)
    for t in toks:
        row = low.get(t.lower())
        if not row: continue
        for col in ("UI", "API", "Application", "Domain", "Infrastructure", "DB"):
            for name in row.get(col) or []:
                for ident in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", name):
                    if t.lower() in ident.lower() and ident not in out: out.append(ident)
    return out

def resolve_symbols(element: str, data: dict, ctx: dict, min_len=3) -> tuple:
    """元素名 → 可比對符號清單與來源:ASCII 符號 → 專案詞彙表(名詞→符號)→ 本 spec SA2(實體→英文);再經分層命名對照表展開。"""
    toks, how = _resolve_base(element, data, ctx, min_len)
    full = _with_naming(toks, ctx)
    return full, (how + "+naming" if len(full) > len(toks) else how)

def _resolve_base(element: str, data: dict, ctx: dict, min_len=3) -> tuple:
    import re
    toks = [t for t in re.split(r"[^A-Za-z0-9_]+", element) if len(t) >= min_len]
    if toks: return toks, "ascii"
    zh = re.sub(r"\s*\([^)]*\)", "", element).strip()
    terms = ((ctx.get("glossary") or {}).get("terms") or {})
    g = terms.get(zh) or terms.get(element)
    if g and g.get("symbol"): return [t for t in re.split(r"[^A-Za-z0-9_]+", g["symbol"]) if len(t) >= min_len], "glossary"
    for e in data.get("sa_entities") or []:
        if e["name"] in (zh, element) and e.get("en"): return [t for t in re.split(r"[^A-Za-z0-9_]+", e["en"]) if len(t) >= min_len], "sa2"
    return [], "none"

def glossary_consistency(data, params, ctx):
    """本 spec 的 SA2 實體 vs 專案詞彙表(其他 spec 的條目)。"""
    gl = ctx.get("glossary") or {}; terms = gl.get("terms") or {}
    me = ctx.get("spec_name") or ""; out = []
    by_symbol = {}
    for k, v in terms.items():
        if v.get("symbol"): by_symbol.setdefault(v["symbol"], []).append((k, v))
    for e in data.get("sa_entities") or []:
        if not e.get("en"): continue
        g = terms.get(e["name"])
        others = [s for s in (g["specs"] if g else []) if s != me]
        if g and g.get("symbol") and g["symbol"] != e["en"] and others:
            out.append(_f("term_conflict", e["name"], term=e["name"], symbol=e["en"], other_spec=others[0], other_symbol=g["symbol"]))
        elif g and others:
            out.append(_f("reused", e["name"], term=e["name"], symbol=e["en"], other_spec=others[0]))
        for k, v in by_symbol.get(e["en"], []):
            if k != e["name"] and any(s != me for s in v["specs"]):
                out.append(_f("symbol_conflict", e["name"], term=e["name"], symbol=e["en"], other_spec=[s for s in v["specs"] if s != me][0], other_term=k))
    return out

def survey_evidence(data, params, ctx):
    """證據格式:path:line  或  path:line "字面文字"(多筆以 ; 分隔)。
    有字面文字 → 驗該行含該文字(區分大小寫);否則驗該行含元素符號(ASCII → 詞彙表 → SA2,不分大小寫)。
    解析不到符號且無字面文字 → no_symbol(WARN,請人確認)。"""
    import pathlib, re
    root = ctx.get("project_root"); statuses = set((ctx.get("contracts") or {}).get("survey_status") or ["existing", "modify", "new"])
    min_len = int(params.get("min_token_len", 3)); cands = ctx.get("survey_candidates") or {}
    EV = re.compile(r'^\s*(.+?):(\d+)(?:\s+"(.+)")?\s*$')
    out = []
    for row in data.get("survey") or []:
        el, st, ev = row["element"], row["status"], row["evidence"]
        if st not in statuses: out.append(_f("bad_status", el, element=el, status=st)); continue
        base, how_sym = _resolve_base(el, data, ctx, min_len)
        toks = _with_naming(base, ctx)          # new 的候選比對用全部層
        if st == "new":
            strong = [c for c in cands.get(el, []) if any(re.search(r"\b" + re.escape(t) + r"\b", c[2]) for t in toks)]
            if strong: out.append(_f("new_but_found", el, element=el, evidence=f"{strong[0][0]}:{strong[0][1]}"))
            continue
        if not ev or ":" not in ev: out.append(_f("no_evidence", el, element=el, status=st)); continue
        for one in [e.strip() for e in ev.split(";") if e.strip()]:
            m = EV.match(one)
            if not m: out.append(_f("path_missing", el, element=el, evidence=one)); continue
            path, line, literal = m.group(1), int(m.group(2)), m.group(3)
            fp = (pathlib.Path(root) / path) if root else None
            if not fp or not fp.exists(): out.append(_f("path_missing", el, element=el, evidence=one)); continue
            try: text = fp.read_text(encoding="utf-8", errors="ignore").splitlines()[line - 1]
            except IndexError: out.append(_f("path_missing", el, element=el, evidence=one)); continue
            if literal is not None:
                if literal in text: out.append(_f("verified", el, element=el, evidence=one, how=f'字面 "{literal}"'))
                else: out.append(_f("line_mismatch", el, element=el, evidence=one, tokens=[literal]))
            elif not base:
                out.append(_f("no_symbol", el, element=el, evidence=one))
            else:
                layer = layer_of(path); names = _layer_names(base, ctx, layer)
                hit = next((t for t in names if re.search(r"\b" + re.escape(t) + r"\b", text, re.I)), None)
                if hit:
                    src = "符號" if hit in base and how_sym == "ascii" else (f"{how_sym} 解析" if hit in base else f"對照表 {layer} 層")
                    out.append(_f("verified", el, element=el, evidence=one, how=f"{src} {hit}"))
                else:
                    out.append(_f("line_mismatch", el, element=el, evidence=one, tokens=names))
    return out
