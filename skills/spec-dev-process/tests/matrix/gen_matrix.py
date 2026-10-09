#!/usr/bin/env python3
"""測試矩陣產生器:情境(3)× 語言(3)× 架構形狀(5),以成對覆蓋產 15 份完整專案到 examples/matrix/<id>/。
每份含:既有 codebase、PM 素材(spec/mock/refs)、前一份 spec 的名詞表、SA0..7 素材、survey、RD spec(首層核心 + ui/ + api/)、
method-log、spec-reviewer、expected.yaml(baseline 與 3 個突變版的預期)。證據行號由產出的程式碼反查,不手填。
用法:python3 tests/matrix/gen_matrix.py [out_dir]"""
import json, pathlib, re, shutil, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from tests.matrix.scenarios import SCENARIOS, pairwise  # noqa: E402

SHAPE = {
    "fs-front":   {"front": "heavy", "back": "thin", "label": {"en": "full-stack, front-heavy", "zh": "全端(重前、輕後)"}},
    "fs-back":    {"front": "thin", "back": "full", "label": {"en": "full-stack, back-heavy", "zh": "全端(輕前、重後)"}},
    "fs-balance": {"front": "full", "back": "full", "label": {"en": "full-stack, balanced", "zh": "全端(均衡)"}},
    "fe-only":    {"front": "heavy", "back": None, "label": {"en": "frontend only", "zh": "純前端"}},
    "be-only":    {"front": None, "back": "full", "label": {"en": "backend only", "zh": "純後端"}},
}
FRONT_LAYERS = ["Page", "Component", "Store", "ApiClient"]
BACK_LAYERS = ["Api", "Application", "Domain", "Infrastructure"]
ALLOWED = [["Page", "Component"], ["Page", "Store"], ["Component", "Store"], ["Store", "ApiClient"], ["Page", "ApiClient"], ["ApiClient", "Api"],
           ["Api", "Application"], ["Api", "Domain"], ["Application", "Domain"], ["Infrastructure", "Domain"], ["Infrastructure", "Application"]]

# ------------------------------------------------------------------ 語言
def L(lang):  # 標題、表頭、固定字串用的語言(mixed 用中文結構)
    return "en" if lang == "en" else "zh"   # 字典鍵(zh-TW 與 mixed 都用中文結構)

def render(text, sc, lang):
    for k, t in sc["terms"].items():
        if lang == "en": rep = t["en"]
        elif lang == "zh-TW": rep = t["zh"]
        else: rep = " " + (t["sym"] if t["kind"] in ("entity", "external", "status") else t["en"]) + " "
        text = text.replace("{" + k + "}", rep)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r" ([,。、,:;!?)」』])", r"\1", text)
    text = re.sub(r"([(「『]) ", r"\1", text)
    return text.strip()

def term(sc, key, lang):
    t = sc["terms"][key]
    return t["en"] if lang == "en" else t["zh"] if lang == "zh-TW" else (t["sym"] if t["kind"] in ("entity", "external", "status") else t["en"])

def elem(sc, key, lang):
    """survey / SA2 的元素名:en → Symbol;zh-TW → 中文(靠 SA2 / 詞彙表解析);mixed → 中文 (Symbol)。"""
    t = sc["terms"][key]
    return t["sym"] if lang == "en" else t["zh"] if lang == "zh-TW" else f'{t["zh"]} ({t["sym"]})'

H = {
    "en": {"bg": "Background and Goals", "scope": "Scope", "glossary": "Glossary", "srcmap": "Source Map", "sources": "Sources",
           "reqs": "Requirements", "ac": "Acceptance Criteria", "nfr": "Non-functional Requirements", "gaps": "Gaps",
           "uc": "Use Cases", "stm": "State Machines", "dm": "Domain Model", "uistates": "UI States", "trace": "Traceability",
           "apilist": "API List", "errors": "Error Codes", "ext": "External Dependencies and Failure Modes", "tables": "Tables", "own": "Ownership",
           "tests": "Test Components", "arch": "Architecture Tests", "nouns": "Nouns", "verbs": "Verbs", "rolew": "Role Words",
           "ents": "Entities", "rels": "Relations", "roles": "Roles and Actions", "map": "Mapping", "screens": "Screens", "fv": "Field Validation",
           "users": "Users", "func": "Functional Requirements", "nfrs": "Non-functional Requirements", "accept": "Acceptance"},
    "zh": {"bg": "背景與目標", "scope": "範圍", "glossary": "名詞表", "srcmap": "來源對照", "sources": "來源",
           "reqs": "需求清單", "ac": "驗收條件", "nfr": "非功能需求", "gaps": "缺口(待 PM 確認)",
           "uc": "Use Case", "stm": "狀態機", "dm": "領域模型", "uistates": "介面狀態", "trace": "追溯(AC → 技術元件)",
           "apilist": "介面清單", "errors": "錯誤碼", "ext": "外部依賴與失敗模式", "tables": "資料表", "own": "擁有權",
           "tests": "測試元件清單", "arch": "架構測試", "nouns": "名詞", "verbs": "動詞", "rolew": "角色詞",
           "ents": "實體", "rels": "關係", "roles": "角色與動作", "map": "對應表", "screens": "畫面清單", "fv": "欄位驗證",
           "users": "使用者與情境", "func": "功能需求", "nfrs": "非功能需求", "accept": "驗收條件"},
}
COL = {  # 表頭(en 用別名,zh 用正名)
    "en": {"req": "| ID | Requirement | Type | Source Anchor | AC |", "nfr": "| ID | Stimulus | Source | Environment | Artifact | Response | Measure | Bound CMP/API | AC |",
           "gaps": "| # | Question | Affects REQ | Assumption |", "srcmap": "| PM Source | RD Artifact |", "gl": "| Term | Definition | Source |",
           "cmp": "| ID | Name | Layer | Context | depends | external | Tech |", "trace": "| AC | CMP | via | Responsibility |",
           "api": "| ID | Method | Path | Request | Response | REQ | Bound NFR | CMP |", "fm": "| External System | Caller CMP | Timeout | Retry | Fallback | Compensation |",
           "own": "| Table | Owner Context | Access From Other Contexts |", "tst": "| ID | Name | kind | CMP Refs | AC Refs |", "fit": "| NFR | Measurement | Threshold | Where |",
           "words": "| Word | POS | Source | Category |", "ents": "| Entity | Symbol | Attributes | Source Words |", "rels": "| Source | Relation | Target | Multiplicity |",
           "roles": "| Role | Action | Flow | REQ |", "survey": "| Element | Element Type | Status | Code Target | Evidence | Note |",
           "screens": "| Screen | Route | Components | Mock | REQ |", "fv": "| Screen | Field | Rule | Error Message | AC Refs |"},
    "zh": {"req": "| ID | 需求 | 型態 | 來源錨點 | AC |", "nfr": "| ID | 刺激 | 來源 | 環境 | 產物 | 回應 | 量測 | 綁定 CMP/API | AC |",
           "gaps": "| # | 問題 | 影響 REQ | 暫時假設 |", "srcmap": "| PM 來源 | RD 產物 |", "gl": "| 名詞 | 定義 | 來源 |",
           "cmp": "| ID | 名稱 | Layer | Context | depends | external | 技術 |", "trace": "| AC | CMP | via | 職責 |",
           "api": "| ID | Method | Path | Request | Response | 對應 REQ | 綁定 NFR | CMP |", "fm": "| 外部系統 | 呼叫點 CMP | 逾時 | 重試 | 降級 | 補償 |",
           "own": "| 表 | Owner Context | 其他 Context 存取方式 |", "tst": "| ID | 名稱 | kind | 對應 CMP | 對應 AC |", "fit": "| NFR | 量測方式 | 門檻 | 執行點 |",
           "words": "| 詞 | 詞性 | 來源 | 歸類 |", "ents": "| 實體 | 英文 | 屬性 | 來源詞 |", "rels": "| 來源 | 關係 | 目標 | 多重性 |",
           "roles": "| 角色 | 動作 | 流程 | 對應 REQ |", "survey": "| 模型元素 | 類型 | 狀態 | 對應 codebase | 證據 | 說明 |",
           "screens": "| 畫面 | 路由 | 元件 | Mock | 對應 REQ |", "fv": "| 畫面 | 欄位 | 規則 | 錯誤訊息 | 對應 AC |"},
}
UC = {"en": ("Primary actor", "Trigger", "Precondition", "Postcondition (success guarantee)", "Main flow", "Alternative flow", "Exception flow", "none"),
      "zh": ("主要參與者", "觸發", "前置條件", "後置條件(成功保證)", "主流程", "替代流程", "例外流程", "無")}
