"""review.versions v1:文件版本追蹤。每次 review / serve 重建時替所有輸入與產出的文件留指紋,有變才記一版。

追蹤什麼:PM spec、mock、參考文件、SA 各步驟 md、RD spec md(含 ui/ api/)、survey、名詞表與命名對照。
指紋三層:文件 hash → 每個標題段落 hash → 每條需求的「上游鍵」:
  pm:<REQ>  該需求來源錨點對應的 PM 段落文字
  req:<REQ> 需求列(標題、來源)+ 它的 AC 文字
上游鍵讓審計能判斷「圖本身沒改,但它依據的需求改了」→ 已通過的確認事項變成「上游已變,請重看」。

存放(不靠 git,也可攜):
  review_dir/audit/versions.jsonl          一版一行:{v, at, git, docs:{path:{hash,lines,kind,sections}}, keys:{key:hash}}
  review_dir/audit/versions/blobs/<hash>.txt  內容定址的文件內容,做 diff 用(只存變過的)
有 git 時另外記 commit 與每份文件最後一次 commit(顯示用,不影響判定)。"""
import datetime, difflib, hashlib, json, pathlib, re, subprocess

KEEP_VERSIONS = 30          # 看板只放最近 30 版的時間軸與 diff
MAX_DIFF_LINES = 400
GENERATED = {"90-traceability.md", "boundary-report.md", "survey-candidates.md", "signoff.md", "threads.md"}

def _h(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()[:12]

def sections(text: str) -> dict:
    """標題 → 段落 hash(含標題下到下一個同級或更高標題前的文字)。同名標題加序號。"""
    out, cur, buf, seen = {}, "(開頭)", [], {}
    def flush():
        if buf or cur != "(開頭)": out[cur] = _h("\n".join(buf).strip())
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if m:
            flush(); name = m.group(2); seen[name] = seen.get(name, 0) + 1
            cur = name if seen[name] == 1 else f"{name} ({seen[name]})"; buf = []
        else: buf.append(line)
    flush()
    return out

def tracked(ctx: dict) -> list:
    """(顯示路徑, 實際路徑, 種類)。顯示路徑一律相對專案根(看得懂、可點開原文)。"""
    data, root = ctx["data"], pathlib.Path(ctx["project_root"]).resolve()
    spec, review = pathlib.Path(ctx["dir"]).resolve(), pathlib.Path(ctx["review_dir"]).resolve()
    out, seen = [], set()
    def add(p: pathlib.Path, kind: str):
        p = p.resolve()
        if p in seen or not p.is_file() or p.name in GENERATED: return
        seen.add(p); rel = str(p.relative_to(root)) if p.is_relative_to(root) else str(p)
        out.append((rel, p, kind))
    src = data.get("sources") or {}
    if (src.get("pm_spec") or {}).get("path"): add(root / src["pm_spec"]["path"], "PM")
    for m in src.get("mocks") or []: add(root / m["path"], "PM")
    for r in src.get("refs") or []:
        if r.get("exists"): add(root / r["path"], "參考")
    for f in data.get("sa_files") or []: add(review / f, "SA")
    for p in sorted(spec.rglob("*.md")):
        if "html" not in p.relative_to(spec).parts: add(p, "RD")
    g = data.get("glossary") or {}
    for k in ("path", "naming_path", "overrides_path"):
        if g.get(k): add(root / g[k] if not pathlib.Path(g[k]).is_absolute() else pathlib.Path(g[k]), "名詞")
    return out

def upstream_keys(data: dict) -> dict:
    secs = ((data.get("sources") or {}).get("pm_spec") or {}).get("sections") or []
    def pm_text(src):
        key = str(src or "").strip()
        s = next((x for x in secs if x["anchor"] == key), None) or next((x for x in secs if key.startswith(x["anchor"] + " ") or key.startswith(x["anchor"] + "(")), None) \
            or next((x for x in secs if key.startswith(x["anchor"])), None)
        return (s["title"] + "\n" + s["text"]) if s else ""
    out, act = {}, data.get("ac_text") or {}
    for r in data.get("requirements") or []:
        t = pm_text(r.get("source"))
        if t: out[f"pm:{r['id']}"] = _h(t)
        out[f"req:{r['id']}"] = _h("\n".join([r.get("title", ""), str(r.get("source", "")), *[(act.get(a) or {}).get("text", a) for a in r.get("acs") or []]]))
    return out

def _git(args, cwd):
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=10)
        return r.stdout.strip() if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError): return None

def git_info(root: pathlib.Path, docs: list) -> dict:
    head = _git(["rev-parse", "--short", "HEAD"], root)
    if not head: return {}
    info = {"commit": head, "branch": _git(["rev-parse", "--abbrev-ref", "HEAD"], root) or "", "docs": {}}
    dirty = _git(["status", "--porcelain", "--", *[str(p) for _, p, _ in docs]], root) or ""
    info["dirty"] = sorted({l[3:].strip() for l in dirty.splitlines() if l.strip()})
    for rel, p, _ in docs:
        last = _git(["log", "-1", "--format=%h|%cs|%an|%s", "--", str(p)], root)
        if last: c, d, a, s = (last.split("|", 3) + ["", "", "", ""])[:4]; info["docs"][rel] = {"commit": c, "date": d, "author": a, "subject": s[:80]}
    return info

