"""transform.panel v1:traceability + log + boundary + gate + kpis → check-panel.html(模板:process/templates/check-panel.html)。"""
import json, pathlib
from core import config as C

TEMPLATE = C.PATHS["templates"] / "check-panel.html"
CDN_TAG = '<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>'

MAX_FILE = 200_000; MAX_TOTAL = 3_000_000; SNIP = 6

def embedded_sources(ctx: dict) -> dict:
    """靜態面板也能點「檔:行」看原文:追蹤的文件(PM / SA / RD / 名詞表)嵌全文,survey 證據指到的程式碼只嵌前後幾行。
    鍵一律是相對專案根的路徑;看板端用「完全相同 → 結尾相同 → 2 位數簡寫」找。"""
    import re
    root = pathlib.Path(ctx["project_root"]).resolve(); data = ctx.get("data") or {}
    files, snips, total = {}, {}, 0
    for d in ((data.get("versions") or {}).get("docs") or []):
        p = (root / d["path"]).resolve()
        if not p.is_file() or not p.is_relative_to(root) or p.stat().st_size > MAX_FILE: continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if total + len(text) > MAX_TOTAL: break
        files[d["path"]] = text; total += len(text)
    for row in data.get("survey") or []:
        for one in str(row.get("evidence") or "").split(";"):
            m = re.match(r'^\s*(.+?):(\d+)', one)
            if not m: continue
            p = (root / m.group(1)).resolve(); n = int(m.group(2))
            if m.group(1) in files or not p.is_file() or not p.is_relative_to(root): continue
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            s = max(1, n - SNIP); snips[f"{m.group(1)}:{n}"] = {"path": m.group(1), "start": s, "lines": lines[s - 1:n + SNIP]}
    return {"files": files, "snippets": snips}

def build(d: pathlib.Path, tr: dict, log: list, boundary: list, g: list, k: dict, offline_js=None, template=TEMPLATE, board=None, sources=None) -> pathlib.Path:
    payload = {"trace": tr, "log": log, "boundary": boundary, "gate": g, "kpis": k, "board": board or {}, "src": sources or {}}
    html = template.read_text(encoding="utf-8").replace("/*__DATA__*/null", json.dumps(payload, ensure_ascii=False))
    if offline_js:
        lib = pathlib.Path(offline_js).read_text(encoding="utf-8").replace("</script>", "<\\/script>")
        html = html.replace(CDN_TAG, "<script>" + lib + "</script>")
    out = d / "check-panel.html"
    out.write_text(html, encoding="utf-8")
    return out

def run(ctx: dict) -> dict:
    from tools.check.engine_v1 import run_gate
    run_gate(ctx)
    build(ctx.get("review_dir") or ctx["dir"], ctx["data"], ctx["log"], ctx.get("boundary") or [], ctx.get("gate") or [], ctx["kpis"],
          C.PATHS["vendor_mermaid"] if ctx.get("offline") else None, board=(ctx.get("config") or {}).get("board"), sources=embedded_sources(ctx))
    return ctx
