---
name: spec-dev-process
description: |
  PM spec → RD spec 轉換工作流程(可攜套件)。輸入 PM 規格(md)與 mock,輸出依規範結構放置的 RD spec(md+mermaid+html);
  每條需求經方法論(Use Case / DDD / UML / C4)分析設計並留 log;md 表格是唯一事實來源,
  spec-dev.py 機械計算技術邊界 B1–B8 與追溯,產出一頁核對面板:需求 × 技術元件 × 測試元件 矩陣、邊界核對、方法論 log(預設隱藏)。
  使用時機:(1) 收到 PM 規格要轉成工程規格 (2) 檢查既有 RD spec 的需求覆蓋與邊界 (3) Refinement 前的技術設計
  觸發短語:"轉 RD spec", "pm spec 轉換", "技術規格", "核對面板", "traceability", "spec-dev"
---

# Spec Dev Process:PM → RD Spec 工作流程

把 PM 規格轉成工程可實作、可測試、可追溯的 RD 規格。LLM 負責分析與設計並把結果填進 md 表格;`spec-dev.py` 負責抽取、核對、產面板。分工固定:**能機械判定的不交給 LLM,LLM 的判斷必須留證據**。

## 使用方式

```
/spec-dev-process docs/pm/avatar-upload.md                        # 只有 md
/spec-dev-process docs/pm/avatar-upload.md --mock mock/avatar/    # md + mock
/spec-dev-process --check docs/rd-spec/avatar-upload/             # 只重跑核對
```

CLI(不經 Claude 也能用,只需 python3):

```bash
python3 spec-dev.py init  docs/rd-spec/avatar-upload --title "會員上傳大頭貼"   # 建骨架
python3 spec-dev.py all   docs/rd-spec/avatar-upload [--offline]               # extract → check → panel → render
python3 spec-dev.py check docs/rd-spec/avatar-upload                           # 只核對;退出碼 1 = 有 FAIL
python3 spec-dev.py run   docs/rd-spec/avatar-upload --to S6                   # 嚴格:依 pipeline stop_on 停
python3 spec-dev.py review docs/rd-spec/avatar-upload                          # 全流程 + spec-reviewer 審計 + 瀏覽器渲染驗證
python3 spec-dev.py signoff docs/rd-spec/avatar-upload --id SEQ-001 --duty buildable --hash <hash> --by 名字   # 確認(看板只顯示;由 AI 呼叫)
```

設定讀取順序:套件 `config.yaml` → rd-spec 目錄或任一上層的 `.spec-dev.yaml`(深合併覆寫,含 `rules.disable` / `rules.overrides`)。

四層架構(細節見 `README.md`):`process/`(流程骨幹與 I/O 契約)→ `tools/`(analyze / check / transform / execute,`registry.yaml` 管版本)→ `rules/`(B1–B8、Gate、方法論路由全是 YAML)→ `tests/`。

## 主流程

```
PM 素材(pm spec + mock + 參考文件)
   │ S0 Intake                      → spec/00-overview.md, 10-requirements.md(REQ + 來源錨點)
   ▼
SA Modeling(方法論可抽換,預設 uml-wordbreak)
   SA0 前置解析(工具層):中/英斷詞 → 名詞/動作/角色/狀態值 → 詞頻×權重 → glossary-mapping + codebase scan → 升/降級
                                       → spec-review/sa/00-lexicon.md(LLM 之後只讀這份,不讀全檔)
   斷詞 → 實體/關係 → 角色/動作/流程 → Use Case / Activity / Sequence / State
                                       → spec-review/sa/01..07(每張圖是分析 log,面板可展開)
   ▼
SV Survey Mapping(工具掃 codebase 出候選 → 人/LLM 定案 → 工具回 codebase 驗證證據)
                                       → spec-review/survey-candidates.md(產生物)、survey-mapping.md(定案)
   ▼
S1 Analyze ─► S2 Design ─► S3 Boundary ─► S4 Test ─► S5 Assemble ─► S6 Panel
   UC/STM/DDD   C4 L1-L3     B1–B8        TST-xxx    traceability   check-panel(含 SA 素材、survey、矩陣、邊界、log)
   NFR          AC→CMP 追溯  由工具算      AC 對應    .json
   └── LLM 填 spec/ 的 md 表格 + 寫 method-log ──┘  └── spec-dev.py ──┘
   ▲                                                                   │
   └──────────── 看 check board → 改 md → 再跑(looping)────────────────┘
```