ROLE = {"Page": ("render and trigger {a}", "顯示並觸發{a}"), "Component": ("UI guard for {a}", "{a}的 UI 守衛"),
        "Store": ("client state transition for {a}", "{a}的前端狀態轉移"), "ApiClient": ("call the API for {a}", "呼叫{a} API"),
        "Api": ("receive the {a} request", "接收{a}請求"), "Application": ("orchestrate {a}", "編排{a}"),
        "Domain": ("enforce the {a} invariant", "{a}的業務規則與不變量"), "Repo": ("persist the {a} result", "持久化{a}結果"),
        "External": ("call the external system for {a}", "為{a}呼叫外部系統")}
TKIND = {"Page": "e2e", "Component": "unit", "Store": "unit", "ApiClient": "contract", "Api": "integration", "Application": "unit",
         "Domain": "unit", "Repo": "integration", "External": "contract"}
TECH = {"Page": "React", "Component": "React", "Store": "Zustand", "ApiClient": "", "Api": "ASP.NET Core", "Application": "MediatR",
        "Job": "ASP.NET Core", "Domain": "", "Repo": "EF Core", "External": ""}

def camel(s): return s[0].lower() + s[1:]
def esc_m(s): return s.replace('"', "'")

# ------------------------------------------------------------------ 元件
def build_components(sc, shape):
    F, B = SHAPE[shape]["front"], SHAPE[shape]["back"]
    ent = sc["terms"][sc["existing_entity"]["key"]]["sym"]
    state_sym = sc["terms"][sc["state_entity"]]["sym"]
    ext = sc["external"]; ext_sym = sc["terms"][ext["key"]]["sym"]
    C = []  # dict(name, layer, role, deps(names), external, tech, action)
    store = sc["store"] if F in ("heavy", "full") else None
    ui_comps = [a for a in sc["actions"] if a["component"]] if F in ("heavy", "full") else []
    handlers = []
    if B:
        for a in sc["actions"]:
            sym = sc["terms"][a["key"]]["sym"]
            name = sym + ("Job" if a["kind"] == "job" else "QueryHandler" if a["kind"] == "query" else "CommandHandler")
            handlers.append((a, name))
    if F:
        C.append(dict(name=sc["page"], layer="Page", role="Page", deps=[a["component"] for a in ui_comps] + ([store] if store else [sc["client"]]), external=[], tech="React", action=None))
        for a in ui_comps:
            C.append(dict(name=a["component"], layer="Component", role="Component", deps=[store] if store else [sc["client"]], external=[], tech="React", action=a["key"]))
        if store:
            C.append(dict(name=store, layer="Store", role="Store", deps=[sc["client"]], external=[], tech="Zustand", action=None))
        C.append(dict(name=sc["client"], layer="ApiClient", role="ApiClient", deps=[sc["controller"]] if B else [], external=[] if B else ["BackendAPI"], tech="", action=None))
    if B:
        domain = state_sym + " (Aggregate)" if B == "full" else None
        repo = f"Sql{ent}Repository : I{ent}Repository"
        extc = f'{ext["client"]} : {ext["iface"]}'
        C.append(dict(name=sc["controller"], layer="Api", role="Api", deps=[h for a, h in handlers if a["kind"] != "job"], external=[], tech="ASP.NET Core", action=None))
        for a, h in handlers:
            deps = ([domain] if domain else []) + [repo] + ([extc] if a["external"] else [])
            C.append(dict(name=h, layer="Application", role="Application", deps=deps, external=[], tech="ASP.NET Core" if a["kind"] == "job" else "MediatR", action=a["key"]))
        if domain:
            C.append(dict(name=domain, layer="Domain", role="Domain", deps=[], external=[], tech="", action=None))
        C.append(dict(name=repo, layer="Infrastructure", role="Repo", deps=[], external=[], tech="EF Core", action=None))
        C.append(dict(name=extc, layer="Infrastructure", role="External", deps=[], external=[ext_sym], tech="", action=None))
    for i, c in enumerate(C, 1): c["id"] = f"CMP-{i:03d}"
    by = {c["name"]: c["id"] for c in C}
    for c in C: c["dep_ids"] = [by[d] for d in c["deps"]]
    return C

def chain(sc, C, action_key):
    a = next(x for x in sc["actions"] if x["key"] == action_key)
    out = []
    for c in C:
        r = c["role"]
        if r == "Page" and a["kind"] != "job": out.append(c)
        elif r == "Component" and c["action"] == action_key: out.append(c)
        elif r in ("Store", "ApiClient"): out.append(c)
        elif r == "Api" and a["kind"] != "job": out.append(c)
        elif r == "Application" and c["action"] == action_key: out.append(c)
        elif r in ("Domain", "Repo"): out.append(c)
        elif r == "External" and a["external"]: out.append(c)
    return out

# ------------------------------------------------------------------ 既有程式碼
class Code:
    def __init__(self, root): self.root = root; self.loc = {}
    def write(self, rel, lines, marks):
        p = self.root / rel; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        for key, needle in marks.items():
            n = next(i for i, l in enumerate(lines, 1) if needle in l)
            self.loc[key] = (rel, n)

