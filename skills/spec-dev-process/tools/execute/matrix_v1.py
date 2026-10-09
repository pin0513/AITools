"""execute.matrix v1:測試矩陣驗收。每份 testcase:baseline(全流程,0 FAIL)+ 3 個突變版(必須被指定規則抓到)
+ SA0 斷詞召回 + survey 證據驗證數。產出 acceptance.json 與驗收板 _board/(index.html 本機開、page.html 發布用、tc/<id>.html 各份核對面板)。"""
import html, json, pathlib, shutil, tempfile
from core import config as C
from tools.execute import runner_v1 as R

def _fail_rules(ctx):
    return sorted({g["rule"] for g in ctx.get("gate") or [] if g["level"] == "FAIL"} | {b["rule"] for b in ctx.get("boundary") or [] if b["status"] == "FAIL"})

def _run(spec: pathlib.Path, to="S6", offline=False):
    cfg = C.load_config(spec)
    ctx = R.make_ctx(spec, cfg, offline)
    return R.run_pipeline(ctx, to=to, no_stop=True)

def _recall(review: pathlib.Path, key_terms):
    p = review / "lexicon.json"
    if not p.exists(): return 0.0, key_terms
    rows = json.loads(p.read_text(encoding="utf-8"))
    terms = [it["term"].lower() for k in ("nouns", "actions", "roles", "statuses") for it in rows.get(k) or []]
    terms += [it["term"].lower() for it in rows.get("english") or []]
    missing = [kt for kt in key_terms if not any(kt.lower() == t or kt.lower() in t for t in terms)]
    return round(1 - len(missing) / max(1, len(key_terms)), 2), missing

def run_case(case: pathlib.Path, offline=False) -> dict:
    exp = json.loads((case / "expected.json").read_text(encoding="utf-8"))
    spec = case / exp["spec"]; review = case / exp["review"]
    ctx = _run(spec, "S6", offline)
    fails = _fail_rules(ctx)
    verified = sum(1 for g in ctx["gate"] if g["rule"] == "G-SV-evidence" and "已驗證" in g["msg"])
    recall, missing = _recall(review, exp["key_terms"])
    naming = ((ctx.get("glossary") or {}).get("naming")) or {}
    k = ctx.get("kpis") or {}
    res = {"id": exp["id"], "shape": exp["shape"], "lang": exp["lang"], "scenario": exp["scenario"], "title": exp["title"], "shape_label": exp["shape_label"],
           "baseline": {"fail_rules": fails, "fail": len(fails), "warn": sum(1 for g in ctx["gate"] if g["level"] == "WARN"),
                        "boundary": f'{k.get("boundary_pass", 0)}/{k.get("boundary_total", 0)}', "req": k.get("req_count"), "cmp": k.get("component_count"), "tst": k.get("test_count")},
           "survey": {"verified": verified, "expected": exp["expect"]["survey_evidences"]},
           "lexicon": {"recall": recall, "missing": missing, "min": exp["expect"]["min_lexicon_recall"]},
           "naming_rows": len(naming), "layers": exp["layers"], "mutants": [],
           "panel": str((review / "check-panel.html").relative_to(case))}
    for m in exp["mutants"]:
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            dst = tmp / case.name; shutil.copytree(case, dst, ignore=shutil.ignore_patterns("html", "check-panel.html"))
            f = dst / m["file"]; text = f.read_text(encoding="utf-8")
            applied = text.count(m["old"]) == 1
            if applied: f.write_text(text.replace(m["old"], m["new"]), encoding="utf-8")
            mctx = _run(dst / exp["spec"], "S5")
            got = _fail_rules(mctx)
            res["mutants"].append({"name": m["name"], "expect_rule": m["expect_rule"], "applied": applied, "fail_rules": got, "caught": applied and m["expect_rule"] in got})
        finally:
            shutil.rmtree(tmp)
    res["accepted"] = (res["baseline"]["fail"] == 0 and all(x["caught"] for x in res["mutants"])
                       and recall >= res["lexicon"]["min"] and verified == res["survey"]["expected"])
    return res

