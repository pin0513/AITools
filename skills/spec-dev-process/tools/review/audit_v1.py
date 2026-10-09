"""review.audit v1:SA 建模結果與 RD 圖的審計。對每張圖(SA、RD、自動)與每個 SA 表格列記錄:
來源(檔:行 / 自動圖的輸入列)、過程(method-log 中提到它的步驟)、目標(對應需求是否存在)、內容雜湊、機器核對結果、人工簽核狀態。
SA 的核對規格讀方法論檔 steps[*].audit(換方法論就換規格);RD 讀 rules/review/diagram-checks.yaml。
產出 review_dir/audit/:audit.json、signoff.md(人工簽核,SSOT)、history.jsonl(內容變動才追加)。"""
import datetime, hashlib, json, pathlib, re
from core import config as C, mdtables as M, yamlmini
from tools.review import checks_v1 as K, mermaid_v1 as MM

SIGNOFF_HEAD = "| 圖 | 類型 | 目標 | 簽核 hash | 目前 hash | 決定 | 審核者 | 日期 | 備註 |"

def h(code: str) -> str:
    norm = "\n".join(l.rstrip() for l in code.strip().splitlines() if l.strip())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:12]

def _checks_for(item_id: str, rd_spec: dict, sa_spec: dict) -> list:
    best, checks = -1, []
    for prefix, cs in {**rd_spec, **sa_spec}.items():
        if item_id.startswith(prefix) and len(prefix) > best: best, checks = len(prefix), cs
    return checks

def _sa_specs(meth: dict):
    dg, tb = {}, []
    for st in meth.get("steps") or []:
        a = st.get("audit") or {}
        for d in a.get("diagrams") or []: dg[d["prefix"]] = d["checks"]
        for t in a.get("tables") or []: tb.append({"step": st["id"], "file": st.get("output"), **t})
    return dg, tb

def load_signoff(path: pathlib.Path) -> dict:
    if not path.exists(): return {}
    out = {}
    for t in M.parse(path.name, path.read_text(encoding="utf-8")).tables:
        if t.header[:2] != ["圖", "類型"]: continue
        for r in t.rows:
            out[r["圖"]] = {"signed_hash": r.get("簽核 hash", ""), "decision": (r.get("決定") or "pending").strip().lower(),
                           "by": r.get("審核者", ""), "date": r.get("日期", ""), "note": r.get("備註", "")}
    return out

def write_signoff(path: pathlib.Path, items: list, prev: dict):
    L = ["# 圖與表審計 — 人工簽核", "", "<!-- SSOT:人工決定寫在這裡。決定 = approved / rejected / pending。核准時把「目前 hash」填進「簽核 hash」;",
         "     之後圖一改,目前 hash 變了,狀態自動變成 stale。工具每次執行只更新「目前 hash」與新增列,不會改你的決定。也可用 spec-dev.py signoff。 -->", "",
         "## 簽核", "", SIGNOFF_HEAD, "|---|---|---|---|---|---|---|---|---|"]
    for it in items:
        if it["type"] != "diagram": continue
        p = prev.get(it["id"], {})
        L.append(f"| {it['id']} | {it['kind']} | {', '.join(it['targets']) or '*'} | {p.get('signed_hash', '')} | {it['hash']} | {p.get('decision', 'pending') or 'pending'} | {p.get('by', '')} | {p.get('date', '')} | {p.get('note', '')} |")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")

def signoff_status(item, so):
    p = so.get(item["id"])
    if not p or p["decision"] in ("", "pending"): return "pending"
    if p["decision"] == "rejected": return "rejected"
    if p["decision"] == "approved": return "approved" if p["signed_hash"] == item["hash"] else "stale"
    return "pending"

