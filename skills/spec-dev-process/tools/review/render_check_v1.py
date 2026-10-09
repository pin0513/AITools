"""review.render_check v1:用瀏覽器驗證看板。逐張圖(含收合的)解析、JS 錯誤、每條需求一張卡、預設的圖都畫出、窄螢幕不溢出。
需要 node + playwright(+ chromium);沒有時依 config reviewer.render_check 決定:auto → 標「未驗證」(WARN)、off → 不檢查、on → FAIL。"""
import json, os, pathlib, shutil, subprocess
from core import config as C

HERE = pathlib.Path(__file__).resolve().parent

def available():
    if not shutil.which("node"): return False, "沒有 node"
    root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip() if shutil.which("npm") else ""
    ok = subprocess.run(["node", "-e", "require('playwright')"], capture_output=True, env={**os.environ, "NODE_PATH": root}).returncode == 0
    return (ok, root) if ok else (False, "沒有 playwright")

def run(ctx: dict) -> dict:
    mode = str(((ctx["config"].get("reviewer") or {}).get("render_check")) or "auto")
    panel = (ctx.get("review_dir") or ctx["dir"]) / "check-panel.html"
    res = {"mode": mode, "available": False, "reason": "", "parse": {}}
    if mode != "off":
        ok, root = available()
        if not ok: res["reason"] = root
        elif not panel.exists(): res["reason"] = "沒有 check-panel.html"
        else:
            r = subprocess.run(["node", str(HERE / "browser" / "verify.js"), str(C.PATHS["vendor_mermaid"]), str(panel.resolve()), "400"],
                               capture_output=True, text=True, env={**os.environ, "NODE_PATH": root}, timeout=180)
            try: res.update(json.loads(r.stdout.strip().splitlines()[-1])); res["available"] = True
            except Exception: res["reason"] = (r.stderr or r.stdout)[-300:]
    res["reqs"] = len(ctx["data"]["requirements"])
    ctx.setdefault("carry", {})["render_check"] = res; ctx["data"]["render_check"] = res
    au = ctx["data"].get("audit")
    if au:
        for it in au["items"]:
            if it["type"] == "diagram": it["render"] = res["parse"].get(it["id"], "未驗證" if not res["available"] else "未出現在看板")
        au["render_check"] = {k: v for k, v in res.items() if k != "parse"}
        aj = (ctx.get("review_dir") or ctx["dir"]) / "audit" / "audit.json"
        if aj.exists(): aj.write_text(json.dumps(au, ensure_ascii=False, indent=1), encoding="utf-8")
    return ctx