def write_codebase(proj, sc, shape):
    F, B = SHAPE[shape]["front"], SHAPE[shape]["back"]
    code = Code(proj)
    ctx = sc["ctx"]; ee = sc["existing_entity"]; ent = sc["terms"][ee["key"]]["sym"]; q = sc["existing_query"]["sym"]
    ext = sc["external"]
    if B:
        enum = f"public enum {ent}Status {{ {', '.join(ee['file_states'])} }}" if ee["file_states"] else "// no status in this aggregate yet"
        code.write(f"src/api/{ctx}.Domain/{ent}.cs", [f"namespace {ctx}.Domain;", "", enum, "", f"public sealed class {ent}", "{",
                   "    public Guid Id { get; private set; }", f"    {ee['behavior_line']}", "}"],
                   {"entity": f"public sealed class {ent}", "behavior": ee["behavior"]})
        code.write(f"src/api/{ctx}.Domain/I{ent}Repository.cs", [f"namespace {ctx}.Domain;", "", f"public interface I{ent}Repository", "{",
                   f"    Task<{ent}?> GetAsync(Guid id, CancellationToken ct);", "    Task SaveAsync(CancellationToken ct);", "}"],
                   {"repo_iface": f"public interface I{ent}Repository"})
        code.write(f"src/api/{ctx}.Application/{q}QueryHandler.cs", [f"using {ctx}.Domain;", "using MediatR;", "", f"namespace {ctx}.Application;", "",
                   f"public sealed record {q}Query(Guid Id) : IRequest<{ent}?>;", "",
                   f"public sealed class {q}QueryHandler(I{ent}Repository repo) : IRequestHandler<{q}Query, {ent}?>", "{",
                   f"    public Task<{ent}?> Handle({q}Query q, CancellationToken ct) => repo.GetAsync(q.Id, ct);", "}"],
                   {"query": f"public sealed class {q}QueryHandler"})
        code.write(f"src/api/{ctx}.Api/Controllers/{sc['controller']}.cs", [f"using {ctx}.Application;", "using MediatR;", "using Microsoft.AspNetCore.Mvc;", "",
                   f"namespace {ctx}.Api.Controllers;", "", "[ApiController]", f"public sealed class {sc['controller']}(ISender sender) : ControllerBase", "{",
                   f'    [Http{q[0:3].title() if q.startswith("Get") else "Get"}("{sc["existing_query"]["path"]}")]',
                   f"    public async Task<IActionResult> {q}(Guid id, CancellationToken ct) => Ok(await sender.Send(new {q}Query(id), ct));", "}"],
                   {"controller": f"public sealed class {sc['controller']}"})
        code.write(f"src/api/{ctx}.Infrastructure/Sql{ent}Repository.cs", [f"using {ctx}.Domain;", "", f"namespace {ctx}.Infrastructure;", "",
                   f"public sealed class Sql{ent}Repository : I{ent}Repository", "{",
                   f"    public Task<{ent}?> GetAsync(Guid id, CancellationToken ct) => Task.FromResult<{ent}?>(null);",
                   "    public Task SaveAsync(CancellationToken ct) => Task.CompletedTask;", "}"],
                   {"repo": f"public sealed class Sql{ent}Repository"})
        code.write(f"src/api/{ctx}.Infrastructure/{ext['client']}.cs", [f"namespace {ctx}.Infrastructure;", "",
                   f"public interface {ext['iface']} {{ Task {ext['method']}(Guid id, CancellationToken ct); }}", "",
                   f"public sealed class {ext['client']} : {ext['iface']}", "{",
                   f"    public Task {ext['method']}(Guid id, CancellationToken ct) => Task.CompletedTask;", "}"],
                   {"external": f"public sealed class {ext['client']}"})
        code.write(f"src/database/001_{sc['table'].lower()}.sql", ["-- existing", f"CREATE TABLE {sc['table']} (", "    Id uniqueidentifier NOT NULL PRIMARY KEY,",
                   f"    {ee['behavior']} nvarchar(50) NOT NULL", ");"], {"table": f"CREATE TABLE {sc['table']}"})
    if F:
        states = " | ".join(f"'{s}'" for s in (ee["file_states"] or [ee["behavior"]]))
        code.write(f"src/web/src/types/{ent}.ts", ["// shared front-end types (previous issue)", f"export type {ent}Status = {states};", "",
                   f"export type {ent} = {{", "  id: string;", f"  status: {ent}Status;", "};"],
                   {"fe_entity": f"export type {ent} =", "fe_behavior": f"export type {ent}Status"})
        code.write(f"src/web/src/api/{sc['client']}.ts", [f"import type {{ {ent} }} from '../types/{ent}';", "",
                   f"export async function {camel(q)}(id: string): Promise<{ent}> {{", f"  return fetch(`{sc['existing_query']['path'].replace('{id}', '${id}')}`).then(r => r.json());", "}"],
                   {"fe_client": f"export async function {camel(q)}", "fe_client_fetch": "  return fetch("})
        code.write(f"src/web/src/pages/{sc['page']}.tsx", [f"import {{ {camel(q)} }} from '../api/{sc['client']}';", "",
                   f"export function {sc['page']}({{ id }}: {{ id: string }}) {{", f"  void {camel(q)}(id);", "  return <main />;", "}"],
                   {"page": f"export function {sc['page']}", "page_call": f"  void {camel(q)}(id);"})
    return code.loc