def load(path: pathlib.Path) -> list:
    if not path.exists(): return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]

def _diff(old: str, new: str, a: str, b: str) -> dict:
    lines = list(difflib.unified_diff(old.splitlines(), new.splitlines(), a, b, lineterm="", n=2))
    add = sum(1 for l in lines if l.startswith("+") and not l.startswith("+++")); rem = sum(1 for l in lines if l.startswith("-") and not l.startswith("---"))
    return {"add": add, "del": rem, "lines": lines[:MAX_DIFF_LINES], "truncated": len(lines) > MAX_DIFF_LINES}

def snapshot(ctx: dict) -> dict:
    review = pathlib.Path(ctx["review_dir"]); vdir = review / "audit"; blobs = vdir / "versions" / "blobs"
    blobs.mkdir(parents=True, exist_ok=True)
    docs = tracked(ctx)
    cur_docs = {}
    for rel, p, kind in docs:
        text = p.read_text(encoding="utf-8", errors="replace")
        hsh = _h(text); cur_docs[rel] = {"hash": hsh, "lines": text.count("\n") + 1, "kind": kind, "sections": sections(text) if p.suffix == ".md" else {}}
        b = blobs / f"{hsh}.txt"
        if not b.exists(): b.write_text(text, encoding="utf-8")
    keys = upstream_keys(ctx["data"])
    hist_path = vdir / "versions.jsonl"; hist = load(hist_path)
    last = hist[-1] if hist else None
    if not last or {k: v["hash"] for k, v in last["docs"].items()} != {k: v["hash"] for k, v in cur_docs.items()} or last.get("keys") != keys:
        rec = {"v": (last["v"] + 1) if last else 1, "at": datetime.datetime.now().isoformat(timespec="seconds"), "docs": cur_docs, "keys": keys}
        g = git_info(pathlib.Path(ctx["project_root"]).resolve(), docs)
        if g: rec["git"] = {"commit": g["commit"], "branch": g["branch"], "dirty": g["dirty"]}
        with hist_path.open("a", encoding="utf-8") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        hist.append(rec)
    return summarize(hist, blobs, git_info(pathlib.Path(ctx["project_root"]).resolve(), docs) if hist else {})

def summarize(hist: list, blobs: pathlib.Path, git: dict) -> dict:
    """看板用:時間軸(每版變了哪些文件 / 段落 / 上游鍵)、文件清單、diff、上游鍵變更紀錄。"""
    read = lambda h: (blobs / f"{h}.txt").read_text(encoding="utf-8") if h and (blobs / f"{h}.txt").exists() else ""
    timeline, diffs, key_changes = [], {}, {}
    for i, rec in enumerate(hist):
        prev = hist[i - 1] if i else None
        changed = []
        for path, d in rec["docs"].items():
            p = (prev or {}).get("docs", {}).get(path)
            if p and p["hash"] == d["hash"]: continue
            secs = sorted(s for s, h in d["sections"].items() if not p or p["sections"].get(s) != h)
            entry = {"path": path, "kind": d["kind"], "status": "new" if not p else "changed", "sections": secs[:20], "more": max(0, len(secs) - 20)}
            if rec["v"] > hist[-1]["v"] - KEEP_VERSIONS and p:
                df = _diff(read(p["hash"]), read(d["hash"]), f"{path} @v{prev['v']}", f"{path} @v{rec['v']}")
                entry.update(add=df["add"], dele=df["del"]); diffs[f"{rec['v']}:{path}"] = df
            changed.append(entry)
        for path in (prev or {}).get("docs", {}):
            if path not in rec["docs"]: changed.append({"path": path, "kind": prev["docs"][path]["kind"], "status": "removed", "sections": []})
        kch = sorted(k for k, h in (rec.get("keys") or {}).items() if prev and (prev.get("keys") or {}).get(k) != h)
        for k in kch: key_changes.setdefault(k, []).append(rec["v"])
        timeline.append({"v": rec["v"], "at": rec["at"], "git": rec.get("git"), "changed": changed, "keys": kch})
    latest = hist[-1] if hist else {"v": 0, "docs": {}}
    since = {}
    for t in timeline:
        for c in t["changed"]: since[c["path"]] = t["v"]
    docs = [{"path": p, "kind": d["kind"], "hash": d["hash"], "lines": d["lines"], "changed_in": since.get(p, latest["v"]), "git": (git.get("docs") or {}).get(p)}
            for p, d in latest["docs"].items()]
    return {"current": latest["v"], "at": latest.get("at"), "git": {k: git[k] for k in ("commit", "branch", "dirty") if k in git} if git else None,
            "timeline": timeline[-KEEP_VERSIONS:][::-1], "docs": sorted(docs, key=lambda d: (-d["changed_in"], d["kind"], d["path"])),
            "diffs": diffs, "key_changes": key_changes}

def run(ctx: dict) -> dict:
    res = snapshot(ctx)
    ctx.setdefault("carry", {})["versions"] = res; ctx["data"]["versions"] = res
    return ctx