def audit(ctx: dict) -> dict:
    data, review = ctx["data"], ctx["review_dir"]
    meth = ctx.get("methodology") or {}
    rd_spec = (yamlmini.load(C.PATHS["rules_dir"] / "review" / "diagram-checks.yaml") or {}).get("by_prefix") or {}
    sa_dg, sa_tb = _sa_specs(meth)
    req_ids = {r["id"] for r in data["requirements"]}
    log = [e for e in ctx.get("log") or [] if e.get("seq") not in {x.get("supersedes") for x in ctx.get("log") or [] if "supersedes" in x}]
    sodir = review / "audit"; sodir.mkdir(parents=True, exist_ok=True)
    so = load_signoff(sodir / "signoff.md")
    items = []
    phase_of = lambda a: "AUTO" if a.get("auto") else ("SA" if str(a.get("file", "")).startswith("sa/") or a["id"].startswith(("UCD-", "ACT-", "SEQ-SA-", "STM-SA-", "CLS-SA-")) else "RD")
    for a in (data.get("sa_artifacts") or []) + (data.get("artifacts") or []) + (data.get("auto_diagrams") or []):
        parsed = MM.parse(a["mermaid"]); targets = a.get("reqs") or ([a["req"]] if a.get("req") not in (None, "*") else [])
        it = {"type": "diagram", "id": a["id"], "phase": phase_of(a), "kind": parsed["kind"], "heading": a.get("heading", ""),
              "source": a["file"] + (f":{a['line']}" if a.get("line") else ""), "inputs": a.get("inputs") or [],
              "process": [], "targets": targets, "hash": h(a["mermaid"]), "findings": [], "mermaid": a["mermaid"]}
        word = re.compile(r"\b" + re.escape(a["id"]) + r"\b")
        if a.get("auto"): it["process"] = [{"tool": a.get("tool")}]
        else: it["process"] = [{"seq": e["seq"], "stage": e["stage"], "method": e["method"], "out": e["out"]} for e in log if word.search(str(e.get("out", ""))) or word.search(str(e.get("in", "")))]
        for t in targets:
            if t not in req_ids: it["findings"].append({"gate": "target", "outcome": "target_missing", "vars": {"req": t}})
        needs_target = a["id"].startswith(("UC-", "SEQ", "STM-", "ACT-", "UCD-", "CLS-", "AUTO-"))
        if needs_target and not targets: it["findings"].append({"gate": "target", "outcome": "target_none", "vars": {}})
        if not it["process"]: it["findings"].append({"gate": "process", "outcome": "process_none", "vars": {}})
        for chk in _checks_for(a["id"], rd_spec, sa_dg):
            fn = getattr(K, chk, None)
            if fn is None: it["findings"].append({"gate": "consistency", "outcome": "check_unknown", "vars": {"check": chk}}); continue
            for oc, vars_ in fn(a, parsed, data, ctx): it["findings"].append({"gate": "consistency", "outcome": oc, "vars": vars_, "check": chk})
        it["checks"] = _checks_for(a["id"], rd_spec, sa_dg)
        it["signoff"] = signoff_status(it, so); it["signoff_detail"] = so.get(a["id"], {})
        items.append(it)
    for spec in sa_tb:
        rows = (data.get("sa_tables") or {}).get(spec["table"]) or []
        for r in rows:
            it = {"type": "table-row", "id": f"{spec['step']}:{r.get('_file')}:{r.get('_line')}", "phase": "SA", "kind": spec["table"],
                  "heading": " | ".join(str(v) for k, v in r.items() if not k.startswith("_"))[:120], "source": f"{r.get('_file')}:{r.get('_line')}",
                  "targets": re.findall(r"\b(?:REQ|NFR)-\d+\b", r.get("對應 REQ", "")), "findings": [], "checks": spec["checks"]}
            for chk in spec["checks"]:
                for oc, vars_ in getattr(K, chk)(r, data, ctx): it["findings"].append({"gate": "sa_table", "outcome": oc, "vars": vars_, "check": chk})
            items.append(it)
    write_signoff(sodir / "signoff.md", items, so)
    dg = [i for i in items if i["type"] == "diagram"]
    summary = {"diagrams": len(dg), "table_rows": len(items) - len(dg), "by_phase": {p: sum(1 for i in dg if i["phase"] == p) for p in ("SA", "RD", "AUTO")},
               "signoff": {s: sum(1 for i in dg if i["signoff"] == s) for s in ("approved", "stale", "pending", "rejected")},
               "with_findings": sum(1 for i in items if i["findings"])}
    hist = sodir / "history.jsonl"; snap = {i["id"]: i["hash"] for i in dg}
    prev = None
    if hist.exists():
        lines = [l for l in hist.read_text(encoding="utf-8").splitlines() if l.strip()]
        prev = json.loads(lines[-1]) if lines else None
    changed = sorted(k for k in snap if prev and prev["hashes"].get(k) != snap[k])
    removed = sorted(k for k in (prev or {}).get("hashes", {}) if k not in snap)
    if not prev or prev["hashes"] != snap:
        with hist.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"at": datetime.datetime.now().isoformat(timespec="seconds"), "hashes": snap, "summary": summary}, ensure_ascii=False) + "\n")
    summary["changed_since_last"] = changed if prev else []; summary["removed_since_last"] = removed
    res = {"summary": summary, "items": items, "methodology": meth.get("id", ""), "signoff_path": str((sodir / "signoff.md").relative_to(ctx["project_root"])) if (sodir / "signoff.md").resolve().is_relative_to(ctx["project_root"]) else "audit/signoff.md"}
    (sodir / "audit.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return res

def run(ctx: dict) -> dict:
    res = audit(ctx)
    ctx.setdefault("carry", {})["audit"] = res; ctx["data"]["audit"] = res
    return ctx
