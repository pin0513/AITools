---
name: pm-to-rd-spec
description: |
  PM spec → RD spec 轉換工作流程。輸入 PM 規格(md)與 mock,輸出依規範結構放置的 RD spec(md+mermaid+html),
  每條需求都經方法論(Use Case / DDD / UML / C4)分析設計,並產出一頁核對面板:
  需求 × 技術元件 × 測試元件 矩陣、技術邊界核對、方法論 log(預設隱藏)。
  使用時機:(1) 收到 PM 規格要轉成工程規格 (2) 檢查既有 RD spec 的需求覆蓋與邊界 (3) Refinement 前的技術設計
  觸發短語:"轉 RD spec", "pm spec 轉換", "技術規格", "核對面板", "traceability"
---

# PM → RD Spec 工作流程

把 PM 規格轉成工程可實作、可測試、可追溯的 RD 規格。每一步轉換都有方法論背書並留下 log;最後用一頁面板核對輸入與輸出。

## 使用方式

```
/pm-to-rd-spec docs/pm/avatar-upload.md                       # 只有 md
/pm-to-rd-spec docs/pm/avatar-upload.md --mock mock/avatar/   # md + mock
/pm-to-rd-spec --check docs/rd-spec/avatar-upload/            # 只重跑 S3-S6 核對
```

能力設定讀取順序:`skills/pm-to-rd-spec/config.yaml`(預設)→ repo 根目錄 `.pm-to-rd-spec.yaml`(專案覆寫)。

## 流程總覽

```
PM spec (md) ──┐
               ├─► S0 Intake ─► S1 Analyze ─► S2 Design ─► S3 Boundary ─► S4 Test ─► S5 Assemble ─► S6 Panel
mock system ───┘      │             │             │              │            │            │             │
                   REQ-xxx       UC/State/     C4 L1-L3      PASS/WARN/    TST-xxx    rd-spec/      check-panel
                   清單           Domain/NFR    UML seq/class   FAIL         AC 對應     結構落檔       .html
                      └─────────────── 每一步都寫 method-log.jsonl ───────────────┘
```

每個 stage 的產物同時存 `md`(含 mermaid)與 `html`(由 `scripts/render-stage.py` 產生)。

## Stage 定義

| Stage | 輸入 | 方法論 | 輸出 | Gate(見 config.yaml) |
|---|---|---|---|---|
| **S0 Intake** | PM md + mock | 段落切片、需求型態判定 | `10-requirements.md`:REQ-xxx 清單,每條帶來源段落 | 每條有 ID 與來源;必要章節齊全 |
| **S1 Analyze** | REQ 清單 | Use Case、Gherkin、UML State、DDD 戰術模式、Quality Scenario | `20-domain-model.md`、UC/AC | 每條 REQ 有型態與分析產物 |
| **S2 Design** | S1 產物 | C4(Context/Container/Component)、UML Sequence/Class、Contract-first、ERD | `30-architecture-c4.md`、`40-api-contracts.md`、`50-data-model.md` | C4 L1-L3 齊全;Component 有 layer/context |
| **S3 Boundary** | S2 產物 + tech_boundary 設定 | 依賴方向、Bounded Context 契約、資料擁有權、外部系統失敗模式 | `boundary-report.md` | 0 FAIL;WARN 附處置 |
| **S4 Test** | AC + Component | Test Pyramid、AC→Test 對應 | `60-test-design.md`:TST-xxx | 每 AC、每 Component 至少一測試 |
| **S5 Assemble** | 全部 | rd-spec-structure 規範 | `traceability.json`、`90-traceability.md` | 無孤兒節點 |
| **S6 Panel** | traceability.json + method-log.jsonl | — | `check-panel.html` | 可離線開啟;KPI 一致 |

## 方法論路由(S1/S2 必做)

每條需求先判型態,再套對應方法論。路由表與產物規格見 `references/methodology-map.md`。

```
REQ ─► 型態判定 ─┬─ functional     ─► Use Case + Gherkin ─► Sequence
                 ├─ state_heavy    ─► UML State Machine
                 ├─ domain_rich    ─► DDD(Entity/VO/Aggregate)+ Class Diagram
                 ├─ data           ─► ERD + Data Ownership
                 ├─ integration    ─► C4 Context + Contract + Failure Modes
                 └─ non_functional ─► Quality Scenario(刺激/環境/回應/量測)
```

**強制規則**:一條需求可以有多個型態,但不可以 0 筆 method-log。面板對 0 筆者標 FAIL。

## 方法論 log 表示法

