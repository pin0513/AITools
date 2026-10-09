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
```

設定讀取順序:套件 `config.yaml` → rd-spec 目錄或任一上層的 `.spec-dev.yaml`(淺合併覆寫)。

## 流程總覽

```
PM spec (md) ──┐
               ├─► S0 Intake ─► S1 Analyze ─► S2 Design ─► S3 Boundary ─► S4 Test ─► S5 Assemble ─► S6 Panel
mock ──────────┘      │             │             │              │            │            │             │
                   REQ-xxx       UC/STM/DDD/   C4 L1-L3      B1–B8 由     TST-xxx    traceability  check-panel
                   +來源錨點      NFR scenario  UML seq/class  script 算    AC 對應     .json 抽取     .html
                   ─────── LLM 填 md 表格 + 寫 method-log.jsonl ───────┘  └──── spec-dev.py check / panel ────┘
```

| Stage | 誰做 | 輸入 | 方法論 | 產出(檔) | Gate(config.yaml) |
|---|---|---|---|---|---|
| **S0 Intake** | LLM | PM md + mock | 段落切片、型態判定 | `00-overview.md` 來源對照、`10-requirements.md` 需求清單 | 每條 REQ 有 ID 與來源錨點;必要章節齊全 |
| **S1 Analyze** | LLM | REQ | Use Case(Cockburn)、Gherkin、UML State(UI/Domain 分開)、DDD、Quality Scenario | `10` AC/NFR、`20-domain-model.md` | 每條 REQ 有型態與分析產物;UC 有後置條件 |
| **S2 Design** | LLM | S1 產物 | C4 L1–L3、UML Sequence(含 alt/opt)、Contract-first、ERD、**AC→CMP 追溯表** | `30-architecture-c4.md`、`40-api-contracts.md`、`50-data-model.md` | Component 表有 layer/context;每條 AC 有強制它的 CMP |
| **S3 Boundary** | script | md 表格 | B1–B8(`references/tech-boundary-check.md`) | `boundary-report.md` | 0 FAIL;WARN 有處置 |
| **S4 Test** | LLM | AC + CMP | Test Pyramid、AC→Test、Fitness Function、架構測試 | `60-test-design.md` | 每條 AC、每個 CMP 至少一測試 |
| **S5 Assemble** | script | 7 個 md | 抽取 + 孤兒檢查 | `traceability.json`、`90-traceability.md` | 無孤兒;assumed 都在缺口表 |
| **S6 Panel** | script | json + log | — | `check-panel.html`、`html/` | `spec-dev.py all` 退出碼 0 |

## LLM 在每個 stage 的硬性規定

1. **不編造需求**。PM 沒寫的,寫進 `10-requirements.md` 缺口表,method-log 該筆 `evidence=assumed`。mock 只抽 UI 狀態與欄位,歸 `STM-UI`,不進 Aggregate。
2. **每條 REQ 保留來源錨點**(`PM§3.2`),面板 A 區靠它對照。
3. **每條需求在 S1/S2 至少一筆 method-log**,格式見 `references/method-log-notation.md`;`evidence` 只能是 `explicit | inferred | assumed`。
4. **追溯以 AC 為單位**:`30-architecture-c4.md` 追溯表每條 AC 至少一列,寫清楚哪個 CMP 做什麼(格式檢查 / 業務規則 / 持久化)。
5. **NFR 必須綁定 CMP 或 API**,並在 `60-test-design.md` 有 Fitness Function。
6. **表格表頭不可改**:`spec-dev.py extract` 靠表頭簽名辨識表格,清單見 `references/rd-spec-structure.md`。
7. **產生物不手改**:`traceability.json`、`90-traceability.md`、`boundary-report.md`、`check-panel.html`、`html/`。要改就改 md 再重跑。
8. **Gate FAIL 就停**,回報 `spec-dev.py check` 的輸出,不往下跑。

## 方法論路由(S1/S2)

```
REQ ─► 型態判定 ─┬─ functional     ─► Use Case + Gherkin ─► Sequence ─► AC→CMP 追溯
                 ├─ state_heavy    ─► STM-DOM(持久化/影響規則的狀態才算)
                 ├─ domain_rich    ─► DDD(有生命週期 且 有跨物件一致性 → Aggregate;否則 Entity/VO)+ Class
                 ├─ data           ─► ERD + Data Ownership
                 ├─ integration    ─► C4 Context + Contract + Failure Modes
                 └─ non_functional ─► Quality Scenario(六元素)+ Fitness Function + 綁定 CMP/API
```

完整路由表 M1–M18 與產物規格:`references/methodology-map.md`。

## 核對面板

```
┌─ KPI:REQ │ CMP │ TST │ 邊界 PASS/總 (FAIL/WARN) │ 未覆蓋 REQ │ 缺口/assumed ─────────────┐
├─ A. PM 來源 ↔ RD 產物(+ 缺口表 ▸)        ├─ Gate 問題(FAIL/WARN,帶規則 id)───────────┤
├─ B. 需求 × 技術元件(Api/App/Domain/Infra)× 測試元件(unit/int/contract/e2e)× 狀態     │
│    點列展開:AC → CMP(職責)→ TST │ 該列的 B1–B8 結果 │ 該 REQ 的 method-log │ 圖 ▸     │
├─ C. 技術邊界核對:FAIL/WARN 列出;PASS 明細 ▸(收合)                                   │
├─ 架構圖 ▸(跨需求的 C4 / ERD,收合)                                                    │
├─ D. 方法論 log ▸(收合;可篩 REQ / stage / rule / evidence)                              │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

mermaid 預設走 cdnjs;封閉網路用 `--offline`(內嵌 `vendor/mermaid.min.js`,面板 +2.5MB)。

## 技術邊界核對

B1–B8 定義與判定條件:`references/tech-boundary-check.md`。全部由 `specdev/rules.py` 計算,輸入是 md 表格。宣告要變成強制,靠 `60-test-design.md` 架構測試表(NetArchTest)進 CI。

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

`examples/avatar-upload/`:7 個 md 來源 + `method-log.jsonl`,以及 `spec-dev.py all` 的全部產生物。範例**刻意**留了 1 個 B2 FAIL(Domain 依賴 Infrastructure)、1 個 B7 FAIL(AC 無測試)、2 個 assumed、1 個未結案 Spike,讓面板每種狀態都看得到。

---

**Version**: 1.1 | **Updated**: 2026-10-09
