"""analyze.lexicon v1(SA0 前置解析,工具層):PM spec + mock + refs 的中/英文斷詞 → 名詞 / 動作 / 角色 / 狀態值候選,
詞頻 × 章節權重 = 重要性;對專案詞彙表與 codebase 做 glossary-mapping;給升/降級建議。
產出 review_dir/sa/00-lexicon.md(產生物)與 lexicon.json(給 LLM 做 SA1 用,取代整份原文)。零相依:CJK 用 n-gram + 詞典。"""
import json, pathlib, re
from collections import Counter, defaultdict
from core import config as C, yamlmini

CJK = re.compile(r"[一-鿿]+")
EN = re.compile(r"[A-Za-z][A-Za-z0-9_]{2,}")

def load_lexicon(cfg: dict) -> dict:
    lex = yamlmini.load(C.PATHS["rules_dir"] / "methodology" / "sa" / "lexicon-zh.yaml")
    ext = cfg.get("lexicon") or {}
    for k in ("verbs", "role_suffixes", "stop_chars", "stop_words", "en_ignore"):
        lex[k] = list(lex.get(k) or []) + list(ext.get("extra_" + k) or [])
    for k in ("ngram", "min_freq", "promote_top_ratio", "section_weights", "doc_weights", "split_chars"):
        if k in ext: lex[k] = ext[k]
    return lex

def _sections(text: str, weights: dict):
    """每段文字配章節權重:標題含關鍵字者乘權重,其餘 1。回傳 [(weight, text, heading)]"""
    out, cur_w, cur_h, buf = [], 1, "", []
    for line in text.splitlines():
        m = re.match(r"^#{1,6}\s+(.*)", line)
        if m:
            if buf: out.append((cur_w, "\n".join(buf), cur_h)); buf = []
            cur_h = m.group(1); cur_w = max([w for k, w in weights.items() if k in cur_h] or [1])
        else:
            buf.append(line)
    if buf: out.append((cur_w, "\n".join(buf), cur_h))
    return out

def _clean(text: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)            # mock html 標籤
    text = re.sub(r"`[^`]*`", " ", text)
    return text

def _split_runs(run: str, split_chars: set, status_prefixes: tuple):
    """在 split_chars 切開;但 已/未/待 若接在詞首(狀態值)則保留在詞內。"""
    out, cur = [], ""
    for i, ch in enumerate(run):
        if ch in split_chars and not (ch in status_prefixes and (i == 0 or run[i - 1] in split_chars)):
            if cur: out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur: out.append(cur)
    return out

def cjk_neighbors(text: str, lex: dict, grams: set) -> dict:
    """每個 gram 的左右鄰字集合(同一切分單位內)。"""
    split_c = set(lex.get("split_chars") or []); st_pre = tuple(lex.get("status_prefixes") or [])
    nb = defaultdict(lambda: [set(), set()])
    for big in CJK.findall(text):
        for run in _split_runs(big, split_c, st_pre):
            for g in grams:
                start = run.find(g)
                while start != -1:
                    nb[g][0].add(run[start - 1] if start > 0 else "^")
                    end = start + len(g); nb[g][1].add(run[end] if end < len(run) else "$")
                    start = run.find(g, start + 1)
    return nb

def cjk_candidates(text: str, lex: dict) -> Counter:
    lo, hi = lex["ngram"]; stop_c = set(lex["stop_chars"]); stop_w = set(lex["stop_words"]); cnt = Counter()
    split_c = set(lex.get("split_chars") or []); st_pre = tuple(lex.get("status_prefixes") or [])
    for big in CJK.findall(text):
      for run in _split_runs(big, split_c, st_pre):
        for n in range(lo, hi + 1):
            for i in range(len(run) - n + 1):
                g = run[i:i + n]
                if g[0] in stop_c or g[-1] in stop_c or g in stop_w: continue
                cnt[g] += 1
    return cnt

