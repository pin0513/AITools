---
name: rd-spec-structure
description: RD spec 產出目錄結構與每個檔案的必要章節;S5 依此放置,面板與 script 依檔名前綴定位
---

# RD Spec 產出結構

## 分層原則

首層放**共用核心**(需求、領域模型、架構與追溯、測試),保證一條需求只有一條追溯鏈;第二層依交付面分 `ui/` 與 `api/`,前後端團隊各自擁有。純前端只有 `ui/`(與它消費的 `api/40`),純後端只有 `api/`。舊結構(40、50 放首層)仍可解析。

```
spec/
├── 00-overview  10-requirements  20-domain-model  30-architecture-c4  60-test-design  method-log.jsonl   ← 共用核心
├── ui/41-ui-spec.md        畫面清單、介面狀態(STM-UI)、欄位驗證                                  ← 前端
└── api/40-api-contracts.md  介面清單、錯誤碼、失敗模式;api/50-data-model.md  ERD、擁有權              ← 後端 / 兩隊契約
specs/glossary.md        跨 spec 詞彙表(產生物)
specs/naming-map.md      分層命名對照表(產生物):名詞 → 符號 → UI / API / Application / Domain / Infrastructure / DB
specs/naming-overrides.md 手寫覆寫(同欄位,有值的格子覆蓋自動推導)
```

### 分層命名對照表怎麼來、怎麼用

| 欄 | 來源 |
|---|---|
| 名詞、符號 | SA2 實體表(實體 / 英文)、SA3 動作欄開頭的 PascalCase |
| UI / API / Application / Domain / Infrastructure | 30 的 Component 表:名稱含該符號者,依 Layer 歸欄;API 欄另加 SA3 的 `METHOD path` |
| DB | 50 的 erDiagram 實體 |
| 既有程式碼的名字 | survey 的「對應 codebase」欄(點號串取最後一段)+ 證據路徑判層(`*.Application/` → Application、`src/web/` → UI…) |

survey 證據驗證**只用證據所在層的名字**比對:證據在 `*.Domain/`,只認 Domain 欄;在 `src/database/`,才認 DB 欄。這是測試矩陣的突變版逼出來的:跨層通查會讓 `namespace Orders.Domain;` 因 DB 表名 `Orders` 被誤判成證據。

根目錄由 `config.yaml` 的 `output.root` 決定,預設 `docs/rd-spec/{feature-slug}/`。檔名前綴數字固定,不得改名。

```
docs/rd-spec/{feature-slug}/
├── 00-overview.md            S0   背景、目標、範圍、名詞表、來源 PM spec 路徑與版本
├── 10-requirements.md        S0/1 REQ-xxx 清單(型態、來源錨點)、AC-xxx(Gherkin)、NFR-xxx(Quality Scenario)
├── 20-domain-model.md        S1   UC-xxx、STM-xxx、DDD 清單與不變量、classDiagram
├── 30-architecture-c4.md     S2   C4 L1 Context、L2 Container、L3 Component(CMP-xxx 表)、SEQ-xxx
├── 40-api-contracts.md       S2   API-xxx、錯誤碼、外部呼叫失敗模式
├── 50-data-model.md          S2   erDiagram、欄位表、索引、Data Ownership
├── 60-test-design.md         S4   TST-xxx(kind、對應 AC、對應 CMP)、Fitness Function、架構測試
├── method-log.jsonl          全程 方法論 log(LLM 寫,append-only)
│   ── 以下為產生物,由 spec-dev.py 產生,不手改 ──
├── traceability.json         check  由上面 7 個 md 抽取 + B1–B8 結果 + Gate + KPI
├── 90-traceability.md        check  需求 × 元件 × 測試 矩陣、AC → CMP → TST、Gate 問題(給 PR review 看)
├── boundary-report.md        check  B1–B8 每條規則的 PASS/WARN/FAIL + evidence + 處置
├── check-panel.html          panel  一頁核對面板
└── html/                     render 每個 md 的 html 渲染
```

**單一事實來源**:7 個 md 檔的表格。`traceability.json` 是抽取物,改它沒用,下次 `check` 就被覆蓋。

## 每個檔的必要章節

