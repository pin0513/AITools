"""transform.panel v1:traceability + log + boundary + gate + kpis → check-panel.html(模板:process/templates/check-panel.html)。"""
import json, pathlib
from core import config as C

TEMPLATE = C.PATHS["templates"] / "check-panel.html"
CDN_TAG = '<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/11.4.1/mermaid.min.js"></script>'

def build(d: pathlib.Path, tr: dict, log: list, boundary: list, g: list, k: dict, offline_js=None, template=TEMPLATE) -> pathlib.Path:
    payload = {"trace": tr, "log": log, "boundary": boundary, "gate": g, "kpis": k}
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
    build(ctx["dir"], ctx["data"], ctx["log"], ctx.get("boundary") or [], ctx.get("gate") or [], ctx["kpis"],
          C.PATHS["vendor_mermaid"] if ctx.get("offline") else None)
    return ctx
