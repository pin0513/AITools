#!/usr/bin/env python3
"""transform.render v1:rd-spec 目錄下每個 *.md → html/<name>.html。mermaid 預設走 CDN;offline=True 時內嵌 vendor/mermaid.min.js。
只做標題/表格/程式碼區塊/mermaid 的最小轉換,其餘段落原樣輸出。"""
import html, pathlib, re, sys

MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"

def md_to_html(text: str) -> str:
    out, i, lines = [], 0, text.splitlines()
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            lang = line[3:].strip()
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            body = "\n".join(lines[i + 1:j])
            if lang == "mermaid":
                out.append(f'<pre class="mermaid">{html.escape(body)}</pre>')
            else:
                out.append(f'<pre><code class="lang-{html.escape(lang)}">{html.escape(body)}</code></pre>')
            i = j + 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i]); i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            if len(cells) >= 2 and all(re.fullmatch(r":?-+:?", c) for c in cells[1]):
                head, body = cells[0], cells[2:]
            else:
                head, body = None, cells
            t = ["<table>"]
            if head:
                t.append("<tr>" + "".join(f"<th>{html.escape(c)}</th>" for c in head) + "</tr>")
            for r in body:
                t.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>")
            t.append("</table>")
            out.append("\n".join(t))
            continue
        m = re.match(r"^(#{1,3})\s+(.*)", line)
        if m:
            out.append(f"<h{len(m.group(1))}>{html.escape(m.group(2))}</h{len(m.group(1))}>")
        elif line.startswith("- "):
            out.append(f"<li>{html.escape(line[2:])}</li>")
        elif line.strip():
            out.append(f"<p>{html.escape(line)}</p>")
        i += 1
    return "\n".join(out)

PAGE = """<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>body{{font:15px/1.6 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 16px;color:#1f2328;background:#fff}}
table{{border-collapse:collapse;margin:1rem 0}}th,td{{border:1px solid #d0d7de;padding:4px 10px;text-align:left}}
th{{background:#f6f8fa}}pre{{background:#f6f8fa;padding:12px;overflow:auto}}pre.mermaid{{background:#fff}}
@media (prefers-color-scheme:dark){{body{{background:#0d1117;color:#e6edf3}}th{{background:#161b22}}pre{{background:#161b22}}pre.mermaid{{background:#0d1117}}th,td{{border-color:#30363d}}}}
</style></head><body>{body}
<script src="{cdn}"></script><script>mermaid.initialize({{startOnLoad:true,theme:matchMedia('(prefers-color-scheme:dark)').matches?'dark':'default'}});</script>
</body></html>"""

def script_tag(offline_js: "pathlib.Path|None") -> str:
    if offline_js:
        lib = offline_js.read_text(encoding="utf-8").replace("</script>", "<\\/script>")
        return f"<script>{lib}</script>"
    return f'<script src="{MERMAID_CDN}"></script>'

def render_dir(d: pathlib.Path, offline_js=None, review_dir: pathlib.Path = None) -> list:
    outdir = (review_dir or d) / "html"; outdir.mkdir(exist_ok=True)
    tag = script_tag(offline_js); done = []
    sources = sorted(d.glob("*.md")) + sorted(d.glob("ui/*.md")) + sorted(d.glob("api/*.md"))
    if review_dir and review_dir != d:
        sources += sorted(review_dir.glob("*.md")) + sorted((review_dir / "sa").glob("*.md"))
    for md in sources:
        body = md_to_html(md.read_text(encoding="utf-8"))
        page = PAGE.format(title=md.stem, body=body, cdn="__MERMAID__").replace('<script src="__MERMAID__"></script>', tag)
        name = (md.parent.name + "-" if md.parent.name in ("sa", "ui", "api") else "") + md.stem + ".html"
        (outdir / name).write_text(page, encoding="utf-8")
        done.append(md.name)
    return done


def run(ctx: dict) -> dict:
    from core import config as C
    ctx["rendered"] = render_dir(ctx["dir"], C.PATHS["vendor_mermaid"] if ctx.get("offline") else None, ctx.get("review_dir"))
    return ctx
