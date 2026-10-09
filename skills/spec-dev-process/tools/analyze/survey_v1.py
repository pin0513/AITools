"""analyze.survey v1:Survey Mapping 候選產生。讀 review_dir/sa/02 的實體英文名與 03 的動作、10 的 REQ,掃 codebase 找出現位置,
寫 review_dir/survey-candidates.md(產生物)。定案的 survey-mapping.md 由人/LLM 寫,G-SV-evidence 驗證其證據。"""
import pathlib, re
from core import mdtables as M

STOP = {"GET", "POST", "PUT", "DELETE", "PATCH", "HTTP", "API", "ID"}

def _tokens(name: str, min_len=3):
    return [t for t in re.split(r"[^A-Za-z0-9_]+", name) if len(t) >= min_len]

def scan(project_root: pathlib.Path, cfg: dict, elements: list) -> dict:
    sv = cfg.get("survey") or {}
    roots = [project_root / r for r in (sv.get("code_roots") or ["src"])]
    exts = set(sv.get("extensions") or [".cs", ".ts", ".tsx", ".sql"]); ignore = set(sv.get("ignore") or [])
    limit = int(sv.get("max_candidates_per_element") or 5)
    files = []
    for root in roots:
        if not root.exists(): continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix in exts and not (set(p.parts) & ignore): files.append(p)
    hits = {}
    for el in elements:
        toks = _tokens(el)
        if not toks: continue
        pat = re.compile(r"\b(" + "|".join(re.escape(t) for t in toks) + r")\b", re.I)
        found = []
        for p in files:
            try: lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError: continue
            for n, line in enumerate(lines, 1):
                if pat.search(line):
                    found.append((str(p.relative_to(project_root)), n, line.strip()[:100]))
                    if len(found) >= limit: break
            if len(found) >= limit: break
        hits[el] = found
    return hits

def elements_from_sa(review_dir: pathlib.Path, contracts: dict, data: dict) -> list:
    sig = {k: v["signature"] for k, v in contracts["tables"].items()}
    els = []
    p = review_dir / "sa" / "02-entities-relations.md"
    if p.exists():
        for t in M.parse(p.name, p.read_text(encoding="utf-8")).tables:
            if M.classify(t, sig) == "sa_entities": els += [r["英文"] for r in t.rows if r.get("英文")]
    p = review_dir / "sa" / "03-roles.md"
    if p.exists():
        for t in M.parse(p.name, p.read_text(encoding="utf-8")).tables:
            if M.classify(t, sig) == "sa_roles":
                for r in t.rows:
                    m = re.match(r"\s*([A-Z][A-Za-z0-9]+)", r.get("動作", ""))   # 動作欄開頭的 PascalCase 詞(括號內的 HTTP 路徑不算)
                    if m and m.group(1).upper() not in STOP: els.append(m.group(1))
    seen, out = set(), []
    for e in els:
        if e not in seen: seen.add(e); out.append(e)
    return out

def candidates_md(hits: dict) -> str:
    lines = ["# Survey 候選(由 analyze.survey 產生,不手改;定案寫 survey-mapping.md)", "", "| 模型元素 | 候選檔案 | 行 | 片段 |", "|---|---|---|---|"]
    for el, found in hits.items():
        if not found: lines.append(f"| {el} | (無) | | |")
        for path, n, snip in found: lines.append(f"| {el} | {path} | {n} | `{snip.replace('|', '¦')}` |")
    return "\n".join(lines) + "\n"

def run(ctx: dict) -> dict:
    review, root = ctx["review_dir"], ctx["project_root"]
    els = elements_from_sa(review, ctx["contracts"], ctx.get("data") or {})
    hits = scan(root, ctx["config"], els)
    (review / "survey-candidates.md").write_text(candidates_md(hits), encoding="utf-8")
    ctx["survey_candidates"] = hits
    return ctx
