"""analyze.assets v1:已知資產索引。掃 config.assets.roots(預設 docs/、specs/done/)下的 md,依標題切段,
每段記 path、line、heading、摘錄。面板用它在「轉換證據」旁列出相關的既有文件段落,並提供查找框。工具層建索引,不把全文送進模型。"""
import pathlib, re

def index(project_root: pathlib.Path, cfg: dict) -> list:
    a = cfg.get("assets") or {}
    roots = a.get("roots") or ["docs", "specs/done"]; exts = set(a.get("extensions") or [".md"])
    max_sections = int(a.get("max_sections") or 400); excerpt = int(a.get("excerpt") or 400)
    out = []
    for root in roots:
        base = project_root / root
        if not base.exists(): continue
        for f in sorted(p for p in base.rglob("*") if p.is_file() and p.suffix in exts):
            rel = str(f.relative_to(project_root)); lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
            heads = [(i, m.group(2).strip()) for i, l in enumerate(lines) if (m := re.match(r"^(#{1,4})\s+(.*)", l))] or [(0, f.stem)]
            if heads[0][0] != 0: heads.insert(0, (0, f.stem))
            for k, (i, h) in enumerate(heads):
                end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
                body = "\n".join(lines[i + (1 if lines and re.match(r"^#", lines[i]) else 0):end]).strip()
                if not body and k + 1 < len(heads): continue
                out.append({"path": rel, "line": i + 1, "heading": h, "text": body[:excerpt], "root": root})
                if len(out) >= max_sections: return out
    return out

def run(ctx: dict) -> dict:
    ctx.setdefault("carry", {})["assets"] = index(ctx["project_root"], ctx["config"])
    if ctx.get("data") is not None: ctx["data"]["assets"] = ctx["carry"]["assets"]
    return ctx