def run_matrix(root: pathlib.Path, offline=False) -> dict:
    cases = sorted(p.parent for p in root.glob("*/expected.json"))
    results = [run_case(c, offline) for c in cases]
    summary = {"cases": len(results), "accepted": sum(r["accepted"] for r in results),
               "baseline_clean": sum(r["baseline"]["fail"] == 0 for r in results),
               "mutants": sum(len(r["mutants"]) for r in results), "mutants_caught": sum(m["caught"] for r in results for m in r["mutants"]),
               "recall_by_lang": {lg: round(sum(r["lexicon"]["recall"] for r in results if r["lang"] == lg) / max(1, sum(r["lang"] == lg for r in results)), 2) for lg in ("en", "zh", "mixed")}}
    out = {"summary": summary, "results": results}
    (root / "acceptance.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    board = root / "_board"
    if board.exists(): shutil.rmtree(board)
    (board / "tc").mkdir(parents=True)
    for r, c in zip(results, cases):
        src = c / r["panel"]
        if src.exists(): shutil.copy(src, board / "tc" / f'{r["id"]}.html')
    body = board_body(out)
    (board / "page.html").write_text(body, encoding="utf-8")
    (board / "index.html").write_text("<!doctype html><html lang=\"zh-Hant\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\"></head><body>" + body + "</body></html>", encoding="utf-8")
    return out

SHAPES = [("fs-front", "全端 · 重前輕後"), ("fs-back", "全端 · 輕前重後"), ("fs-balance", "全端 · 均衡"), ("fe-only", "純前端"), ("be-only", "純後端")]
LANGS = [("en", "English"), ("zh", "中文"), ("mixed", "中英混用")]
SCEN = {"s1": "訂單取消與退款", "s2": "會議室預約", "s3": "會員點數兌換"}
MUT = {"evidence-line": "證據行號", "reverse-dependency": "反向依賴", "untested-ac": "無測試 AC", "namespace-evidence": "命名空間證據"}

def board_body(out: dict) -> str:
    e = html.escape; s = out["summary"]; by = {(r["shape"], r["lang"]): r for r in out["results"]}
    def cell(r):
        if not r: return '<td class="empty">—</td>'
        muts = "".join(f'<li class="{"ok" if m["caught"] else "bad"}" title="預期 {e(m["expect_rule"])};實際 FAIL:{e(", ".join(m["fail_rules"]) or "無")}">'
                       f'<span class="mk">{"抓到" if m["caught"] else "漏抓"}</span>{e(MUT.get(m["name"], m["name"]))}</li>' for m in r["mutants"])
        rec = r["lexicon"]["recall"]; miss = ", ".join(r["lexicon"]["missing"])
        return (f'<td><article class="case {"pass" if r["accepted"] else "fail"}">'
                f'<header><span class="sid">{e(r["scenario"].upper())}</span><span class="st">{"驗收通過" if r["accepted"] else "未通過"}</span></header>'
                f'<h3>{e(SCEN.get(r["scenario"], r["title"]))}</h3>'
                f'<dl><div><dt>baseline</dt><dd>{"0 FAIL" if r["baseline"]["fail"] == 0 else e(", ".join(r["baseline"]["fail_rules"]))}</dd></div>'
                f'<div><dt>邊界</dt><dd>{e(r["baseline"]["boundary"])}</dd></div>'
                f'<div><dt>證據</dt><dd>{r["survey"]["verified"]}/{r["survey"]["expected"]}</dd></div>'
                f'<div><dt>召回</dt><dd title="漏:{e(miss) or "無"}">{rec:.0%}</dd></div>'
                f'<div><dt>元件/對照</dt><dd>{r["baseline"]["cmp"]} · {r["naming_rows"]}</dd></div></dl>'
                f'<ul class="muts">{muts}</ul>'
                f'<a class="open" href="tc/{e(r["id"])}.html">開啟核對面板</a><code class="cid">{e(r["id"])}</code></article></td>')
    rows = "".join(f'<tr><th scope="row">{e(lbl)}</th>' + "".join(cell(by.get((sh, lg))) for lg, _ in LANGS) + "</tr>" for sh, lbl in SHAPES)
    rec = s["recall_by_lang"]
    return f"""<title>Spec Reviewer 驗收矩陣</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:wght@500;600&family=Noto+Sans+TC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* layout:摘要列 → 形狀 × 語言 的 5×3 格,每格一份 testcase;窄螢幕整張表可水平捲動 */
:root{{--bg:#f4f6f8;--surface:#ffffff;--line:#d5dce3;--fg:#17212b;--muted:#5b6876;--accent:#1f5f8b;--ok:#1d7a46;--okbg:#e3f3e9;--bad:#b3261e;--badbg:#fbe7e5;
--display:"IBM Plex Sans Condensed","Noto Sans TC",system-ui,sans-serif;--body:"Noto Sans TC",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#11171d;--surface:#18212a;--line:#2b3742;--fg:#e4eaf0;--muted:#94a3b2;--accent:#7cb6e0;--ok:#5fcf8e;--okbg:#16301f;--bad:#f2877e;--badbg:#3a1c1a;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#11171d;--surface:#18212a;--line:#2b3742;--fg:#e4eaf0;--muted:#94a3b2;--accent:#7cb6e0;--ok:#5fcf8e;--okbg:#16301f;--bad:#f2877e;--badbg:#3a1c1a;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:15px/1.55 var(--body);margin:0}}
.wrap{{max-width:1200px;margin:0 auto;padding-inline:16px;padding-block:28px 48px;display:grid;gap:24px}}
h1{{font:600 1.75rem/1.2 var(--display);margin:0;text-wrap:balance;letter-spacing:.01em}}
.lede{{color:var(--muted);margin:6px 0 0;max-width:68ch}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}
.kpi{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:12px 14px;display:grid;gap:2px}}
.kpi b{{font:600 1.6rem/1.1 var(--display);font-variant-numeric:tabular-nums}}
.kpi span{{color:var(--muted);font-size:.82rem}}
.kpi.good b{{color:var(--ok)}} .kpi.warn b{{color:var(--bad)}}
.scroll{{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--surface)}}
table.grid{{border-collapse:collapse;min-width:900px;width:100%}}
.grid th,.grid td{{border-bottom:1px solid var(--line);padding:10px;vertical-align:top;text-align:left}}
.grid thead th{{font:600 .78rem var(--display);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);background:var(--bg)}}
.grid tbody th{{font:600 .95rem var(--display);white-space:nowrap;width:130px}}
.case{{display:grid;gap:6px;padding:10px 12px;border-radius:6px;border-left:4px solid var(--ok);background:var(--bg)}}
.case.fail{{border-left-color:var(--bad)}}
.case header{{display:flex;justify-content:space-between;align-items:center;gap:8px}}
.sid{{font:500 .75rem var(--mono);color:var(--accent);letter-spacing:.06em}}
.st{{font-size:.75rem;padding:1px 8px;border-radius:999px;background:var(--okbg);color:var(--ok);font-weight:500}}
.case.fail .st{{background:var(--badbg);color:var(--bad)}}
.case h3{{margin:0;font:600 1rem/1.3 var(--body)}}
dl{{margin:0;display:grid;grid-template-columns:1fr 1fr;gap:2px 12px;font-size:.82rem}}
dl div{{display:flex;justify-content:space-between;gap:6px;border-bottom:1px dotted var(--line);white-space:nowrap}}
dt{{color:var(--muted)}} dd{{margin:0;font-family:var(--mono);font-variant-numeric:tabular-nums}}
.muts{{list-style:none;margin:2px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:4px}}
.muts li{{font-size:.75rem;border:1px solid var(--line);border-radius:4px;padding:1px 6px;display:flex;gap:4px;align-items:center}}
.muts .mk{{font-weight:700}} .muts .ok .mk{{color:var(--ok)}} .muts .bad{{border-color:var(--bad)}} .muts .bad .mk{{color:var(--bad)}}
.open{{color:var(--accent);font-weight:500;font-size:.88rem;text-decoration:none}} .open:hover,.open:focus-visible{{text-decoration:underline;outline:none}}
.cid{{font:.72rem var(--mono);color:var(--muted)}}
.notes{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.note{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:12px 14px}}
.note h2{{font:600 .8rem var(--display);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}}
.note p,.note li{{margin:0;font-size:.88rem;max-width:65ch}} .note ul{{margin:0;padding-left:18px;display:grid;gap:4px}}
code{{font-family:var(--mono)}}
td.empty{{color:var(--muted)}}
</style>
<div class="wrap">
<header><h1>Spec Reviewer 驗收矩陣</h1>
<p class="lede">3 種語言 × 3 種商業情境 × 5 種架構形狀,以成對覆蓋取 15 份完整專案。每份跑一次全流程(baseline 必須 0 FAIL),再跑 3 到 4 個刻意改壞的突變版,reviewer 必須用指定規則抓到。</p></header>
<section class="kpis" aria-label="摘要">
<div class="kpi {"good" if s["accepted"] == s["cases"] else "warn"}"><b>{s["accepted"]}/{s["cases"]}</b><span>驗收通過</span></div>
<div class="kpi {"good" if s["baseline_clean"] == s["cases"] else "warn"}"><b>{s["baseline_clean"]}/{s["cases"]}</b><span>baseline 0 FAIL</span></div>
<div class="kpi {"good" if s["mutants_caught"] == s["mutants"] else "warn"}"><b>{s["mutants_caught"]}/{s["mutants"]}</b><span>突變版被抓到</span></div>
<div class="kpi"><b>{rec["en"]:.0%} · {rec["zh"]:.0%} · {rec["mixed"]:.0%}</b><span>斷詞召回 英 · 中 · 混</span></div>
</section>
<div class="scroll"><table class="grid"><thead><tr><th>架構形狀</th>{"".join(f"<th>{e(l)}</th>" for _, l in LANGS)}</tr></thead><tbody>{rows}</tbody></table></div>
<section class="notes">
<div class="note"><h2>成對覆蓋</h2><p>情境 = (形狀序號 + 語言序號) mod 3。任兩個維度的每種組合至少出現一次:形狀 × 語言 15 組、形狀 × 情境 15 組、語言 × 情境 9 組。</p></div>
<div class="note"><h2>突變版</h2><ul><li><b>證據行號</b>:把一條 survey 證據改指第 1 行,應由 <code>G-SV-evidence</code> 抓到。</li><li><b>反向依賴</b>:Domain 依賴 Repository,或 ApiClient 依賴 Store,應由 <code>B2</code> 抓到。</li><li><b>無測試 AC</b>:在需求表加一條沒有測試的 AC,應由 <code>B7</code> 抓到。</li><li><b>命名空間證據</b>(有後端的形狀):對應欄寫 <code>Ctx.Domain.Entity</code>、證據指 namespace 行,應由 <code>G-SV-evidence</code> 抓到。</li></ul></div>
<div class="note"><h2>驗收條件</h2><ul><li>baseline 0 FAIL</li><li>每個突變版都被指定規則抓到</li><li>survey 證據驗證數 = 預期數</li><li>SA0 斷詞召回 ≥ 60%(對照情境定義的實體、角色、動作詞)</li></ul></div>
</section>
</div>"""

def run(ctx: dict) -> dict:
    ctx["matrix"] = run_matrix(ctx["dir"], ctx.get("offline"))
    return ctx