| 檔 | 必要 h2 | 缺了會怎樣 |
|---|---|---|
| 00-overview | 背景與目標、範圍(In/Out)、名詞表、來源 | S0 Gate WARN |
| 10-requirements | 需求清單、驗收條件、非功能需求 | S0 Gate FAIL |
| 20-domain-model | Use Case、狀態機(可寫「不適用」並說明)、領域模型 | S1 Gate FAIL |
| 30-architecture-c4 | Context、Container、Component、Sequence | S2 Gate FAIL |
| 40-api-contracts | 介面清單、錯誤碼、外部依賴與失敗模式 | S2 Gate WARN(無 integration 型態時可省) |
| 50-data-model | 資料表、擁有權、遷移 | S2 Gate WARN(無 data 型態時可省) |
| 60-test-design | 測試元件清單、Fitness Function、架構測試 | S4 Gate FAIL |

## ID 命名

| 前綴 | 對象 | 格式 |
|---|---|---|
| REQ | 需求 | `REQ-001` |
| AC | 驗收條件 | `AC-001-1`(REQ-001 的第 1 條) |
| NFR | 非功能需求 | `NFR-001` |
| UC / SEQ / CLS / ERD | Use Case / Sequence / Class / ERD | `UC-001`,h3 標題以 ID 開頭,括號內寫對應 REQ:`### SEQ-001 上傳(UC-001 / REQ-001)` |
| STM-DOM / STM-UI | 領域狀態機 / 介面狀態機 | `STM-DOM-001`、`STM-UI-001`,不可混放 |
| CMP | 技術元件 | `CMP-001` |
| API | 介面 | `API-001` |
| TST | 測試元件 | `TST-001` |

## extract 讀哪些表格

表格靠**表頭前幾欄**辨識(簽名定義在 `process/io-contracts.yaml`,這裡是人讀版),順序與字樣要一致;章節標題可自由。

| 表(所在檔)| 表頭簽名 | 用途 |
|---|---|---|
| 需求清單(10)| `ID \| 需求 \| 型態 \| 來源錨點 \| AC` | REQ 與 AC 清單 |
| 非功能需求(10)| `ID \| 刺激 \| 來源 \| 環境 \| 產物 \| 回應 \| 量測 \| 綁定 CMP/API \| AC` | NFR、B6 綁定 |
| 缺口(10)| `# \| 問題 \| 影響 REQ \| 暫時假設` | assumed 證據的對照 |
| 來源對照(00)| `PM 來源 \| RD 產物` | 面板 A 區 |
| Component(30)| `ID \| 名稱 \| Layer \| Context \| depends \| external \| 技術` | B2/B3/B4/B8 |
| 追溯(30)| `AC \| CMP \| via \| 職責` | B1、矩陣、AC→CMP |
| 介面清單(40)| `ID \| Method \| Path \| … \| 對應 REQ \| 綁定 NFR \| CMP` | B6 經 API 綁 CMP |
| 失敗模式(40)| `外部系統 \| 呼叫點 CMP \| 逾時 \| 重試 \| 降級 \| 補償` | B4 |
| 擁有權(50)| `表 \| Owner Context \| …` | B5(配 erDiagram 實體)|
| 測試元件(60)| `ID \| 名稱 \| kind \| 對應 CMP \| 對應 AC` | B7、矩陣 |
| Fitness(60)| `NFR \| 量測方式 \| 門檻 \| 執行點` | B6 |

mermaid 區塊掛到最近的 h3;h3 以 `process/io-contracts.yaml` `artifacts.heading_prefixes`(UC- / STM- / SEQ- / CLS- / ERD- / C4-)開頭才會被當成 artifact,括號內的 `REQ-xxx` / `NFR-xxx` 決定它在面板哪一列展開。

## traceability.json(產生物)

頂層鍵:`feature, title, source_files, io_map, requirements, components, ac_links, apis, failure_modes, ownership, erd_entities, tests, fitness, gaps, use_cases, artifacts, extract_errors, boundary_checks, gate, kpis`。欄位對應上表,看 `examples/avatar-upload/traceability.json`。

孤兒定義(S5 Gate):REQ 無任何 AC→CMP link 且無 NFR 綁定(B1 FAIL);TST 無任何 AC;AC 無任何 TST(B7 FAIL);追溯表引用不存在的 AC/CMP。