# ------------------------------------------------------------------ 產生一份
def gen_one(out_root, shape, lang, sid):
    sc = SCENARIOS[sid]; tc_id = f"{shape}-{lang}-{sid}"; proj = out_root / tc_id
    if proj.exists(): shutil.rmtree(proj)
    proj.mkdir(parents=True)
    lg = L(lang); h = H[lg]; col = COL[lg]; F, B = SHAPE[shape]["front"], SHAPE[shape]["back"]
    T = lambda k: term(sc, k, lang); R = lambda s: render(s, sc, lang); pick = lambda d: d["en"] if lang == "en" else d["zh"]
    issue = sc["issue"]; spec = proj / "specs" / "rd" / issue / "spec"; review = proj / "specs" / "rd" / issue / "spec-review"
    inprog = proj / "specs" / "in-progress" / issue
    for d in (spec, review / "sa", inprog / "mock"): d.mkdir(parents=True, exist_ok=True)
    loc = write_codebase(proj, sc, shape)
    C = build_components(sc, shape); cid = {c["name"]: c["id"] for c in C}
    ee = sc["existing_entity"]; ent_key = ee["key"]; ent_sym = sc["terms"][ent_key]["sym"]
    title = pick(sc["title"]); shape_label = pick(SHAPE[shape]["label"])

    # ---------- 專案設定 ----------
    over = {"output": {"review_dir": "../spec-review"}, "sa_modeling": {"methodology": "uml-wordbreak"}, "survey": {"code_roots": ["src"]},
            "tech_boundary": {"bounded_contexts": [sc["ctx"]], "tech_allowlist": ["ASP.NET Core", "EF Core", "MediatR", "React", "Zustand", "xUnit", "Vitest", "Playwright", "k6"]},
            "rules": {"overrides": {"B2": {"params": {"layers": FRONT_LAYERS + BACK_LAYERS, "allowed": ALLOWED}}}}}
    if not B: over["rules"]["overrides"]["B4"] = {"params": {"adapter_layer": "ApiClient"}}
    (proj / ".spec-dev.yaml").write_text("# 產生器輸出:" + tc_id + "\n" + json.dumps(over, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---------- PM 素材 ----------
    pm = [f"# {title} (PM spec)", "", f"## 1 {h['bg']}", R(pick(sc["background"])), "", f"## 2 {h['users']}", R(pick(sc["users"])), "", f"## 3 {h['func']}"]
    for r in sc["reqs"]:
        pm += [f"### {r['anchor']} {R(pick(r['title']))}", R(pick(r["pm"])), ""]
    pm += [f"## 4 {h['nfrs']}", R(pick(sc["nfr"]["pm"])), "", f"## 5 {h['accept']}"]
    for r in sc["reqs"]:
        for ac_id, txt in r["acs"]:
            g, w, t = (R(x) for x in pick(txt)); pm.append(f"- {g} → {w} → {t}")
    (inprog / "pm-spec.md").write_text("\n".join(pm) + "\n", encoding="utf-8")
    mock_path = f"specs/in-progress/{issue}/mock/{sc['feature']}.html"
    if F:
        btns = "".join(f'<button data-action="{sc["terms"][a["key"]]["sym"]}">{T(a["key"])}</button>' for a in sc["actions"] if a["component"])
        states = "/".join(sc["states"])
        (proj / mock_path).write_text(f'<!doctype html><html><meta charset="utf-8"><title>mock</title><body style="font-family:system-ui">'
                                      f'<h2>{T(sc["state_entity"])} <span data-state="{sc["states"][0]}">{sc["states"][0]}</span></h2>'
                                      f'<!-- states: {states} -->{btns}<table><tr><th>{T(ent_key)}</th><th>status</th></tr></table></body></html>\n', encoding="utf-8")
    (inprog / "refs.md").write_text(f"# refs\n\n- `docs/architectures/overview.md`\n- shape: {shape_label}\n", encoding="utf-8")
    (proj / "docs" / "architectures").mkdir(parents=True, exist_ok=True)
    arch_txt = {"en": f"# Architecture\nShape: {shape_label}. Front layers: Page, Component, Store, ApiClient. Back layers: Api, Application, Domain, Infrastructure.\n",
                "zh": f"# 架構概觀\n形狀:{shape_label}。前端分層 Page、Component、Store、ApiClient;後端分層 Api、Application、Domain、Infrastructure。\n"}
    (proj / "docs" / "architectures" / "overview.md").write_text(pick(arch_txt), encoding="utf-8")

    # ---------- 前一份 spec 的名詞表(跨 spec 詞彙表來源)----------
    prev = proj / "specs" / "rd" / "prev" / "spec"; prev.mkdir(parents=True, exist_ok=True)
    gl_rows = []
    for k in [ent_key, sc["external"]["key"]]:
        t = sc["terms"][k]; nm = f'{t["en"]} ({t["sym"]})' if lang == "en" else f'{t["zh"]} ({t["sym"]})'
        gl_rows.append(f"| {nm} | {t['en'] if lang == 'en' else t['zh']} | prev PM§1 |")
    (prev / "00-overview.md").write_text(f"# previous issue\n\n## {h['glossary']}\n{col['gl']}\n|---|---|---|\n" + "\n".join(gl_rows) + "\n", encoding="utf-8")

    # ---------- SA 素材 ----------
    sa = review / "sa"
    def anchor_of(k):
        for r in sc["reqs"]:
            if "{" + k + "}" in pick(r["pm"]): return f"PM§{r['anchor']}"
        return "PM§1"
    kinds = {"entity": [], "external": [], "action": [], "role": []}
    for k, t in sc["terms"].items():
        if t["kind"] in kinds: kinds[t["kind"]].append(k)
    cat = {"en": {"entity": "entity candidate", "external": "external system", "action": "action", "role": "actor"},
           "zh": {"entity": "實體候選", "external": "外部系統", "action": "動作", "role": "Actor"}}[lg]
    pos = {"en": ("noun", "verb", "role"), "zh": ("名詞", "動詞", "角色")}[lg]
    w = [f"# SA1 {h['nouns']} / {h['verbs']} / {h['rolew']}", "", f"## {h['nouns']}", col["words"], "|---|---|---|---|"]
    w += [f"| {T(k)} | {pos[0]} | {anchor_of(k)} | {cat[sc['terms'][k]['kind']]} |" for k in kinds["entity"] + kinds["external"]]
    w += ["", f"## {h['verbs']}", col["words"], "|---|---|---|---|"]
    w += [f"| {T(k)} | {pos[1]} | {anchor_of(k)} | {cat['action']}: {sc['terms'][k]['sym']} |" for k in kinds["action"]]
    w += ["", f"## {h['rolew']}", col["words"], "|---|---|---|---|"]
    w += [f"| {T(k)} | {pos[2]} | {anchor_of(k)} | {cat['role']}: {sc['terms'][k]['sym']} |" for k in kinds["role"]]
    (sa / "01-break-words.md").write_text("\n".join(w) + "\n", encoding="utf-8")
    ent_keys = kinds["entity"]
    e = [f"# SA2 {h['ents']} / {h['rels']}", "", f"## {h['ents']}", col["ents"], "|---|---|---|---|"]
    for k in ent_keys:
        t = sc["terms"][k]; name = t["en"] if lang == "en" else t["zh"]
        attrs = "Id, Status" if k == sc["state_entity"] else "Id"
        e.append(f"| {name} | {t['sym']} | {attrs} | {T(k)} |")
    e += ["", f"## {h['rels']}", col["rels"], "|---|---|---|---|"]
    rels = [(sc["terms"][ent_key]["sym"], "has", sc["terms"][k]["sym"], "1..*") for k in ent_keys if k != ent_key]
    e += [f"| {a} | {r} | {b} | {m} |" for a, r, b, m in rels]
    e += ["", f"### CLS-SA-001 (REQ-001)", "```mermaid", "classDiagram"]
    e += [f"  class {sc['terms'][k]['sym']}" for k in ent_keys] + [f"  {a} --> {b} : {r}" for a, r, b, m in rels] + ["```"]
    (sa / "02-entities-relations.md").write_text("\n".join(e) + "\n", encoding="utf-8")
    ro = [f"# SA3 {h['roles']}", "", f"## {h['roles']}", col["roles"], "|---|---|---|---|"]
    for a in sc["actions"]:
        sym = sc["terms"][a["key"]]["sym"]; how = f"{a['method']} {a['path']}" if a["method"] else "job"
        req = next(r["id"] for r in sc["reqs"] if a["key"] in r["actions"])
        ro.append(f"| {T(a['actor'])} | {sym}({how}) | {T(a['key'])} | {req} |")
    (sa / "03-roles.md").write_text("\n".join(ro) + "\n", encoding="utf-8")
    ucd = ["# SA4 Use Case Diagram", "", "## Use Case Diagram", f"### UCD-001 ({', '.join(r['id'] for r in sc['reqs'])})", "```mermaid", "flowchart LR"]
    for a in sc["actions"]:
        ucd.append(f'  {a["actor"]}(["{esc_m(T(a["actor"]))}"]) --> {a["key"]}(("{esc_m(T(a["key"]))}"))')
    ucd.append("```")
    (sa / "04-usecase.md").write_text("\n".join(ucd) + "\n", encoding="utf-8")
    main = sc["reqs"][0]; ok_ac, err_ac = main["acs"][0], main["acs"][1]
    act = ["# SA5 Activity Diagram", "", "## Activity Diagram"]
    for i, rq_ in enumerate(sc["reqs"], 1):
        ok_ = pick(rq_["acs"][0][1]); er_ = pick(rq_["acs"][-1][1]) if len(rq_["acs"]) > 1 else None
        act += [f"### ACT-{i:03d} ({rq_['id']})", "```mermaid", "flowchart TD",
                f'  A["{esc_m(R(ok_[1]))}"] --> B{{"{esc_m(R(ok_[0]))}?"}}', f'  B -->|yes| C["{esc_m(R(ok_[2]))}"]']
        act += [f'  B -->|no| D["{esc_m(R(er_[2]))}"]'] if er_ else ['  B -->|no| E["—"]']
        act += ["```", ""]
    (sa / "05-activity.md").write_text("\n".join(act) + "\n", encoding="utf-8")
    a0 = next(a for a in sc["actions"] if a["key"] == main["actions"][0])
    seq = ["# SA6 Sequence Diagram", "", "## Sequence Diagram"]
    for i, rq_ in enumerate(sc["reqs"], 1):
        ax = next(a for a in sc["actions"] if a["key"] == rq_["actions"][0])
        parts = ([] if ax["kind"] == "job" else (["Web"] if F else ["Client"])) + (["API", "DB"] if B else ["BackendAPI"]) + ([sc["terms"][sc["external"]["key"]]["sym"]] if (B and ax["external"]) else [])
        seq += [f"### SEQ-SA-{i:03d} ({rq_['id']})", "```mermaid", "sequenceDiagram", f"  actor U as {sc['terms'][ax['actor']]['sym']}"]
        seq += [f"  participant {p_}" for p_ in parts]
        prev_p = "U"
        for p_ in parts:
            seq.append(f"  {prev_p}->>{p_}: {sc['terms'][ax['key']]['sym']}"); prev_p = p_
        seq += [f"  {parts[0]}-->>U: ok", "```", ""]
    (sa / "06-sequence.md").write_text("\n".join(seq) + "\n", encoding="utf-8")
    stm_reqs = ", ".join(r["id"] for r in sc["reqs"] if any(sc["terms"][k]["sym"] in [ev for _, _, ev in sc["transitions"]] for k in r["actions"])) or "REQ-001"
    stm = ["# SA7 State Diagram", "", "## State Diagram", f"### STM-SA-001 {sc['terms'][sc['state_entity']]['sym']}.Status ({stm_reqs})", "```mermaid", "stateDiagram-v2"]
    stm += [f"  {a} --> {b}: {ev}" for a, b, ev in sc["transitions"]] + ["```"]
    (sa / "07-state.md").write_text("\n".join(stm) + "\n", encoding="utf-8")

    # ---------- survey ----------
    sv = [f"# Survey Mapping", "", f"## {h['map']}", col["survey"], "|---|---|---|---|---|---|"]
    evidences = 0
    def ev(key): rel, n = loc[key]; return f"{rel}:{n}"
    if B: e_ev = ev("entity"); beh = loc["behavior"]
    else: e_ev = ev("fe_entity"); beh = loc["fe_behavior"]
    sv.append(f"| {elem(sc, ent_key, lang)} | Aggregate | modify | {ent_sym} | {e_ev} | |"); evidences += 1   # 中文元素 → 靠 SA2 / 詞彙表解析
    sv.append(f'| {ee["behavior"]} rule | Rule | existing | {ent_sym}.{ee["behavior"]} | {beh[0]}:{beh[1]} "{ee["behavior"]}" | |'); evidences += 1
    sv.append(f"| {elem(sc, sc['new_entity'], lang)} | Entity | new | {sc['terms'][sc['new_entity']]['sym']} | | |")
    qsym = sc["existing_query"]["sym"]
    qtarget = f"{qsym}QueryHandler" if B else camel(qsym)
    q_path = sc["existing_query"]["path"].split("{")[0].rstrip("/")   # 行為行:實際打的路徑(字面鎖定)
    sv.append(f"| {qsym} | Query | existing | {qtarget} | {ev('query') if B else ev('fe_client') + '; ' + ev('fe_client_fetch') + ' \"' + q_path + '\"'} | |"); evidences += 1
    for a in sc["actions"]:
        sv.append(f"| {sc['terms'][a['key']]['sym']} | {a['kind'].title()} | new | {sc['terms'][a['key']]['sym']} | | |")
    if B:
        sv.append(f"| Sql{ent_sym}Repository | Adapter | modify | Sql{ent_sym}Repository | {ev('repo')} | |"); evidences += 1
        sv.append(f"| {sc['external']['client']} | Adapter | existing | {sc['external']['client']} | {ev('external')} | |"); evidences += 1
        sv.append(f"| {sc['controller']} | Api | modify | {sc['controller']} | {ev('controller')} | |"); evidences += 1
    if F:
        # 頁面元件:宣告行只證明元件存在 → 再加一行行為行(它實際呼叫的查詢)並字面鎖定
        sv.append(f'| {sc["page"]} | Page | modify | {sc["page"]} | {ev("page")}; {ev("page_call")} "{camel(qsym)}(id)" | |'); evidences += 1
        if B: sv.append(f"| {ent_sym} type | Type | existing | {ent_sym} | {ev('fe_entity')} | |"); evidences += 1
    (review / "survey-mapping.md").write_text("\n".join(sv) + "\n", encoding="utf-8")

    # ---------- RD spec:首層核心 ----------
    ov = [f"# {title} — overview", "", f"## {h['bg']}", R(pick(sc["background"])), "", f"## {h['scope']}", f"{shape_label}", "",
          f"## {h['glossary']}", col["gl"], "|---|---|---|"]
    for k in ent_keys:
        t = sc["terms"][k]; ov.append(f"| {(t['en'] if lang == 'en' else t['zh'])} ({t['sym']}) | {T(k)} | {anchor_of(k)} |")
    ov += ["", f"## {h['srcmap']}", col["srcmap"], "|---|---|", "| PM§1 | 00-overview.md |"]
    ov += [f"| PM§{r['anchor']} | {r['id']}, UC-{r['id'][4:]} |" for r in sc["reqs"]] + [f"| PM§4 | {sc['nfr']['id']} |"]
    if F: ov.append(f"| {mock_path} | STM-UI-001 |")
    ov += ["", f"## {h['sources']}", f"- PM spec: `specs/in-progress/{issue}/pm-spec.md`"] + ([f"- Mock: `{mock_path}`"] if F else []) + [f"- refs: `specs/in-progress/{issue}/refs.md`"]
    (spec / "00-overview.md").write_text("\n".join(ov) + "\n", encoding="utf-8")

    nfr = sc["nfr"]; api_rows = []; api_id = {}
    if B or F:
        n = 0
        for a in sc["actions"]:
            if not a["method"]: continue
            n += 1; api_id[a["key"]] = f"API-{n:03d}"
    nfr_bind = api_id.get(nfr["action"]) or cid[sc["client"]] if not B else api_id.get(nfr["action"])
    rq = [f"# {title} — requirements", "", f"## {h['reqs']}", col["req"], "|---|---|---|---|---|"]
    for r in sc["reqs"]:
        rq.append(f"| {r['id']} | {R(pick(r['title']))} | {r['types']} | PM§{r['anchor']} | {', '.join(a for a, _ in r['acs'])} |")
    rq += ["", f"## {h['ac']}", "```gherkin"]
    for r in sc["reqs"]:
        for ac_id, txt in r["acs"]:
            g, w_, t_ = (R(x) for x in pick(txt))
            rq += [f"# {ac_id}", f"Given {g}", f"When {w_}", f"Then {t_}", ""]
    rq += ["```", "", f"## {h['nfr']}", col["nfr"], "|---|---|---|---|---|---|---|---|---|",
           f"| {nfr['id']} | {R(pick(nfr['pm']))} | user | normal load | {nfr_bind} | ok | {nfr['measure']} | {nfr_bind} | AC-N01-1 |",
           "", f"## {h['gaps']}", col["gaps"], "|---|---|---|---|"]
    (spec / "10-requirements.md").write_text("\n".join(rq) + "\n", encoding="utf-8")

    u = UC[lg]; dm = [f"# {title} — domain model", "", f"## {h['uc']}"]
    for r in sc["reqs"]:
        a = next(x for x in sc["actions"] if x["key"] == r["actions"][0])
        ok_ = pick(r["acs"][0][1]); err = pick(r["acs"][-1][1])
        dm += [f"### UC-{r['id'][4:]} {R(pick(r['title']))} ({r['id']})", f"- {u[0]}: {T(a['actor'])}", f"- {u[1]}: {R(ok_[1])}",
               f"- {u[2]}: {R(ok_[0])}", f"- {u[3]}: {R(ok_[2])}", f"- {u[4]}:", f"  1. {R(ok_[1])}", f"  2. {R(ok_[2])}", f"- {u[5]}: {u[7]}",
               f"- {u[6]}: {R(err[2]) if len(r['acs']) > 1 else u[7]}", "", "```mermaid", "flowchart LR",
               f'  S(["{esc_m(T(a["actor"]))}"]) --> P["{esc_m(R(ok_[1]))}"] --> Q["{esc_m(R(ok_[2]))}"]'] + \
              ([f'  P -.-> X["{esc_m(R(err[2]))}"]'] if len(r["acs"]) > 1 else []) + ["```", ""]
    st_sym = sc["terms"][sc["state_entity"]]["sym"]
    dm += [f"## {h['stm']}", f"### STM-DOM-001 {st_sym}.Status ({stm_reqs})", "```mermaid", "stateDiagram-v2"] + [f"  {a} --> {b}: {ev_}" for a, b, ev_ in sc["transitions"]] + ["```", ""]
    dm += [f"## {h['dm']}", "| Type | Name | Invariant |" if lang == "en" else "| 類型 | 名稱 | 不變量 |", "|---|---|---|",
           f"| Aggregate Root | {st_sym} | Status: {' → '.join(sc['states'])} |"]
    dm += [f"| Entity | {sc['terms'][k]['sym']} | — |" for k in ent_keys if sc["terms"][k]["sym"] != st_sym]
    dm += ["", f"### CLS-001 {st_sym} (REQ-001)", "```mermaid", "classDiagram", f"  class {st_sym} {{ +Id +Status }}"] + [f"  {a} --> {b} : {r_}" for a, r_, b, m in rels] + ["```"]
    (spec / "20-domain-model.md").write_text("\n".join(dm) + "\n", encoding="utf-8")

    ar = [f"# {title} — architecture (C4)", "", "## Context (L1)" if lang == "en" else "## Context(L1)", "### C4-L1", "```mermaid", "C4Context",
          f'  Person(u, "{esc_m(T(sc["actions"][0]["actor"]))}")', f'  System(sys, "{esc_m(title)}")']
    if B: ar.append(f'  System_Ext(ext, "{sc["terms"][sc["external"]["key"]]["sym"]}")')
    else: ar.append('  System_Ext(ext, "BackendAPI")')
    ar += ['  Rel(u, sys, "use")', '  Rel(sys, ext, "call")', "```", "", "## Container (L2)" if lang == "en" else "## Container(L2)", "### C4-L2", "```mermaid", "C4Container"]
    if F: ar.append('  Container(web, "Web", "React", "")')
    if B: ar += ['  Container(api, "API", ".NET", "")', '  ContainerDb(db, "SQL Server", "", "")']
    ar += ["```", "", "## Component (L3)" if lang == "en" else "## Component(L3)", col["cmp"], "|---|---|---|---|---|---|---|"]
    for c in C:
        ar.append(f"| {c['id']} | {c['name']} | {c['layer']} | {sc['ctx']} | {', '.join(c['dep_ids'])} | {', '.join(c['external'])} | {c['tech']} |")
    ar += ["", "### C4-L3", "```mermaid", "flowchart LR"] + [f'  {c["id"].replace("-", "")}["{esc_m(c["name"].split(" :")[0])}<br/>{c["layer"]}"]' for c in C]
    ar += [f'  {c["id"].replace("-", "")} --> {d.replace("-", "")}' for c in C for d in c["dep_ids"]] + ["```", "", f"## {h['trace']}", col["trace"], "|---|---|---|---|"]
    links = {}
    for ri, r in enumerate(sc["reqs"], 1):
        for ac_id, _ in r["acs"]:
            for ak in r["actions"]:
                for c in chain(sc, C, ak):
                    if (ac_id, c["id"]) in links: continue
                    rr = ROLE[c["role"]][0 if lang == "en" else 1].replace("{a}", T(ak))
                    links[(ac_id, c["id"])] = rr; ar.append(f"| {ac_id} | {c['id']} | SEQ-{ri:03d} | {rr} |")
    bind_cmp = cid[sc["controller"]] if B else cid[sc["client"]]
    links[("AC-N01-1", bind_cmp)] = "NFR"; ar.append(f"| AC-N01-1 | {bind_cmp} | {nfr_bind} | NFR {nfr['measure']} |")
    ar += ["", "## Sequence"]
    for i, rq_ in enumerate(sc["reqs"], 1):
        ax = next(a for a in sc["actions"] if a["key"] == rq_["actions"][0])
        seq_ch = chain(sc, C, ax["key"])
        ar += [f"### SEQ-{i:03d} (UC-{rq_['id'][4:]} / {rq_['id']})", "```mermaid", "sequenceDiagram", f"  actor U as {sc['terms'][ax['actor']]['sym']}"]
        ar += [f"  participant {c['id'].replace('-', '')} as {c['name'].split(' :')[0].split(' (')[0]}" for c in seq_ch]
        # 呼叫沿著元件依賴表走(深度優先),不畫成一條直線——否則圖與 30 的 depends 矛盾(G-DG-consistency 會抓)
        ids_ = {c["id"] for c in seq_ch}; by_id = {c["id"]: c for c in seq_ch}; m_ = lambda x: x.replace("-", "")
        pointed = {d for c in seq_ch for d in c["dep_ids"] if d in ids_}; seen = set(); act_ = sc["terms"][ax["key"]]["sym"]
        def visit(c):
            seen.add(c["id"])
            for d in c["dep_ids"]:
                if d in ids_ and d not in seen:
                    ar.append(f"  {m_(c['id'])}->>{m_(d)}: {act_}"); visit(by_id[d]); ar.append(f"  {m_(d)}-->>{m_(c['id'])}: ok")
        roots = [c for c in seq_ch if c["id"] not in pointed]
        for c in roots:
            ar.append(f"  U->>{m_(c['id'])}: {act_}"); visit(c); ar.append(f"  {m_(c['id'])}-->>U: ok")
        ar += ["```", ""]
    (spec / "30-architecture-c4.md").write_text("\n".join(ar) + "\n", encoding="utf-8")

    # ---------- 第二層:api/ ----------
    if B or F:
        (spec / "api").mkdir(exist_ok=True)
        ap = [f"# {title} — API spec", "", f"## {h['apilist']}", col["api"], "|---|---|---|---|---|---|---|---|"]
        for a in sc["actions"]:
            if not a["method"]: continue
            req = next(r["id"] for r in sc["reqs"] if a["key"] in r["actions"])
            ap.append(f"| {api_id[a['key']]} | {a['method']} | {a['path']} | json | 200 | {req} | {nfr['id'] if a['key'] == nfr['action'] else ''} | {bind_cmp} |")
        ap += ["", f"## {h['ext']}", col["fm"], "|---|---|---|---|---|---|"]
        if B: ap.append(f"| {sc['terms'][sc['external']['key']]['sym']} | {cid[sc['external']['client'] + ' : ' + sc['external']['iface']]} | 5s | 3 | 503 | retry next run |")
        else: ap.append(f"| BackendAPI | {cid[sc['client']]} | 5s | 2 | show error | — |")
        (spec / "api" / "40-api-contracts.md").write_text("\n".join(ap) + "\n", encoding="utf-8")
    if B:
        new_sym = sc["terms"][sc["new_entity"]]["sym"]
        dmd = [f"# {title} — data model", "", f"## {h['tables']}", "### ERD-001", "```mermaid", "erDiagram", f"  {sc['table']} ||--o{{ {new_sym} : has",
               f"  {sc['table']} {{", "    uniqueidentifier Id PK", "  }", f"  {new_sym} {{", "    uniqueidentifier Id PK", "  }", "```", "",
               f"## {h['own']}", col["own"], "|---|---|---|", f"| {sc['table']} | {sc['ctx']} | — |", f"| {new_sym} | {sc['ctx']} | — |"]
        (spec / "api" / "50-data-model.md").write_text("\n".join(dmd) + "\n", encoding="utf-8")

    # ---------- 第二層:ui/ ----------
    if F:
        (spec / "ui").mkdir(exist_ok=True)
        ui_ids = [c["id"] for c in C if c["layer"] in FRONT_LAYERS]
        human_reqs = [r["id"] for r in sc["reqs"] if any(next(a for a in sc["actions"] if a["key"] == k)["kind"] != "job" for k in r["actions"])]
        ui = [f"# {title} — UI spec", "", f"## {h['screens']}", col["screens"], "|---|---|---|---|---|",
              f"| {sc['page']} | /{sc['feature']} | {', '.join(ui_ids)} | {mock_path} | {', '.join(human_reqs)} |", "",
              f"## {h['uistates']}", f"### STM-UI-001 {sc['page']} (REQ-001)", "```mermaid", "stateDiagram-v2", "  [*] --> Idle", "  Idle --> Loading: submit",
              "  Loading --> Done: 200", "  Loading --> Idle: error", "```", "", f"## {h['fv']}", col["fv"], "|---|---|---|---|---|",
              f"| {sc['page']} | {sc['terms'][main['actions'][0]]['sym']} | {R(pick(err_ac[1])[0])} | {R(pick(err_ac[1])[2])} | {err_ac[0]} |"]
        (spec / "ui" / "41-ui-spec.md").write_text("\n".join(ui) + "\n", encoding="utf-8")

    # ---------- 60 測試 ----------
    ts = [f"# {title} — test design", "", f"## {h['tests']}", col["tst"], "|---|---|---|---|---|"]
    n = 0
    for c in C:
        acs = sorted({ac for (ac, ci) in links if ci == c["id"] and ac != "AC-N01-1"})
        if not acs: continue
        n += 1; ts.append(f"| TST-{n:03d} | {c['name'].split(' :')[0].split(' (')[0]}Tests | {TKIND[c['role']]} | {c['id']} | {', '.join(acs)} |")
    n += 1; ts.append(f"| TST-{n:03d} | {nfr['id']}FitnessTest | e2e | {bind_cmp} | AC-N01-1 |")
    ts += ["", "## Fitness Function", col["fit"], "|---|---|---|---|", f"| {nfr['id']} | k6 / Playwright | {nfr['measure']} | CI nightly |"]
    (spec / "60-test-design.md").write_text("\n".join(ts) + "\n", encoding="utf-8")

    # ---------- method-log ----------
    log = []; seqn = 0
    def add(req, stage, method, rule, i, o, note=""):
        nonlocal seqn; seqn += 1
        log.append({"seq": seqn, "req": req, "stage": stage, "method": method, "rule": rule, "in": i, "out": o, "evidence": "explicit", "gaps": [], "note": note})
    add("*", "S0", "Intake.Sectioning", "S0", f"specs/in-progress/{issue}/pm-spec.md", "PM§1..§5")
    add("*", "SA", "SA1.WordBreak", "SA1", "sa/00-lexicon.md", "sa/01-break-words.md")
    add("*", "SA", "SA2.Entities", "SA2", "sa/01", "sa/02-entities-relations.md")
    add("*", "SV", "Survey.Mapping", "SV", "survey-candidates.md", "survey-mapping.md")
    for r in sc["reqs"]:
        add(r["id"], "S1", "UseCase", "M1", f"PM§{r['anchor']}", f"UC-{r['id'][4:]}")
        add(r["id"], "S2", "CleanArch.Layers", "M15", f"UC-{r['id'][4:]}", ", ".join(sorted({c['id'] for k in r['actions'] for c in chain(sc, C, k)})), shape)
    add(nfr["id"], "S1", "QualityScenario", "M11", "PM§4", nfr["id"]); add(nfr["id"], "S2", "FitnessFunction", "M12", nfr["id"], f"TST-{n:03d}")
    add("*", "S4", "AC.TestMapping", "M17", "AC-*", f"TST-001..{n:03d}")
    nreq = len(sc["reqs"])
    add("*", "SA", "SA2.ClassDiagram", "SA2", "sa/01-break-words.md", "CLS-SA-001")
    add("*", "S2", "UML.Class", "M13", "CLS-SA-001", "CLS-001")
    add("*", "SA", "SA4.UseCaseDiagram", "SA4", "sa/03-roles.md", "UCD-001")
    add("*", "SA", "SA5.Activity", "SA5", "sa/04-usecase.md", ", ".join(f"ACT-{i:03d}" for i in range(1, nreq + 1)))
    add("*", "SA", "SA6.Sequence", "SA6", "sa/05-activity.md", ", ".join(f"SEQ-SA-{i:03d}" for i in range(1, nreq + 1)))
    add("*", "SA", "SA7.State", "SA7", "sa/02-entities-relations.md", "STM-SA-001")
    add("*", "S2", "C4.Context/Container", "M14", "sa/06-sequence.md", "C4-L1, C4-L2")
    add("*", "S3", "C4.Component", "M15", "30 元件表", "C4-L3")
    add("*", "S3", "UML.Sequence", "M16", "C4-L3, UC-*", ", ".join(f"SEQ-{i:03d}" for i in range(1, nreq + 1)))
    add("*", "S2", "UML.State", "M13", "STM-SA-001", "STM-DOM-001")
    if B: add("*", "S3", "ERD", "M18", "SA2 實體", "ERD-001")
    if F: add("*", "S3", "UI.StateMachine", "M19", "STM-DOM-001", "STM-UI-001")
    (spec / "method-log.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in log) + "\n", encoding="utf-8")

    # ---------- spec-reviewer ----------
    tools = proj / "specs" / "tools" / "spec-reviewer"; tools.mkdir(parents=True, exist_ok=True)
    (tools / "review.sh").write_text('#!/usr/bin/env bash\n# 用法:review.sh [--strict | --watch] [--offline];SPEC_DEV 指向 spec-dev.py\nset -euo pipefail\n'
        'HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; PROJ="$(cd "$HERE/../../.." && pwd)"\n'
        'SPEC_DEV="${SPEC_DEV:-$(cd "$PROJ/../../.." && pwd)/spec-dev.py}"\n'
        f'SPEC="$PROJ/specs/rd/{issue}/spec"\n'
        'if [[ "${1:-}" == "--strict" ]]; then shift; python3 "$SPEC_DEV" run "$SPEC" --to S6 "$@"\n'
        'elif [[ "${1:-}" == "--watch" ]]; then shift; python3 "$SPEC_DEV" review "$SPEC" --watch "$@"\n'
        'else python3 "$SPEC_DEV" review "$SPEC" "$@"; fi\n', encoding="utf-8")
    (tools / "review.sh").chmod(0o755)

    # ---------- expected.yaml(驗收預期)----------
    ent_row = next(c for c in C if c["role"] == ("Domain" if any(c["role"] == "Domain" for c in C) else "Store"))
    if any(c["role"] == "Domain" for c in C):
        repo_id = next(c["id"] for c in C if c["role"] == "Repo"); src_c = ent_row; new_deps = [repo_id]
    else:
        src_c = next(c for c in C if c["role"] == "ApiClient"); new_deps = src_c["dep_ids"] + [cid[sc["store"]]]
    row = f"| {src_c['id']} | {src_c['name']} | {src_c['layer']} | {sc['ctx']} | {', '.join(src_c['dep_ids'])} | {', '.join(src_c['external'])} | {src_c['tech']} |"
    row_bad = f"| {src_c['id']} | {src_c['name']} | {src_c['layer']} | {sc['ctx']} | {', '.join(new_deps)} | {', '.join(src_c['external'])} | {src_c['tech']} |"
    req1_acs = ", ".join(a for a, _ in sc["reqs"][0]["acs"])
    key_terms = []
    for k, t in sc["terms"].items():
        if t["kind"] not in ("entity", "role", "action"): continue
        key_terms.append(t["en"] if lang == "en" else t["zh"] if lang == "zh-TW" else (t["sym"].lower() if t["kind"] == "entity" else t["en"]))
    expected = {"id": tc_id, "shape": shape, "lang": lang, "scenario": sid, "title": title, "shape_label": shape_label,
                "spec": f"specs/rd/{issue}/spec", "review": f"specs/rd/{issue}/spec-review",
                "expect": {"fail": 0, "survey_evidences": evidences, "min_lexicon_recall": 0.6},
                "key_terms": sorted(set(key_terms)),
                "layers": sorted({c["layer"] for c in C}), "components": len(C),
                "mutants": [
                    {"name": "evidence-line", "file": f"specs/rd/{issue}/spec-review/survey-mapping.md", "old": e_ev, "new": e_ev.rsplit(":", 1)[0] + ":1", "expect_rule": "G-SV-evidence"},
                    {"name": "reverse-dependency", "file": f"specs/rd/{issue}/spec/30-architecture-c4.md", "old": row, "new": row_bad, "expect_rule": "B2"},
                    {"name": "untested-ac", "file": f"specs/rd/{issue}/spec/10-requirements.md", "old": f"| {req1_acs} |", "new": f"| {req1_acs}, AC-001-9 |", "expect_rule": "B7"},
                ] + ([{"name": "namespace-evidence", "file": f"specs/rd/{issue}/spec-review/survey-mapping.md",
                       "old": f"| modify | {ent_sym} | {e_ev} |", "new": f"| modify | {sc['ctx']}.Domain.{ent_sym} | {e_ev.rsplit(':', 1)[0]}:1 |", "expect_rule": "G-SV-evidence"}] if B else [])}
    (proj / "expected.json").write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return expected

def main(out=None):
    out = pathlib.Path(out) if out else ROOT / "examples" / "matrix"
    out.mkdir(parents=True, exist_ok=True)
    made = [gen_one(out, shape, lang, sid) for shape, lang, sid in pairwise()]
    (out / "README.md").write_text("# 測試矩陣(產生物)\n\n由 `tests/matrix/gen_matrix.py` 產生,不手改。驗收:`python3 spec-dev.py matrix examples/matrix`。\n\n"
        "| ID | 形狀 | 語言 | 情境 | 元件 | 層 |\n|---|---|---|---|---|---|\n" +
        "\n".join(f"| {e['id']} | {e['shape_label']} | {e['lang']} | {e['scenario']} {e['title']} | {e['components']} | {', '.join(e['layers'])} |" for e in made) + "\n", encoding="utf-8")
    print(f"generated {len(made)} testcases → {out}")
    return made

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
