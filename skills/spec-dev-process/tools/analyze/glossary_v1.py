"""analyze.glossary v1:跨 spec 詞彙表。掃 config.glossary.spec_roots 下每個 <issue>/spec(+ 其 review_dir 的 sa/02、survey-mapping),
抽 名詞 ↔ 符號 ↔ 定義,合併寫到 config.glossary.path(產生物);同名詞不同符號列入「衝突」表。ctx["glossary"] 供 survey / G-GL 用。"""
import pathlib, re
from core import mdtables as M

def collect(project_root: pathlib.Path, cfg: dict, contracts: dict) -> tuple:
    project_root = pathlib.Path(project_root).resolve()
    gl = cfg.get("glossary") or {}
    sig = {k: v["signature"] for k, v in contracts["tables"].items()}
    review_rel = (cfg.get("output") or {}).get("review_dir") or "."
    entries = []   # {term, symbol, definition, spec, source}
    for root in (gl.get("spec_roots") or ["specs/rd"]):
        base = project_root / root
        if not base.exists(): continue
        for spec_dir in sorted(p for p in base.glob("*/spec") if p.is_dir()):
            spec = spec_dir.parent.name
            review = (spec_dir / review_rel).resolve()
            files = [(spec_dir / "00-overview.md", "glossary_table"), (review / "sa" / "02-entities-relations.md", "sa_entities"), (review / "survey-mapping.md", "survey")]
            for f, want in files:
                if want not in (gl.get("sources") or []) or not f.exists(): continue
                f = f.resolve(); rel = str(f.relative_to(project_root)) if f.is_relative_to(project_root) else f.name
                for t in M.parse(f.name, f.read_text(encoding="utf-8")).tables:
                    name = M.classify(t, sig)
                    for r in t.rows:
                        if name == "sa_entities" and want == "sa_entities" and r.get("英文"):
                            entries.append({"term": r["實體"], "symbol": r["英文"], "definition": r.get("屬性", ""), "spec": spec, "source": f"{rel}:{r['_line']}"})
                        elif name == "glossary" and want == "glossary_table":
                            m = re.search(r"\(([A-Za-z][\w.]*)\)", r["名詞"]) or re.search(r"\b([A-Z][A-Za-z0-9]+)\b", r.get("定義", ""))
                            entries.append({"term": re.sub(r"\s*\([^)]*\)", "", r["名詞"]).strip(), "symbol": m.group(1) if m else "", "definition": r.get("定義", ""), "spec": spec, "source": f"{rel}:{r['_line']}"})
                        elif name == "survey" and want == "survey":
                            m = re.match(r"^(.*?)\s*\(([A-Za-z][\w.]*)\)\s*$", r["模型元素"])
                            if m: entries.append({"term": m.group(1).strip(), "symbol": m.group(2), "definition": r.get("說明", ""), "spec": spec, "source": f"{rel}:{r['_line']}"})
    merged, conflicts = {}, []
    for e in entries:
        key = e["term"]
        if key in merged:
            m = merged[key]
            if e["symbol"] and m["symbol"] and e["symbol"] != m["symbol"]:
                conflicts.append({"term": key, "symbol_a": m["symbol"], "source_a": f"{m['spec']} {m['source']}", "symbol_b": e["symbol"], "source_b": f"{e['spec']} {e['source']}"})
            elif not m["symbol"] and e["symbol"]:
                m["symbol"] = e["symbol"]; m["source"] = e["source"]; m["spec"] = e["spec"]
            if not m["definition"] and e["definition"]: m["definition"] = e["definition"]
            if e["spec"] not in m["specs"]: m["specs"].append(e["spec"])
        else:
            merged[key] = {**e, "specs": [e["spec"]]}
    return merged, conflicts

LAYER_GROUP = {"Page": "UI", "Component": "UI", "Store": "UI", "ApiClient": "UI", "Api": "API",
               "Application": "Application", "Domain": "Domain", "Infrastructure": "Infrastructure"}
NAMING_COLS = ["UI", "API", "Application", "Domain", "Infrastructure", "DB"]

def _ident(name: str) -> str:
    return re.split(r"\s*[:(]", name)[0].strip()

def _matches(sym: str, name: str) -> bool:
    return sym.lower() in name.lower()

