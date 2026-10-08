---
name: methodology-map
description: 需求型態 → 方法論 → 表示法(UML / C4 / Gherkin / ERD)的路由表,S1 與 S2 依此決定每條需求的分析與設計產物
---

# 方法論路由表

每條需求先判型態,再查表決定要產出哪些分析/設計產物。一條需求可命中多個型態,每個命中都要各寫一筆 method-log。

## 型態判定訊號

| 型態 | 判定訊號(PM spec 出現的字眼/結構) | 典型例子 |
|---|---|---|
| `functional` | 「使用者可以…」「系統應…」、有明確操作者與結果 | 上傳大頭貼、查詢訂單 |
| `state_heavy` | 狀態詞 ≥ 3 個、有「轉為」「變更為」「逾期」「取消」 | 訂單生命週期、審核流程 |
| `domain_rich` | 業務規則 ≥ 3 條、有計算公式、有一致性約束 | 折扣計算、庫存扣減 |
| `data` | 新增欄位/表、匯入匯出、報表、歷史保留 | 會員資料匯入、月報 |
| `integration` | 第三方、API、Webhook、同步、排程 | 金流串接、簡訊發送 |
| `non_functional` | 時間/量/率/安全/合規的數字或形容詞 | 「要快」「支援千人」「個資」 |

「要快」「很多人用」這種形容詞算 `non_functional` 訊號,但必須在 S1 轉成 Quality Scenario 的量測值;轉不出數字 → 寫進 `gaps` 回問 PM。

## 路由表

| 型態 | 方法論 (rule id) | 產物 | 表示法 | 落在哪個檔 |
|---|---|---|---|---|
| functional | Use Case (M1) | UC-xxx:主流程、替代流程、例外流程 | 文字 + mermaid `flowchart` | `20-domain-model.md` |
| functional | Gherkin (M2) | AC-xxx-n:Given/When/Then | Gherkin 區塊 | `10-requirements.md` |
| functional | UML Sequence (M4) | SEQ-xxx:每個 UC 主流程一張 | mermaid `sequenceDiagram` | `30-architecture-c4.md` |
| state_heavy | UML State Machine (M3) | STM-xxx:狀態、事件、守衛、動作 | mermaid `stateDiagram-v2` | `20-domain-model.md` |
| domain_rich | DDD 戰術模式 (M5) | Entity / Value Object / Aggregate / Domain Event 清單 + 不變量 | 表格 + mermaid `classDiagram` | `20-domain-model.md` |
| data | ERD (M6) | 表、欄位、鍵、索引、保留期 | mermaid `erDiagram` | `50-data-model.md` |
| data | Data Ownership (M7) | 每張表唯一 owner context | 表格 | `50-data-model.md` |
| integration | C4 Context (M8) | 外部系統、方向、協定 | mermaid `C4Context` | `30-architecture-c4.md` |
| integration | Contract-first (M9) | API-xxx:endpoint、request/response、錯誤碼 | 表格 + 範例 JSON | `40-api-contracts.md` |
| integration | Failure Modes (M10) | 每個外部呼叫:逾時、重試、降級、補償 | 表格 | `40-api-contracts.md` |
| non_functional | Quality Scenario (M11) | NFR-xxx:刺激 / 來源 / 環境 / 產物 / 回應 / 量測 | 表格 | `10-requirements.md` |
| non_functional | Fitness Function (M12) | 可自動量測的檢查(例 P95 < 500ms 的 load test) | 表格 | `60-test-design.md` |
| architecture | C4 Container (M13) | 執行單元、技術、通訊 | mermaid `C4Container` | `30-architecture-c4.md` |
| architecture | C4 Component (M14) | CMP-xxx:每個 Component 帶 `layer` + `context` | mermaid `C4Component` | `30-architecture-c4.md` |
| architecture | Clean Architecture Layers (M15) | Component → Api/Application/Domain/Infrastructure 歸屬 | 表格 | `30-architecture-c4.md` |
| test | Test Pyramid (M16) | TST-xxx:kind ∈ unit/integration/contract/e2e | 表格 | `60-test-design.md` |
| test | AC→Test Mapping (M17) | 每條 AC 對到 ≥ 1 個 TST | 矩陣 | `90-traceability.md` |

## S2 Component 命名與屬性

```
CMP-xxx
  name:    依技術棧慣例(C#:AvatarController / UploadAvatarCommandHandler / AvatarRepository)
  layer:   Api | Application | Domain | Infrastructure
  context: Bounded Context 名稱(取自 tech_boundary.bounded_contexts)
  depends: [CMP-yyy, ...]            # 用於 B2 依賴方向核對
  external: [AzureBlob]              # 若直接呼叫外部系統,用於 B4
```

MediatR 棧的預設切法:Controller(Api)→ Command/Query Handler(Application)→ Aggregate/Domain Service(Domain)← Repository/Adapter(Infrastructure)。

## 不要做的事

- 不要為 `functional` 需求硬畫 state diagram;狀態 < 3 個就用 UC 替代流程表達。
- 不要為每個 Component 畫 class diagram;只畫 `domain_rich` 命中的 Aggregate。
- 不要在 S1 決定技術(Redis、Blob);技術選型是 S2 的事,S1 只寫「需要分散式快取」這種能力需求。
