"""review.signoff v1:把人的判斷寫進 spec-review/audit/signoff.md(SSOT),一張圖 × 一個確認事項一列。
以事情區分、不以人區分:同一個人可以把一張圖的多個確認事項一起做完。
通過時必須給「看到的那個 hash」,且要等於目前內容 hash,否則拒絕(避免簽到你沒看過的版本);
確認事項必須是這張圖要做的(rules/review/duties.yaml);退回要寫怎麼改,「不需要」要寫理由。"""
import datetime, json, pathlib

class Refused(ValueError):
    """拒絕寫入(伺服器回 200 + error,CLI 印出後退出碼 1)。"""

def apply(review_dir: pathlib.Path, diagram: str, by: str, decision: str, seen_hash: str = "", note: str = "", duty: str = "buildable") -> str:
    au = review_dir / "audit" / "audit.json"
    if not au.exists(): raise Refused("找不到 audit/audit.json,請先跑 spec-dev.py review")
    audit = json.loads(au.read_text(encoding="utf-8")); ver = audit.get("version") or 0
    items = {i["id"]: i for i in audit["items"] if i["type"] == "diagram"}
    if diagram not in items: raise Refused(f"{diagram} 不在審計清單")
    it = items[diagram]; cur = it["hash"]
    if duty not in it.get("duties", []): raise Refused(f"{diagram} 沒有「{duty}」這個確認事項(要做:{', '.join(it.get('duties') or [])})")
    if decision not in ("approved", "rejected", "n/a", "pending"): raise Refused("決定只能是 approved / rejected / n/a / pending")
    if not by.strip(): raise Refused("要寫審核者名字")
    if decision == "approved" and seen_hash != cur:
        raise Refused(f"拒絕核准:你看到的 hash {seen_hash or '(未提供)'} ≠ 目前內容 {cur}。圖已變動,請重新確認。")
    if decision == "rejected" and not note.strip(): raise Refused("退回必須附備註,寫要怎麼改")
    if decision == "n/a" and not note.strip(): raise Refused("標「不需要」必須寫理由")
    path = review_dir / "audit" / "signoff.md"; text = path.read_text(encoding="utf-8").splitlines()
    today = datetime.date.today().isoformat()
    for i, line in enumerate(text):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) >= 10 and cells[0] == diagram and cells[1] == duty:
            if len(cells) < 11: cells.append("")
            cells[10] = f"v{ver}" if ver and decision != "pending" else ""   # 確認當時的文件版本
            cells[4] = cur if decision == "approved" else ("" if decision == "pending" else cells[4]); cells[5] = cur
            cells[6] = decision; cells[7] = by.replace("|", "/"); cells[8] = today; cells[9] = note.replace("|", "/").replace("\n", " ")
            text[i] = "| " + " | ".join(cells) + " |"
            path.write_text("\n".join(text) + "\n", encoding="utf-8")
            return f"{diagram}「{duty}」: {decision} by {by} @ {cur}" + (f" (v{ver})" if ver else "")
    raise Refused(f"signoff.md 沒有 {diagram} / {duty} 這一列,請先跑 spec-dev.py review")
