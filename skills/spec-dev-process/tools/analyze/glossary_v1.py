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
    return {"terms": [{"term": k, **{x: v[x] for x in ("symbol", "definition", "specs", "source")}} for k, v in gl["terms"].items()],
            "conflicts": gl["conflicts"], "path": str(out.relative_to(root)) if out.is_relative_to(root) else str(out)}

def run(ctx: dict) -> dict:
    root, cfg = ctx["project_root"], ctx["config"]
    merged, conflicts = collect(root, cfg, ctx["contracts"])
    out = root / ((cfg.get("glossary") or {}).get("path") or "specs/glossary.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(glossary_md(merged, conflicts), encoding="utf-8")
    ctx["glossary"] = {"terms": merged, "conflicts": conflicts, "path": str(out)}
    if ctx.get("data") is not None:
        ctx["data"]["glossary"] = to_data(ctx["glossary"], root)
    return ctx