def analyze(docs: list, lex: dict, glossary_terms: dict) -> dict:
    """docs: [(label, text)]。回傳 {nouns, actions, roles, statuses, english, stats}"""
    weights = lex.get("section_weights") or {}; dw = lex.get("doc_weights") or {}
    freq, weight, where, pm_freq = Counter(), Counter(), defaultdict(set), Counter()
    for label, text in docs:
        kind = label.split(":")[0]; dwt = float(dw.get(kind, 1.0))
        for w, chunk, heading in _sections(_clean(text), weights):
            c = cjk_candidates(chunk, lex)
            for g, n in c.items():
                freq[g] += n; weight[g] += n * w * dwt; where[g].add(f"{label}§{heading[:12]}" if heading else label)
                if kind != "ref": pm_freq[g] += n
            for tok in EN.findall(chunk):
                if tok.upper() in set(lex["en_ignore"]) or tok.islower() and len(tok) < 4: continue
                key = "en:" + tok; freq[key] += 1; weight[key] += w * dwt; where[key].add(label)
    # 邊界熵:左鄰字唯一(非句首)且「鄰字+詞」同頻 → 是更長詞的碎片;右鄰同理
    grams = [g for g in freq if not g.startswith("en:")]
    if lex.get("boundary_filter", True):
        nb = defaultdict(lambda: [set(), set()])
        for label, text in docs:
            for g, (l, r) in cjk_neighbors(_clean(text), lex, set(grams)).items():
                nb[g][0] |= l; nb[g][1] |= r
        frag = set()
        for g in grams:
            l, r = nb[g]
            if len(l) == 1 and "^" not in l and freq.get(next(iter(l)) + g, 0) >= freq[g]: frag.add(g)
            if len(r) == 1 and "$" not in r and freq.get(g + next(iter(r)), 0) >= freq[g]: frag.add(g)
        grams = [g for g in grams if g not in frag]
    # 去冗:短詞若只出現在某個更長且詞頻 ≥ 它的詞裡 → 丟
    keep = set()
    by_len = sorted(grams, key=len, reverse=True)
    for g in by_len:
        if any(g != G and g in G and freq[G] >= freq[g] for G in keep): continue
        keep.add(g)
    verbs, suffixes, st_pre = lex["verbs"], tuple(lex["role_suffixes"]), tuple(lex["status_prefixes"])
    is_action = lambda g: g in verbs or any(g.endswith(v) for v in verbs if len(v) >= 2)   # 整詞是動詞或以動詞結尾;動詞+名詞複合詞(審核紀錄)是名詞
    in_dict = is_action
    rows = {"nouns": [], "actions": [], "roles": [], "statuses": [], "english": []}
    for g in keep:
        f, w = freq[g], weight[g]
        known = g in glossary_terms or in_dict(g) or g.endswith(suffixes)
        if f < lex["min_freq"] and not known: continue
        item = {"term": g, "freq": f, "weight": round(w, 1), "pm_freq": pm_freq[g], "where": sorted(where[g])[:4]}
        if g.startswith(st_pre) and len(g) >= 3 and is_action(g[1:]): rows["statuses"].append(item)      # 待審核、已核准、可修改
        elif g.endswith(suffixes): rows["roles"].append(item)
        elif in_dict(g): rows["actions"].append(item)
        else:
            gl = glossary_terms.get(g) or {}
            item["symbol"] = gl.get("symbol", ""); item["glossary_specs"] = gl.get("specs", [])
            rows["nouns"].append(item)
    # 角色片語:「提醒審核者」「表單審核者」= 前綴 + 已存在且更高頻的角色 → 不是新角色
    role_terms = {it["term"]: it["freq"] for it in rows["roles"]}
    rows["roles"] = [it for it in rows["roles"] if not any(it["term"] != r and it["term"].endswith(r) and f > it["freq"] for r, f in role_terms.items())]
    for key in [k for k in freq if k.startswith("en:")]:
        rows["english"].append({"term": key[3:], "freq": freq[key], "weight": weight[key], "where": sorted(where[key])[:4]})
    for k in rows: rows[k].sort(key=lambda x: (-x["weight"], -x["freq"], x["term"]))
    # 升降級:權重前 N% 或有符號 → 升
    for k in ("nouns", "actions", "roles"):
        n = len(rows[k]); top = max(1, int(n * lex.get("promote_top_ratio", 0.6)))
        for i, it in enumerate(rows[k]):
            only_ref = it["pm_freq"] == 0
            it["suggest"] = "升" if (it.get("symbol") or (i < top and it["freq"] >= lex["min_freq"] and not only_ref)) else "降"
    rows["stats"] = {"docs": [d[0] for d in docs], "cjk_candidates": sum(1 for g in freq if not g.startswith("en:")), "after_boundary": len(grams), "kept": len(keep)}
    return rows

