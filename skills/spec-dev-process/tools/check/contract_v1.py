"""契約檢查 v1:llm stage 的產物是否存在、章節齊全、必要表格可辨識、表格必要欄齊全。輸出與 gate 同形:{level, rule, ids, msg}。"""
import json, pathlib
from core import mdtables as M

def check_files(d: pathlib.Path, contracts: dict, files: list, review_dir: pathlib.Path = None) -> list:
    out = []; tables = contracts["tables"]; sig = {k: v["signature"] for k, v in tables.items()}
    for fname in files:
        fname = fname.split("#")[0]
        spec = contracts["files"].get(fname)
        if not spec: continue
        base = (review_dir or d) if spec.get("dir") == "review" else d
        p = next((base / rel for rel in (spec.get("paths") or [fname]) if (base / rel).exists()), base / (spec.get("paths") or [fname])[0])
        rule = f"C-{spec.get('stage', '?')}"
        if not p.exists():
            if spec.get("when_missing") == "ignore": continue
            out.append({"level": "FAIL" if spec.get("required") else "WARN", "rule": rule, "ids": [fname], "msg": f"缺檔 {fname}"}); continue
        if fname.endswith(".jsonl"):
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip(): continue
                try: e = json.loads(line)
                except json.JSONDecodeError: out.append({"level": "FAIL", "rule": rule, "ids": [fname], "msg": f"{fname} 第 {n} 行不是 JSON"}); continue
                miss = [k for k in spec.get("jsonl_fields", []) if k not in e]
                if miss: out.append({"level": "FAIL", "rule": rule, "ids": [fname], "msg": f"{fname} 第 {n} 行缺欄 {miss}"})
                if "evidence" in e and e["evidence"] not in spec.get("evidence", []): out.append({"level": "FAIL", "rule": rule, "ids": [fname], "msg": f"{fname} 第 {n} 行 evidence='{e['evidence']}' 不在 {spec.get('evidence')}"})
            continue
        doc = M.parse(fname, p.read_text(encoding="utf-8"))
        for sec in spec.get("sections", []):
            if not any(h.startswith(sec) for h in doc.h2):
                out.append({"level": "FAIL" if spec.get("required") else "WARN", "rule": rule, "ids": [fname], "msg": f"{fname} 缺章節 ## {sec}"})
        found = {}
        for t in doc.tables:
            name = M.classify(t, sig)
            if name: found.setdefault(name, t)
        for name in spec.get("required_tables", []):
            if name not in found:
                out.append({"level": "FAIL", "rule": rule, "ids": [fname], "msg": f"{fname} 缺表格 {name}(表頭 {' | '.join(map(str, tables[name]['signature']))} …)"})
        for name, t in found.items():
            miss = [c for c in tables[name]["columns"] if c not in t.header]
            if miss: out.append({"level": "WARN", "rule": rule, "ids": [fname], "msg": f"{fname} 表格 {name} 缺欄 {miss}"})
    return out

def run(ctx: dict, stage=None) -> dict:
    files = stage["outputs"] if stage else list(ctx["contracts"]["files"])
    ctx["contract_findings"] = check_files(ctx["dir"], ctx["contracts"], files, ctx.get("review_dir"))
    return ctx
