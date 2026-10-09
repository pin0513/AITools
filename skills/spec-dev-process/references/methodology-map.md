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
| `state_heavy` | 狀態詞 ≥ 3 個 **且狀態會持久化或影響業務規則**;只在畫面上切換的(idle/loading/done)不算,那是 UI 狀態 | 訂單生命週期、審核流程 |
| `domain_rich` | 業務規則 ≥ 3 條、有計算公式、有一致性約束 | 折扣計算、庫存扣減 |
| `data` | 新增欄位/表、匯入匯出、報表、歷史保留 | 會員資料匯入、月報 |
| `integration` | 第三方、API、Webhook、同步、排程 | 金流串接、簡訊發送 |
| `non_functional` | 時間/量/率/安全/合規的數字或形容詞 | 「要快」「支援千人」「個資」 |

「要快」「很多人用」這種形容詞算 `non_functional` 訊號,但必須在 S1 轉成 Quality Scenario 的量測值;轉不出數字 → 寫進 `gaps` 回問 PM。

## 路由表

| 型態 | 方法論 (rule id) | 產物 | 表示法 | 落在哪個檔 |
|---|---|---|---|---|
| functional | Use Case (M1) | UC-xxx(Cockburn):參與者、觸發、前置條件、**後置條件**、主/替代/例外流程。後置條件是 M5 不變量與 M17 測試斷言的來源,缺了 Gate WARN | 文字 + mermaid `flowchart` | `20-domain-model.md` |
| functional | Gherkin (M2) | AC-xxx-n:Given/When/Then | Gherkin 區塊 | `10-requirements.md` |
| functional | UML Sequence (M4) | SEQ-xxx:每個 UC 一張;例外流程若互動對象不同,用 `alt`/`opt` fragment 畫進同一張 | mermaid `sequenceDiagram` | `30-architecture-c4.md` |
| state_heavy | UML State Machine (M3) | STM-DOM-xxx(領域,掛 Aggregate)/ STM-UI-xxx(介面,從 mock 抽);兩者分開放,UI 狀態不進 Aggregate | mermaid `stateDiagram-v2` | `20-domain-model.md` |
| domain_rich | DDD 戰術模式 (M5) | Entity / VO / Aggregate / Domain Event 清單 + 不變量 + 來源 UC 後置條件。**建 Aggregate 的判準**:有自己的生命週期 且 有跨物件一致性約束;缺一就是既有 Aggregate 的 Entity/VO | 表格 + mermaid `classDiagram` | `20-domain-model.md` |
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
| architecture | AC→Component (M18) | 追溯表:每條 AC 由哪個 CMP 強制、職責是什麼(格式檢查 / 業務規則 / 持久化)| 表格 | `30-architecture-c4.md` |
| test | AC→Test Mapping (M17) | 每條 AC 對到 ≥ 1 個 TST(TST = 測試類別,不是方法)| 表格 | `60-test-design.md` |

## S2 Component 命名與屬性

Component 表格(`30-architecture-c4.md`)的欄位就是規則的輸入:

| 欄 | 寫法 | 被哪條規則讀 |
|---|---|---|
| 名稱 | `Impl : IInterface` 代表經介面暴露 | B2(Application→Infrastructure 經介面則 PASS) |
| Layer | Api / Application / Domain / Infrastructure | B2 |
| Context | Bounded Context 名 | B3 |
| depends | CMP ID,逗號分隔 | B2、B3 |
| external | 外部系統名 | B4(配 40-api-contracts 失敗模式表) |
| 技術 | 套件/框架名 | B8(配 config tech_allowlist) |

MediatR 棧的預設切法:Controller(Api)→ Command/Query Handler(Application)→ Aggregate/Domain Service(Domain)← Repository/Adapter(Infrastructure)。

## 不要做的事

- 不要為 `functional` 需求硬畫 state diagram;狀態 < 3 個就用 UC 替代流程表達。
- 不要把 mock 的畫面狀態寫成領域狀態機;它屬於 STM-UI,不掛 Aggregate。
- 不要為每個 Component 畫 class diagram;只畫 `domain_rich` 命中的 Aggregate。
- 不要在 S1 決定技術(Redis、Blob);技術選型是 S2 的事,S1 只寫「需要分散式快取」這種能力需求。
