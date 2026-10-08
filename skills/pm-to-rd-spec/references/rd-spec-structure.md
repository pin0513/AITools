---
name: rd-spec-structure
description: RD spec 產出目錄結構與每個檔案的必要章節;S5 依此放置,面板與 script 依檔名前綴定位
---

# RD Spec 產出結構

根目錄由 `config.yaml` 的 `output.root` 決定,預設 `docs/rd-spec/{feature-slug}/`。檔名前綴數字固定,不得改名。

```
docs/rd-spec/{feature-slug}/
├── 00-overview.md            S0   背景、目標、範圍、名詞表、來源 PM spec 路徑與版本
├── 10-requirements.md        S0/1 REQ-xxx 清單(型態、來源錨點)、AC-xxx(Gherkin)、NFR-xxx(Quality Scenario)
├── 20-domain-model.md        S1   UC-xxx、STM-xxx、DDD 清單與不變量、classDiagram
├── 30-architecture-c4.md     S2   C4 L1 Context、L2 Container、L3 Component(CMP-xxx 表)、SEQ-xxx
├── 40-api-contracts.md       S2   API-xxx、錯誤碼、外部呼叫失敗模式
├── 50-data-model.md          S2   erDiagram、欄位表、索引、Data Ownership
├── 60-test-design.md         S4   TST-xxx(kind、對應 AC、對應 CMP)、Fitness Function
├── 90-traceability.md        S5   需求 × 元件 × 測試 矩陣的 md 版(給 PR review 看)
├── boundary-report.md        S3   B1–B8 每條規則的 PASS/WARN/FAIL + evidence + 處置
├── traceability.json         S5   面板資料來源(schema 見下)
├── method-log.jsonl          全程 方法論 log
├── check-panel.html          S6   一頁核對面板(由 script 產生,不手改)
└── html/                     S6   每個 md 的 html 渲染(render-stage.py 產生)
    ├── 00-overview.html
    └── ...
```

## 每個檔的必要章節

| 檔 | 必要 h2 | 缺了會怎樣 |
|---|---|---|
| 00-overview | 背景與目標、範圍(In/Out)、名詞表、來源 | S0 Gate WARN |
| 10-requirements | 需求清單、驗收條件、非功能需求 | S0 Gate FAIL |
| 20-domain-model | Use Case、狀態機(可寫「不適用」並說明)、領域模型 | S1 Gate FAIL |
| 30-architecture-c4 | Context、Container、Component、Sequence | S2 Gate FAIL |
| 40-api-contracts | 介面清單、錯誤碼、外部依賴與失敗模式 | S2 Gate WARN(無 integration 型態時可省) |
| 50-data-model | 資料表、擁有權、遷移 | S2 Gate WARN(無 data 型態時可省) |
| 60-test-design | 測試元件清單、AC 對應、Fitness Function | S4 Gate FAIL |
| 90-traceability | 矩陣、孤兒清單 | S5 Gate FAIL |

## ID 命名

| 前綴 | 對象 | 格式 |
|---|---|---|
| REQ | 需求 | `REQ-001` |
| AC | 驗收條件 | `AC-001-1`(REQ-001 的第 1 條) |
| NFR | 非功能需求 | `NFR-001` |
| UC / STM / SEQ | Use Case / State Machine / Sequence | `UC-001`,同號對應同一 REQ 為原則 |
| CMP | 技術元件 | `CMP-001` |
| API | 介面 | `API-001` |
| TST | 測試元件 | `TST-001` |

## traceability.json schema

```json
{
  "feature": "avatar-upload",
  "title": "會員上傳大頭貼",
  "generated_at": "2026-10-08T10:00:00+08:00",
  "source": { "pm_spec": "docs/pm/avatar-upload.md", "mocks": ["mock/avatar/upload.html"] },
  "io_map": [ { "in": "PM§3.1", "out": ["REQ-001"] }, { "in": "mock/avatar/upload.html", "out": ["STM-001"] } ],
  "requirements": [ { "id": "REQ-001", "title": "...", "types": ["functional"], "source": "PM§3.1", "acs": ["AC-001-1"] } ],
  "components": [ { "id": "CMP-001", "name": "AvatarController", "layer": "Api", "context": "Member", "depends": ["CMP-002"], "external": [] } ],
  "tests": [ { "id": "TST-001", "name": "UploadAvatarHandlerTests", "kind": "unit", "components": ["CMP-002"], "acs": ["AC-001-1"] } ],
  "links": [ { "req": "REQ-001", "component": "CMP-001", "via": "SEQ-001" } ],
  "boundary_checks": [ { "rule": "B2", "target": "CMP-003", "status": "FAIL", "evidence": "...", "action": "..." } ],
  "artifacts": [ { "id": "SEQ-001", "kind": "sequence", "file": "30-architecture-c4.md", "mermaid": "sequenceDiagram\n ..." } ]
}
```

孤兒定義(S5 Gate):REQ 無任何 link;CMP 無任何 link;TST 無任何 acs;AC 無任何 TST。