每次轉換寫一行到 `method-log.jsonl`,面板上以單行表示法顯示,預設隱藏。完整欄位與範例見 `references/method-log-notation.md`。

```
[REQ-002] S1 UseCase      PM§3.2 → UC-002      rule=M1 conf=0.9
[REQ-002] S2 UML.Sequence UC-002 → SEQ-002     rule=M4 conf=0.8 gap="重試次數未定義"
[REQ-002] S3 Boundary.B4  CMP-004 → PASS       rule=B4 evidence="BlobAdapter 在 Infrastructure"
```

## 核對面板(check-panel.html)

一頁,四區,預設只看得到摘要與矩陣;明細點列才展開。

```
┌─ 摘要 KPI ──────────────────────────────────────────────────────────┐
│ REQ 7 │ Component 9 │ Test 12 │ Boundary PASS 11/12 │ 未覆蓋 REQ 1 │
├─ A. 輸入 ↔ 輸出 ──────────────┬─ B. 需求 × 技術元件 × 測試元件 ────┤
│ PM§1 背景 → 00-overview       │        │Api│App│Dom│Inf│ unit│int│e2e│
│ PM§3.1 上傳 → REQ-001 ▸       │ REQ-001│ ● │ ● │ ● │ ● │  ● │ ● │ ● │
│ PM§3.2 裁切 → REQ-002 ▸       │ REQ-002│ ● │ ● │   │   │  ● │   │ ⚠ │
│ mock/avatar.html → 3 states   │ REQ-003│   │   │   │   │    │   │   │ ✗ 未覆蓋
├─ C. 技術邊界核對 ──────────────┴─────────────────────────────────────┤
│ B2 Domain→Infrastructure 依賴  CMP-003  FAIL  evidence: using Azure.Storage │
├─ D. 方法論 log ▸(預設收合)───────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────────────┘
```

產生方式:

```bash
python3 skills/pm-to-rd-spec/scripts/build-check-panel.py docs/rd-spec/avatar-upload/
# 完全離線版(內嵌 mermaid,約 +2.5MB):
python3 skills/pm-to-rd-spec/scripts/build-check-panel.py docs/rd-spec/avatar-upload/ --mermaid-js node_modules/mermaid/dist/mermaid.min.js
```

script 同時跑 S5/S6 Gate(孤兒節點、0 筆方法論需求、AC 無測試),有 FAIL 以非 0 退出碼結束但檔案照產。預設用 cdnjs 載 mermaid,封閉網路請用 `--mermaid-js`。

## 技術邊界核對

規則 B1–B8 定義在 `references/tech-boundary-check.md`。核對對象是 S2 產出的 Component 與 Contract,不是程式碼。每條規則輸出 PASS/WARN/FAIL + evidence,寫入 `traceability.json` 的 `boundary_checks`。

## 產出結構

依 `references/rd-spec-structure.md` 放置;檔名前綴數字固定,不得改名,面板與 script 依此定位。模板在 `templates/rd-spec/`。

## 執行時的硬性規定

1. **不編造需求**。PM spec 沒寫的,寫進 `gaps` 回問 PM,不自行補完。mock 只抽 UI 狀態與欄位。
2. **每條 REQ 保留來源段落錨點**(例 `PM§3.2`),面板 A 區靠它對照。
3. **NFR 必須落到具體 Component**,否則 S3 規則 B6 標 WARN。
4. **測試元件以 AC 為單位對應**,不是以 REQ 為單位;一條 AC 多個測試可以,零個不行。
5. **Gate FAIL 就停**,輸出到該 stage 為止的檔案與 `boundary-report.md`,不往下跑。
6. 技術棧預設 C# / .NET / SQL Server / Redis / MediatR / Azure;專案覆寫以 `.pm-to-rd-spec.yaml` 為準。

## 與其他 skill 的關係

| Skill | 關係 |
|---|---|
| `dev-team-ba` | S1 的 Gherkin / SPIDR 拆解規則沿用 |
| `dev-team-architect` | S2 的 NFR 補充與 Spike 判斷沿用 |
| `qa-testcase-write-guideline` | S4 的測試案例撰寫格式沿用 |
| `user-story-mastery` | S0 需求切片時的 INVEST 檢查沿用 |

## 範例

`examples/avatar-upload/` 含一份完整跑過 S0–S6 的輸出:`traceability.json`、`method-log.jsonl`、`check-panel.html`。先開 `check-panel.html` 看面板長什麼樣,再看資料檔。

---

**Version**: 1.0 | **Created**: 2026-10-08