def naming_from_spec(spec_dir: pathlib.Path, review: pathlib.Path, contracts: dict, spec: str) -> dict:
    """一份 spec → {symbol: {"term", "spec", UI: [...], API: [...], ...}}。符號來自 SA2 實體與 SA3 動作。"""
    from tools.analyze.extract_v1 import extract
    data = extract(spec_dir, contracts, review)
    syms = [(e["en"], e["name"]) for e in data.get("sa_entities") or [] if e.get("en")]
    action_api = {}
    for r in data.get("sa_roles") or []:
        m = re.match(r"\s*([A-Z][A-Za-z0-9]+)\s*(?:\((.*)\))?", r.get("action", ""))
        if m:
            syms.append((m.group(1), r.get("flow", "")))
            if m.group(2) and m.group(2).lower() != "job": action_api[m.group(1)] = m.group(2).strip()
    out = {}
    for sym, term in syms:
        row = {"term": term, "spec": spec, **{c: [] for c in NAMING_COLS}}
        for c in data.get("components") or []:
            grp = LAYER_GROUP.get(c["layer"])
            if grp and _matches(sym, c["name"]):
                ident = _ident(c["name"])
                if ident not in row[grp]: row[grp].append(ident)
        if sym in action_api: row["API"].insert(0, action_api[sym])
        for t in data.get("erd_entities") or []:
            if _matches(sym, t): row["DB"].append(t)
        if any(row[c] for c in NAMING_COLS) or sym not in out: out[sym] = row
    # 既有程式碼命名:survey 的「對應 codebase」欄 + 證據路徑判層(*.Application/ → Application、src/web → UI…)
    for r in data.get("survey") or []:
        # 點號串只取最後一段(Forms.Domain.FormSubmission → FormSubmission;命名空間片段不是類別名)
        targets = [chain.split(".")[-1] for chain in re.findall(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", r.get("target") or "")]
        targets = [t for t in targets if len(t) >= 3]
        path = (r.get("evidence") or "").split(":")[0]
        grp = next((g for pat, g in PATH_LAYER if pat in path), None)
        if not targets or not grp: continue
        base = re.findall(r"[A-Z][A-Za-z0-9]{2,}", r["element"])
        sym = base[0] if base else targets[0]
        # 只收和符號相關的識別字:命名空間片段(Forms.Domain.X 的 Forms、Domain)不收,否則 namespace 行會被誤判成證據
        keep = [t for t in targets if sym.lower() in t.lower()]
        if not keep: continue
        row = out.setdefault(sym, {"term": r["element"], "spec": spec, **{c: [] for c in NAMING_COLS}})
        for t in keep:
            if t not in row[grp]: row[grp].append(t)
    return out

from tools.check.predicates_v1 import PATH_LAYER  # noqa: E402  與證據驗證共用同一份判層規則

def load_overrides(project_root: pathlib.Path, contracts: dict, path: str) -> dict:
    """手寫覆寫檔(同欄位),有值的格子覆蓋自動推導。"""
    p = project_root / path
    if not p.exists(): return {}
    sig = {k: v["signature"] for k, v in contracts["tables"].items()}
    out = {}
    for t in M.parse(p.name, p.read_text(encoding="utf-8")).tables:
        if M.classify(t, sig) != "naming_map": continue
        for r in t.rows:
            out[r["符號"]] = {"term": r.get("名詞", ""), **{c: [x.strip() for x in r.get(c, "").split(",") if x.strip()] for c in NAMING_COLS}}
    return out

def collect_naming(project_root: pathlib.Path, cfg: dict, contracts: dict) -> dict:
    project_root = pathlib.Path(project_root).resolve(); gl = cfg.get("glossary") or {}
    review_rel = (cfg.get("output") or {}).get("review_dir") or "."
    merged = {}
    for root in (gl.get("spec_roots") or ["specs/rd"]):
        for spec_dir in sorted(p for p in (project_root / root).glob("*/spec") if p.is_dir()):
            for sym, row in naming_from_spec(spec_dir, (spec_dir / review_rel).resolve(), contracts, spec_dir.parent.name).items():
                m = merged.setdefault(sym, {"term": row["term"], "specs": [], **{c: [] for c in NAMING_COLS}})
                if row["spec"] not in m["specs"]: m["specs"].append(row["spec"])
                if not m["term"]: m["term"] = row["term"]
                for c in NAMING_COLS:
                    for x in row[c]:
                        if x not in m[c]: m[c].append(x)
    for sym, ov in load_overrides(project_root, contracts, gl.get("naming_overrides") or "specs/naming-overrides.md").items():
        m = merged.setdefault(sym, {"term": ov["term"], "specs": ["(override)"], **{c: [] for c in NAMING_COLS}})
        for c in NAMING_COLS:
            if ov[c]: m[c] = ov[c]
        if ov["term"]: m["term"] = ov["term"]
        m["override"] = True
    return merged

def naming_md(naming: dict) -> str:
    L = ["# 分層命名對照表(跨 spec)", "", "<!-- 由 analyze.glossary 產生,不手改。要修正某格,寫在 specs/naming-overrides.md(同欄位,有值的格子覆蓋這裡)-->", "",
         "## 分層命名對照", "", "| 名詞 | 符號 | UI | API | Application | Domain | Infrastructure | DB | 來源 spec |", "|---|---|---|---|---|---|---|---|---|"]
    for sym in sorted(naming):
        r = naming[sym]
        L.append(f"| {r['term']} | {sym} | " + " | ".join(", ".join(r[c]) for c in NAMING_COLS) + f" | {', '.join(r['specs'])}{' (override)' if r.get('override') else ''} |")
    return "\n".join(L) + "\n"

def glossary_md(merged: dict, conflicts: list) -> str:
    lines = ["# 專案詞彙表(跨 spec)", "", "<!-- 由 analyze.glossary 產生,不手改;要改符號請改來源 spec 的 SA2 實體表或名詞表 -->", "",
             "## 詞彙", "", "| 名詞 | 符號 | 定義 | 來源 spec | 來源 |", "|---|---|---|---|---|"]
    for k in sorted(merged, key=lambda k: (merged[k]["symbol"] or "~", k)):
        m = merged[k]; lines.append(f"| {k} | {m['symbol']} | {m['definition'][:80]} | {', '.join(m['specs'])} | {m['source']} |")
    lines += ["", "## 衝突", "", "| 名詞 | 符號 A | 來源 A | 符號 B | 來源 B |", "|---|---|---|---|---|"]
    lines += [f"| {c['term']} | {c['symbol_a']} | {c['source_a']} | {c['symbol_b']} | {c['source_b']} |" for c in conflicts] or ["| (無) | | | | |"]
    return "\n".join(lines) + "\n"

def to_data(gl: dict, root) -> dict:
    """ctx["glossary"] → 可序列化、放進 traceability.json 的形式。"""
    import pathlib
    out = pathlib.Path(gl["path"]); root = pathlib.Path(root).resolve()
    np_ = pathlib.Path(gl.get("naming_path") or out)
    return {"terms": [{"term": k, **{x: v[x] for x in ("symbol", "definition", "specs", "source")}} for k, v in gl["terms"].items()],
            "conflicts": gl["conflicts"], "path": str(out.relative_to(root)) if out.is_relative_to(root) else str(out),
            "naming": [{"symbol": k, **v} for k, v in sorted((gl.get("naming") or {}).items())],
            "naming_path": str(np_.relative_to(root)) if np_.is_relative_to(root) else str(np_)}

def run(ctx: dict) -> dict:
    root, cfg = ctx["project_root"], ctx["config"]
    merged, conflicts = collect(root, cfg, ctx["contracts"])
    out = root / ((cfg.get("glossary") or {}).get("path") or "specs/glossary.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(glossary_md(merged, conflicts), encoding="utf-8")
    naming = collect_naming(root, cfg, ctx["contracts"])
    npath = root / ((cfg.get("glossary") or {}).get("naming_path") or "specs/naming-map.md")
    npath.write_text(naming_md(naming), encoding="utf-8")
    ctx["glossary"] = {"terms": merged, "conflicts": conflicts, "path": str(out), "naming": naming, "naming_path": str(npath)}
    if ctx.get("data") is not None:
        ctx["data"]["glossary"] = to_data(ctx["glossary"], root)
    return ctx
