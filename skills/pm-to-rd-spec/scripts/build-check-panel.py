#!/usr/bin/env python3
"""由 traceability.json + method-log.jsonl 產生一頁核對面板 check-panel.html。
用法: python3 build-check-panel.py <rd-spec-dir> [--template <path>] [--mermaid-js <mermaid.min.js>]
--mermaid-js 會把 mermaid 內嵌進 html(約 2.5MB),面板即可完全離線開啟;不給則用 cdnjs。
同時做 S5/S6 Gate 檢查:孤兒節點、0 筆方法論需求、KPI 一致性;有 FAIL 以非 0 退出碼結束(檔案仍會產生)。
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_TEMPLATE = HERE.parent / "templates" / "check-panel.html"
MERMAID_CDN_TAG = '<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/11.4.1/mermaid.min.js"></script>'

def load(d: pathlib.Path):
    tr = json.loads((d / "traceability.json").read_text(encoding="utf-8"))
    log_path = d / "method-log.jsonl"
    log = []
    if log_path.exists():
        for n, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    log.append(json.loads(line))
                except json.JSONDecodeError as e:
                    sys.exit(f"method-log.jsonl 第 {n} 行不是合法 JSON: {e}")
    return tr, log

def gate(tr, log):
    """回傳 (issues, kpis)。issues 每筆 {level, msg}。"""
    issues = []
    reqs = {r["id"]: r for r in tr.get("requirements", [])}
    cmps = {c["id"]: c for c in tr.get("components", [])}
    tests = tr.get("tests", [])
    links = tr.get("links", [])
    acs = {ac: r["id"] for r in reqs.values() for ac in r.get("acs", [])}
    superseded = {e["supersedes"] for e in log if "supersedes" in e}
    live = [e for e in log if e.get("seq") not in superseded]

    linked_req = {l["req"] for l in links}
    linked_cmp = {l["component"] for l in links}
    tested_ac = {ac for t in tests for ac in t.get("acs", [])}
    tested_cmp = {c for t in tests for c in t.get("components", [])}
    logged_req = {e["req"] for e in live if e.get("stage") in ("S1", "S2")}

    for rid in reqs:
        if rid not in linked_req:
            issues.append({"level": "FAIL", "msg": f"{rid} 無任何技術元件 link(孤兒需求)"})
        if rid not in logged_req:
            issues.append({"level": "FAIL", "msg": f"{rid} 在 S1/S2 無方法論 log(0 筆)"})
    for cid in cmps:
        if cid not in linked_cmp:
            issues.append({"level": "FAIL", "msg": f"{cid} 未被任何需求引用(孤兒元件)"})
        if cid not in tested_cmp:
            issues.append({"level": "WARN", "msg": f"{cid} 無測試元件(B7)"})
    for ac, rid in acs.items():
        if ac not in tested_ac:
            issues.append({"level": "FAIL", "msg": f"{ac}({rid})無測試元件(B7)"})
    for t in tests:
        if not t.get("acs"):
            issues.append({"level": "FAIL", "msg": f"{t['id']} 未對應任何 AC(孤兒測試)"})
    for l in links:
        if l["req"] not in reqs or l["component"] not in cmps:
            issues.append({"level": "FAIL", "msg": f"link {l} 指向不存在的節點"})
    for e in live:
        if e.get("confidence", 1) < 0.7:
            issues.append({"level": "WARN", "msg": f"{e['req']} {e['stage']} {e['method']} confidence={e['confidence']}"})

    bc = tr.get("boundary_checks", [])
    uncovered = [rid for rid in reqs if rid not in linked_req or rid not in logged_req
                 or any(ac not in tested_ac for ac in reqs[rid].get("acs", []))]
    kpis = {
        "req_count": len(reqs), "component_count": len(cmps), "test_count": len(tests),
        "boundary_pass": sum(1 for b in bc if b["status"] == "PASS"), "boundary_total": len(bc),
        "boundary_fail": sum(1 for b in bc if b["status"] == "FAIL"),
        "uncovered_req": len(uncovered),
        "open_gaps": sum(len(e.get("gaps", [])) for e in live),
    }
    return issues, kpis

def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    d = pathlib.Path(argv[1])
    tpl = pathlib.Path(argv[argv.index("--template") + 1]) if "--template" in argv else DEFAULT_TEMPLATE
    tr, log = load(d)
    issues, kpis = gate(tr, log)
    payload = {"trace": tr, "log": log, "kpis": kpis, "gate": issues}
    html = tpl.read_text(encoding="utf-8").replace("/*__DATA__*/null", json.dumps(payload, ensure_ascii=False))
    if "--mermaid-js" in argv:
        lib = pathlib.Path(argv[argv.index("--mermaid-js") + 1]).read_text(encoding="utf-8")
        html = html.replace(MERMAID_CDN_TAG, "<script>" + lib.replace("</script>", "<\\/script>") + "</script>")
    out = d / "check-panel.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out}")
    for k, v in kpis.items():
        print(f"  {k}: {v}")
    for i in issues:
        print(f"  [{i['level']}] {i['msg']}")
    fails = [i for i in issues if i["level"] == "FAIL"] + [b for b in tr.get("boundary_checks", []) if b["status"] == "FAIL"]
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
