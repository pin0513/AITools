"""analyze.extract v1:md(唯一事實來源)→ traceability dict。只抽取 + 結構錯誤,不做規則判定(那是 rules/ + check.*)。
工具介面:run(ctx) 讀 ctx["dir"]、ctx["contracts"],寫 ctx["data"]、ctx["log"]。"""
import json, pathlib, re
from core import mdtables as M

FILES = ["00-overview.md", "10-requirements.md", "20-domain-model.md", "30-architecture-c4.md",
         "40-api-contracts.md", "50-data-model.md", "60-test-design.md"]
ID_RE = re.compile(r"\b(REQ|NFR)-\d+\b")

def _kind(code: str, kinds: dict) -> str:
    head = code.strip().splitlines()[0].strip() if code.strip() else ""
    for k, v in kinds.items():
        if head.startswith(k):
            return v
    return "other"

def extract(d: pathlib.Path, contracts: dict, review_dir: pathlib.Path = None):
    sig = {k: v["signature"] for k, v in contracts["tables"].items()}
    kinds = contracts.get("artifacts", {}).get("kinds") or {}
    prefixes = tuple(contracts.get("artifacts", {}).get("heading_prefixes") or ())
    errors, docs = [], {}
    for f in FILES:
        p = d / f
        if p.exists():
            docs[f] = M.parse(f, p.read_text(encoding="utf-8"))
        else:
            errors.append({"level": "FAIL" if contracts["files"].get(f, {}).get("required") else "WARN",
                           "rule": contracts["files"].get(f, {}).get("stage", "S5"), "ids": [f], "msg": f"缺檔 {f}"})
    tables = {}
    for doc in docs.values():
        for t in doc.tables:
            name = M.classify(t, sig)
            if name:
                tables.setdefault(name, []).extend(t.rows)

    def rows(name): return tables.get(name, [])

    reqs = []
    for r in rows("requirements"):
        reqs.append({"id": r["ID"], "title": r["需求"], "types": [x.strip() for x in r["型態"].replace(",", ",").split(",") if x.strip()],
                     "source": r.get("來源錨點", ""), "acs": M.split_ids(r.get("AC", ""))})
    for r in rows("nfr"):
        bind_col = next((h for h in r if h.startswith("綁定")), None)
        reqs.append({"id": r["ID"], "title": f'{r.get("刺激","")} → {r.get("回應","")} ({r.get("量測","")})'.strip(),
                     "types": ["non_functional"], "source": r.get("來源", ""), "acs": M.split_ids(r.get("AC", "")),
                     "binds": M.split_ids(r.get(bind_col, "")) if bind_col else [], "measure": r.get("量測", "")})
    comps = []
    for r in rows("components"):
        comps.append({"id": r["ID"], "name": r["名稱"], "layer": r["Layer"], "context": r["Context"],
                      "depends": M.split_ids(r.get("depends", "")), "external": [x.strip() for x in r.get("external", "").split(",") if x.strip()],
                      "tech": [x.strip() for x in r.get("技術", "").split(",") if x.strip()],
                      "interface": r["名稱"].split(":")[1].strip() if ":" in r["名稱"] else ""})
    ac_links = [{"ac": r["AC"], "component": r["CMP"], "via": r.get("via", ""), "role": r.get("職責", "")} for r in rows("ac_links")]
    apis = [{"id": r["ID"], "method": r["Method"], "path": r["Path"], "reqs": M.split_ids(r.get("對應 REQ", "")),
             "nfrs": M.split_ids(r.get("綁定 NFR", "")), "component": M.split_ids(r.get("CMP", ""))} for r in rows("apis")]
    failure_modes = [{"system": r["外部系統"], "component": M.split_ids(r["呼叫點 CMP"]), "timeout": r.get("逾時", ""),
                      "retry": r.get("重試", ""), "degrade": r.get("降級", ""), "compensate": r.get("補償", "")} for r in rows("failure_modes")]
    ownership = [{"table": r["表"], "owner": r["Owner Context"], "access": r.get("其他 Context 存取方式", "")} for r in rows("ownership")]
    tests = [{"id": r["ID"], "name": r["名稱"], "kind": r["kind"], "components": M.split_ids(r.get("對應 CMP", "")),
              "acs": M.split_ids(r.get("對應 AC", ""))} for r in rows("tests")]
    fitness = [{"nfr": r["NFR"], "how": r.get("量測方式", ""), "threshold": r.get("門檻", ""), "where": r.get("執行點", "")} for r in rows("fitness")]
    io_map = [{"in": r["PM 來源"], "out": [x.strip() for x in r["RD 產物"].split(",") if x.strip()]} for r in rows("io_map")]
    gaps = [{"n": r["#"], "question": r["問題"], "reqs": M.split_ids(r.get("影響 REQ", "")), "assumption": r.get("暫時假設", "")} for r in rows("gaps")]

    artifacts = []
    for doc in docs.values():
        for mm in doc.mermaid:
            mid = re.match(r"^([A-Z0-9][\w-]*)", mm.heading) if mm.heading.startswith(prefixes) else None
            req = ID_RE.search(mm.heading)
            artifacts.append({"id": mid.group(1) if mid else f"{doc.file}:{mm.line}", "kind": _kind(mm.code, kinds),
                              "file": doc.file, "line": mm.line, "heading": mm.heading, "req": req.group(0) if req else "*", "mermaid": mm.code})
    # 20-domain-model 的 UC 章節:抓 pre/post 條件是否存在
    ucs = []
    dm = docs.get("20-domain-model.md")
    if dm:
        for h in dm.h3:
            m = re.match(r"^(UC-\d+)", h)
            if m:
                body = dm.text.split("### " + h, 1)[1].split("\n### ", 1)[0] if "### " + h in dm.text else ""
                ucs.append({"id": m.group(1), "heading": h,
                            "has_pre": "前置條件" in body, "has_post": "後置條件" in body, "has_trigger": "觸發" in body,
                            "has_exception": "例外流程" in body})
    # ERD 實體名
    erd_entities = []
    for a in artifacts:
        if a["kind"] == "erd":
            erd_entities += re.findall(r"^\s*([A-Za-z_]\w*)\s*\{", a["mermaid"], re.M)

    if not reqs: errors.append({"level": "FAIL", "rule": "S0", "ids": ["10-requirements.md"], "msg": "10-requirements.md 沒有需求清單表格(表頭 ID | 需求 | 型態 …)"})
    if not comps: errors.append({"level": "FAIL", "rule": "S2", "ids": ["30-architecture-c4.md"], "msg": "30-architecture-c4.md 沒有 Component 表格(表頭 ID | 名稱 | Layer …)"})

    # ---- SA 素材與 survey(review_dir)----
    review_dir = review_dir or d
    sa_files, sa_artifacts, sa_entities, sa_roles, sa_words, survey = [], [], [], [], 0, []
    for fname, spec in contracts["files"].items():
        if spec.get("dir") != "review": continue
        p = review_dir / fname
        if not p.exists(): continue
        sa_files.append(fname)
        doc = M.parse(fname, p.read_text(encoding="utf-8"))
        for t in doc.tables:
            name = M.classify(t, sig)
            if name == "sa_entities": sa_entities += [{"name": r["實體"], "en": r.get("英文", ""), "attrs": r.get("屬性", ""), "source": r.get("來源詞", "")} for r in t.rows]
            elif name == "sa_roles": sa_roles += [{"role": r["角色"], "action": r["動作"], "flow": r.get("流程", ""), "reqs": M.split_ids(r.get("對應 REQ", ""))} for r in t.rows]
            elif name == "words": sa_words += len(t.rows)
            elif name == "survey": survey += [{"element": r["模型元素"], "kind": r["類型"], "status": r.get("狀態", ""), "target": r.get("對應 codebase", ""), "evidence": r.get("證據", ""), "note": r.get("說明", "")} for r in t.rows]
        for mm in doc.mermaid:
            mid = re.match(r"^([A-Z0-9][\w-]*)", mm.heading) if mm.heading.startswith(prefixes) else None
            req = ID_RE.search(mm.heading)
            sa_artifacts.append({"id": mid.group(1) if mid else f"{fname}:{mm.line}", "kind": _kind(mm.code, kinds), "file": fname, "line": mm.line,
                                 "heading": mm.heading, "req": req.group(0) if req else "*", "mermaid": mm.code})

    ov = docs.get("00-overview.md")
    title = ov.text.splitlines()[0].lstrip("# ").split(" — ")[0].strip() if ov else d.name
    return {
        "feature": d.name, "title": title, "source_files": sorted(docs),
        "io_map": io_map, "requirements": reqs, "components": comps, "ac_links": ac_links, "apis": apis,
        "failure_modes": failure_modes, "ownership": ownership, "erd_entities": sorted(set(erd_entities)),
        "tests": tests, "fitness": fitness, "gaps": gaps, "use_cases": ucs, "artifacts": artifacts,
        "sa_files": sa_files, "sa_artifacts": sa_artifacts, "sa_entities": sa_entities, "sa_roles": sa_roles, "sa_word_count": sa_words, "survey": survey,
        "extract_errors": errors,
    }

def load_log(d: pathlib.Path):
    p = d / "method-log.jsonl"
    log = []
    if p.exists():
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    log.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise SystemExit(f"method-log.jsonl 第 {n} 行不是合法 JSON: {e}")
    return log


def run(ctx: dict) -> dict:
    ctx["data"] = extract(ctx["dir"], ctx["contracts"], ctx.get("review_dir"))
    ctx["log"] = load_log(ctx["dir"])
    return ctx
