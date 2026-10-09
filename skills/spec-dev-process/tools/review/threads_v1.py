"""review.threads v1:PM / QA / RD 共同核對時的提問串。SSOT = spec-review/audit/threads.md(md 表格,一列一則)。
問題掛在某個審計項目(圖 ID / SA 表格列 / REQ / 缺口 GAP-n)上;「給」是希望哪個視角(PM / QA / RD)回答的提示,不是指定人,留空 = 任何人。回答與結案也寫回同一列。"""
import datetime, pathlib
from core import mdtables as M

HEAD = "| # | 項目 | 從 | 給 | 問題 | 回答 | 狀態 | 時間 |"

def _clean(s): return str(s or "").replace("|", "/").replace("\n", " ").strip()

def load(path: pathlib.Path) -> list:
    if not path.exists(): return []
    out = []
    for t in M.parse(path.name, path.read_text(encoding="utf-8")).tables:
        if t.header[:2] != ["#", "項目"]: continue
        for r in t.rows:
            try: n = int(r["#"])
            except ValueError: continue
            out.append({"n": n, "item": r["項目"], "from": r["從"], "to": r["給"], "text": r["問題"], "answer": r.get("回答", ""),
                        "status": (r.get("狀態") or "open").strip(), "at": r.get("時間", "")})
    return out

def save(path: pathlib.Path, rows: list):
    L = ["# 共同核對提問串(PM / QA / RD)", "", "<!-- SSOT:看板(spec-dev.py serve)上的提問與回答都寫在這裡;也可以直接編輯。狀態 = open / closed。 -->", "",
         "## 提問", "", HEAD, "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['n']} | {_clean(r['item'])} | {_clean(r['from'])} | {_clean(r['to'])} | {_clean(r['text'])} | {_clean(r.get('answer'))} | {r['status']} | {r['at']} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L) + "\n", encoding="utf-8")

def ask(path, item, frm, to, text):
    if not text.strip(): raise ValueError("問題不能是空的")
    rows = load(path); n = max([r["n"] for r in rows] or [0]) + 1
    rows.append({"n": n, "item": item, "from": frm, "to": to, "text": text, "answer": "", "status": "open",
                 "at": datetime.datetime.now().isoformat(timespec="minutes")})
    save(path, rows); return n

def answer(path, n, by, text, close=True):
    rows = load(path)
    for r in rows:
        if r["n"] == int(n):
            if text.strip(): r["answer"] = (r["answer"] + " / " if r["answer"] else "") + f"{by}:{text.strip()}"
            if close: r["status"] = "closed"
            save(path, rows); return r
    raise ValueError(f"沒有 Q{n}")