def map_codebase(rows: dict, ctx: dict) -> None:
    """名詞候選有符號者 → 掃 codebase 命中數(工具層,不進模型)。"""
    from tools.analyze.survey_v1 import scan
    syms = [it["symbol"] for it in rows["nouns"] if it.get("symbol")] + [it["term"] for it in rows["english"][:30]]
    hits = scan(ctx["project_root"], ctx["config"], syms) if syms else {}
    for it in rows["nouns"]:
        it["code_hits"] = len(hits.get(it.get("symbol") or "", [])) if it.get("symbol") else None
        it["code_first"] = (lambda h: f"{h[0][0]}:{h[0][1]}" if h else "")(hits.get(it.get("symbol") or "", []))
    for it in rows["english"]:
        h = hits.get(it["term"], []); it["code_hits"] = len(h); it["code_first"] = f"{h[0][0]}:{h[0][1]}" if h else ""

def lexicon_md(spec: str, rows: dict) -> str:
    L = [f"# {spec} SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)", "",
         f"來源:{', '.join(rows['stats']['docs'])} · CJK 候選 {rows['stats']['cjk_candidates']} → 邊界熵後 {rows['stats'].get('after_boundary', '?')} → 去冗後 {rows['stats']['kept']}", "",
         "規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。", "",
         "## 名詞候選", "", "| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |", "|---|---|---|---|---|---|---|"]
    for it in rows["nouns"]:
        hits = "—" if it.get("code_hits") is None else (f"{it['code_hits']} ({it['code_first']})" if it["code_hits"] else "0")
        L.append(f"| {it['term']} | {it['freq']} | {it['weight']} | {it.get('symbol','')} | {hits} | {it['suggest']} | {' '.join(it['where'])} |")
    L += ["", "## 動作候選", "", "| 詞 | 詞頻 | 權重 | 建議 | 出現 |", "|---|---|---|---|---|"]
    L += [f"| {it['term']} | {it['freq']} | {it['weight']} | {it['suggest']} | {' '.join(it['where'])} |" for it in rows["actions"]]
    L += ["", "## 角色候選", "", "| 詞 | 詞頻 | 權重 | 建議 | 出現 |", "|---|---|---|---|---|"]
    L += [f"| {it['term']} | {it['freq']} | {it['weight']} | {it['suggest']} | {' '.join(it['where'])} |" for it in rows["roles"]]
    L += ["", "## 狀態值候選(屬性,不建實體)", "", "| 詞 | 詞頻 | 出現 |", "|---|---|---|"]
    L += [f"| {it['term']} | {it['freq']} | {' '.join(it['where'])} |" for it in rows["statuses"]]
    L += ["", "## 英文符號", "", "| 符號 | 詞頻 | codebase 命中 | 出現 |", "|---|---|---|---|"]
    L += [f"| {it['term']} | {it['freq']} | {it.get('code_hits', 0)}{(' (' + it['code_first'] + ')') if it.get('code_first') else ''} | {' '.join(it['where'])} |" for it in rows["english"][:40]]
    return "\n".join(L) + "\n"

def run(ctx: dict) -> dict:
    cfg, root, review = ctx["config"], ctx["project_root"], ctx["review_dir"]
    lex = load_lexicon(cfg)
    src = (ctx.get("data") or {}).get("sources") or {}
    docs = []
    for key, items in (("pm_spec", [src.get("pm_spec")] if src.get("pm_spec") else []), ("mock", src.get("mocks") or []), ("ref", src.get("refs") or [])):
        for it in items:
            fp = root / it["path"]
            if fp.exists() and fp.suffix.lower() in (".md", ".html", ".htm", ".txt"):
                docs.append((f"{key}:{fp.name}", fp.read_text(encoding="utf-8", errors="ignore")))
    glossary_terms = (ctx.get("glossary") or {}).get("terms") or {}
    if not glossary_terms:
        from tools.analyze.glossary_v1 import collect
        glossary_terms, _ = collect(root, cfg, ctx["contracts"])
    rows = analyze(docs, lex, glossary_terms)
    map_codebase(rows, ctx)
    (review / "sa").mkdir(parents=True, exist_ok=True)
    (review / "sa" / "00-lexicon.md").write_text(lexicon_md(ctx.get("spec_name", ""), rows), encoding="utf-8")
    (review / "lexicon.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    ctx["lexicon"] = rows
    if ctx.get("data") is not None: ctx["data"]["lexicon"] = {k: rows[k][:40] for k in ("nouns", "actions", "roles", "statuses")} | {"stats": rows["stats"]}
    return ctx