SA 的交接規則(`rules/methodology/sa/<name>.yaml` 的 `hand_off`):02 的實體 → 20 的 Entity/VO 候選;03 的角色動作 → UC;07 的狀態 → STM-DOM;survey 的 existing → 30 的 Component 沿用、modify → 標「既有修改」、new → 新 Component。

RD spec 分層:首層共用核心(00、10、20、30、60),第二層 `ui/41-ui-spec.md` 與 `api/40`、`api/50`;專案層有 `specs/glossary.md` 與 `specs/naming-map.md`(分層命名對照,工具查表,不必掃全檔)。細節見 `references/rd-spec-structure.md`。

目錄慣例(見 `examples/testcase1-form-system/`):`specs/rd/<issue>/spec/`(RD spec,唯一事實來源)與 `specs/rd/<issue>/spec-review/`(SA 素材、survey、產生物);專案 `.spec-dev.yaml` 設 `output.review_dir: ../spec-review`。

| Stage | 誰做 | 輸入 | 方法論 | 產出(檔) | Gate(`process/pipeline.yaml`) |
|---|---|---|---|---|---|
| **S0 Intake** | LLM | PM md + mock | 段落切片、型態判定 | `00-overview.md` 來源對照、`10-requirements.md` 需求清單 | 每條 REQ 有 ID 與來源錨點;必要章節齊全 |
| **SA Modeling** | 工具(SA0)+ LLM | REQ + PM 素材 + codebase docs | SA0 工具斷詞與詞頻;方法論 A:斷詞挑選、實體/關係、角色/動作/流程、UCD/ACT/SEQ/STM | `spec-review/sa/00..07.md` | G-SA-steps:每步產出存在、要求的圖至少一張 |
| **SV Survey** | tool + LLM | sa/*.md + codebase + 其他 spec | analyze.glossary 合併跨 spec 詞彙表(名詞 ↔ 符號);analyze.survey 掃 `src/` 出候選;LLM 定案 existing / modify / new | `specs/glossary.md`、`survey-candidates.md`(產生物)、`survey-mapping.md` | G-GL-consistency:本 spec 命名不與他 spec 衝突;G-SV-evidence:existing/modify 的 `path:line`(或 `path:line "字面文字"`)真的含該符號/文字;中文元素經詞彙表或 SA2 解析符號;解析不到 WARN 請人確認 |
| **S1 Analyze** | LLM | REQ + SA + survey | Use Case(Cockburn)、Gherkin、UML State(UI/Domain 分開)、DDD、Quality Scenario | `10` AC/NFR、`20-domain-model.md` | 每條 REQ 有型態與分析產物;UC 有後置條件 |
| **S2 Design** | LLM | S1 產物 | C4 L1–L3、UML Sequence(含 alt/opt)、Contract-first、ERD、**AC→CMP 追溯表** | `30-architecture-c4.md`、`40-api-contracts.md`、`50-data-model.md` | Component 表有 layer/context;每條 AC 有強制它的 CMP |
| **S3 Boundary** | tool | md 表格 | B1–B8(`rules/boundary/`,說明見 `references/tech-boundary-check.md`) | `boundary-report.md` | 0 FAIL;WARN 有處置 |
| **S4 Test** | LLM | AC + CMP | Test Pyramid、AC→Test、Fitness Function、架構測試 | `60-test-design.md` | 每條 AC、每個 CMP 至少一測試 |
| **S5 Assemble** | tool | 7 個 md | 抽取 + Gate(`rules/gates/`) | `traceability.json`、`90-traceability.md` | 無孤兒;assumed 都在缺口表 |
| **S6 Review** | tool + 人 | json + log + 全部圖 | spec-reviewer:自動圖、圖與表核對、審計(來源 / 過程 / 目標 / hash)、確認事項(以事情區分)、渲染驗證;見 `references/spec-reviewer.md` | `check-panel.html`(分頁 + modal)、`audit/`、`html/` | G-DG-* / G-SA-tables / G-S6-render 無 FAIL;確認事項無退回 |

## LLM 在每個 stage 的硬性規定

1. **不編造需求**。PM 沒寫的,寫進 `10-requirements.md` 缺口表,method-log 該筆 `evidence=assumed`。mock 只抽 UI 狀態與欄位,歸 `STM-UI`,不進 Aggregate。
2. **每條 REQ 保留來源錨點**(`PM§3.2`),面板 A 區靠它對照。
3. **每條需求在 S1/S2 至少一筆 method-log**,格式見 `references/method-log-notation.md`;`evidence` 只能是 `explicit | inferred | assumed`。
4. **元素命名中英文並存**:survey 與 SA2 的元素可用中文,但要能對到程式碼符號——SA2 實體表「英文」欄必填;survey 元素純中文時靠詞彙表或 SA2 解析,解析不到只會 WARN,不會假裝驗過。證據指到**能證明行為的那一行**並用 `"字面文字"` 鎖定,不要指函式宣告(規則只驗代理指標,不驗行為)。
5. **追溯以 AC 為單位**:`30-architecture-c4.md` 追溯表每條 AC 至少一列,寫清楚哪個 CMP 做什麼(格式檢查 / 業務規則 / 持久化)。
6. **NFR 必須綁定 CMP 或 API**,並在 `60-test-design.md` 有 Fitness Function。
7. **表格表頭不可改**:extract 靠 `process/io-contracts.yaml` 的表頭簽名辨識表格;人讀版在 `references/rd-spec-structure.md`。
8. **產生物不手改**:`traceability.json`、`90-traceability.md`、`boundary-report.md`、`check-panel.html`、`html/`、`survey-candidates.md`、`specs/glossary.md`。要改就改 md 再重跑。
9. **Gate FAIL 就停**,回報 `spec-dev.py check` 的輸出,不往下跑。

## 方法論路由(S1/S2)

```
REQ ─► 型態判定 ─┬─ functional     ─► Use Case + Gherkin ─► Sequence ─► AC→CMP 追溯
                 ├─ state_heavy    ─► STM-DOM(持久化/影響規則的狀態才算)
                 ├─ domain_rich    ─► DDD(有生命週期 且 有跨物件一致性 → Aggregate;否則 Entity/VO)+ Class
                 ├─ data           ─► ERD + Data Ownership
                 ├─ integration    ─► C4 Context + Contract + Failure Modes
                 └─ non_functional ─► Quality Scenario(六元素)+ Fitness Function + 綁定 CMP/API
```

完整路由表 M1–M18 與產物規格:`references/methodology-map.md`(資料版 `rules/methodology/routing.yaml`,contract test 保證兩邊一致)。

## 核對面板(check-panel.html)= 證據鏈 / 分析鏈 / 邏輯鏈

一個畫面內確認,不切畫面、不開別的 app:PM 原文與 mock、UML、RD 片段全部內嵌,位置用 `檔案:行` 標示。

```
┌─ KPI:REQ │ CMP │ TST │ 邊界 PASS/總 │ 未覆蓋 REQ │ 缺口/assumed ───────────────────────────┐
├─ E. 證據鏈(主區)── 每條需求一列 ─────────────────────────────────────────────────────────┤
│  PM 證據                    │ 分析鏈 ▸(收合)                  │ RD 證據                       │
│  pm-spec.md:L12 PM§3.1 原文 │ SA3 角色→動作、SA2 實體          │ AC-001-1 10:L13 gherkin 原文   │
│  mock ▸(iframe 內嵌)       │ PM§3.1 ─[S1 UseCase·M1]→ UC-001 │   元件 CMP-005 職責 30:L71      │
│                             │ UC-001 ─[S2 Sequence·M4]→ SEQ-001│   測試 TST-001 60:L6           │
│                             │ SA 圖 / RD 圖(mermaid)          │ UC-001 ▸ 20:L4 · API-001 40:L6 │
│                             │ 邏輯鏈 ▸ 為什麼是 PASS:命中規則  │                               │
│                             │   B1/B2/B7/G-* 各自的狀態與證據   │                               │
│  ▸ PM 素材全文(整份 pm-spec 段落 + 全部 mock + 參考清單)                                     │
├─ A. 來源對照 / Gate(FAIL/WARN;INFO ▸ 收合)                                                   │
├─ SA 建模素材 ▸(7 步檔,每張圖可展開)· Survey Mapping(existing/modify/new + 驗證徽章)        │
├─ B. 需求 × 技術元件 × 測試元件 矩陣(點列展開)· C. 技術邊界 · 架構圖 ▸ · D. 方法論 log ▸     │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

每張需求卡三欄:**PM 文字 ↔ 圖 ↔ RD 文字**。中間欄預設顯示兩張自動生成的圖(由資料生成,每條需求一定有圖):
- **追溯圖**:PM 段落 → REQ → AC → 各層元件(依 Layer 分組)→ 測試。
- **元件循序圖**:該需求涉及的元件依層序排列,訊息是各元件對這條 AC 的職責。

手寫的 SA / RD 圖(標題含該 REQ 者)、方法論步驟、邏輯鏈、**詞彙與已知資產**(分層命名對照 + `docs/`、`specs/done/` 中提到相關名詞的段落)收在下方,點開才看。證據鏈頂端有**查找框**,即時搜尋詞彙表、分層命名、已知資產。任何一張圖語法錯誤,會在原位標出「圖語法錯誤」並顯示原始碼,不影響其他圖。

| 鏈 | 回答的問題 | 資料來源 |
|---|---|---|
| 證據鏈 | 這條 RD 內容是從 PM 哪一段、哪張圖來的?落在 RD 哪個檔哪一行? | `00-overview.md`「## 來源」指的 PM spec / mock 路徑;各 md 表格列的行號;gherkin 區塊 |
| 分析鏈 | 中間經過哪些方法論步驟、哪些 SA 產物? | `method-log.jsonl`(依 seq)、`sa/02` 實體、`sa/03` 角色動作、SA/RD 的 mermaid |
| 邏輯鏈 | 為什麼這條需求是 PASS / WARN / FAIL? | 命中該需求(及其 AC、CMP)的 B1–B8 與 Gate 結果,含 evidence 與 action |

要讓證據鏈有料,`00-overview.md` 的「## 來源」必須列 PM spec 與 mock 的路徑(相對專案根);mock 支援 html(iframe)、png/jpg(data URI)、文字。mermaid 預設走 jsDelivr(失敗自動改 unpkg,兩者都失敗會在頁面上提示);封閉網路用 `--offline`(內嵌 `vendor/mermaid.min.js`,+2.5MB)。

## 技術邊界核對

B1–B8 定義在 `rules/boundary/`(嚴重度、訊息、參數都是資料),判定邏輯在 `tools/check/predicates_v1.py`,引擎 `tools/check/engine_v1.py`。人讀說明:`references/tech-boundary-check.md`。宣告要變成強制,靠 `60-test-design.md` 架構測試表(NetArchTest)進 CI。

## 產出結構與表格簽名

`references/rd-spec-structure.md`。檔名前綴固定;表頭簽名固定;mermaid 掛在 `UC- / STM- / SEQ- / CLS- / ERD- / C4-` 開頭的 h3 下。

## 與其他 skill 的關係

| Skill | 關係 |
|---|---|
| `dev-team-ba` | S1 的 Gherkin / SPIDR 拆解規則沿用 |
| `dev-team-architect` | S2 的 NFR 補充與 Spike 判斷沿用 |
| `qa-testcase-write-guideline` | S4 的測試案例撰寫格式沿用 |
| `user-story-mastery` | S0 需求切片時的 INVEST 檢查沿用 |

## 範例

`examples/testcase1-form-system/`:**完整端到端案例**。既有 codebase(issue a/b)+ issue c「表單審核流程」的 PM spec / mock / refs → `specs/rd/issue-c/spec-review/sa/`(SA 七步)→ `survey-mapping.md`(19 個模型元素對回 codebase)→ `spec/`(RD spec)→ check board。`specs/tools/spec-reviewer/review.sh issue-c` 一鍵跑;目標 0 FAIL。

`examples/matrix/`:**測試矩陣**。英文 / 中文 / 中英混用 × 3 種商業情境 × 5 種架構形狀(全端重前、全端重後、全端均衡、純前端、純後端),成對覆蓋 15 份完整專案,由 `tests/matrix/gen_matrix.py` 產生。`python3 spec-dev.py matrix examples/matrix` 每份跑 baseline 加 3 到 4 個突變版,產出 `examples/matrix/_board/index.html` 驗收板。

`examples/avatar-upload/`:7 個 md 來源 + `method-log.jsonl`,以及 `spec-dev.py all` 的全部產生物。範例**刻意**留了 1 個 B2 FAIL(Domain 依賴 Infrastructure)、1 個 B7 FAIL(AC 無測試)、2 個 assumed、1 個未結案 Spike,讓面板每種狀態都看得到。

---

**Version**: 2.4 | **Updated**: 2026-10-09
