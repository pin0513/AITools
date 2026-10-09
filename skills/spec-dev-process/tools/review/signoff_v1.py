"""review.signoff v1:把人的判斷寫進 spec-review/audit/signoff.md(SSOT)。
核准時必須給「看到的那個 hash」,且要等於目前內容 hash,否則拒絕(避免簽到你沒看過的版本)。"""
import datetime, json, pathlib
from tools.review.audit_v1 import load_signoff, SIGNOFF_HEAD

def apply(review_dir: pathlib.Path, diagram: str, by: str, decision: str, seen_hash: str = "", note: str = "") -> str:
    au = review_dir / "audit" / "audit.json"
    if not au.exists(): raise SystemExit("找不到 audit/audit.json,請先跑 spec-dev.py review")
    items = {i["id"]: i for i in json.loads(au.read_text(encoding="utf-8"))["items"] if i["type"] == "diagram"}
    if diagram not in items: raise SystemExit(f"{diagram} 不在審計清單(可用:{', '.join(sorted(items))[:300]}…)")
    cur = items[diagram]["hash"]
    if decision == "approved" and seen_hash != cur:
        raise SystemExit(f"拒絕核准:你看到的 hash {seen_hash or '(未提供)'} ≠ 目前內容 {cur}。圖已變動,請回看板重新確認。")
    if decision == "rejected" and not note: raise SystemExit("退回必須附 --note,寫要怎麼改")
    path = review_dir / "audit" / "signoff.md"; text = path.read_text(encoding="utf-8").splitlines()
    today = datetime.date.today().isoformat(); done = False
    for i, line in enumerate(text):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and cells and cells[0] == diagram:
            cells[3] = cur if decision == "approved" else cells[3]; cells[4] = cur; cells[5] = decision; cells[6] = by; cells[7] = today; cells[8] = note.replace("|", "/")
            text[i] = "| " + " | ".join(cells) + " |"; done = True; break
    if not done: raise SystemExit(f"signoff.md 沒有 {diagram} 這一列,請先跑 spec-dev.py review")
    path.write_text("\n".join(text) + "\n", encoding="utf-8")
    return f"{diagram}: {decision} by {by} @ {cur}"
