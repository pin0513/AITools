---
name: sa-modeling
description: SA 建模階段的方法論 A(uml-wordbreak)人讀說明:七步各自的輸入、方法、判準與常見錯誤;資料版在 rules/methodology/sa/uml-wordbreak.yaml
---

# SA 建模:方法論 A(UML word-break)

目的:在寫 RD spec 之前,先把 PM 素材變成一組**可核對的模型**(實體、角色、流程、狀態),讓後面的 Component 設計有依據,也讓 survey 有東西可以對回 codebase。方法論可抽換:`config.sa_modeling.methodology` 指到 `rules/methodology/sa/` 下另一個 YAML 即可;pipeline 的 SA stage 產出清單由該 YAML 的 `steps[*].output` 決定。

## 七步

| 步 | 輸入 | 做什麼 | 判準 | 常見錯誤 |
|---|---|---|---|---|
| SA1 斷詞 | PM spec、mock、refs | 名詞 / 動詞 / 角色詞各一表,每詞記來源段落與歸類 | 每個詞都能回到 PM§ 或 mock 錨點 | 把「部門主管」這種需求來源當 Actor |
| SA2 實體與關係 | SA1 名詞 | 去重、合併同義、剔除屬性詞;關係寫 來源-關係-目標-多重性;classDiagram | 屬性詞(理由、工作天)不建實體;每個實體有英文名(survey 用) | 把狀態值(待審核)建成實體 |
| SA3 角色、動作、流程 | SA1 動詞、角色詞 | 每個 Actor 的動作清單,動作串流程,對應 REQ | 動作用 PascalCase 動詞開頭(survey 用),括號內可寫 HTTP 路徑 | 系統排程不算 Actor(其實算:System) |
| SA4 Use Case Diagram | SA3 | Actor–UseCase;mermaid 無原生 usecase,用 flowchart LR | 每個 REQ 至少被一個 UseCase 覆蓋 | 把 UseCase 畫成功能選單 |
| SA5 Activity Diagram | SA3 流程 | 每條主要流程一張;分支、迴圈 | 分支條件寫得出來(理由 ≥ 10 字) | 畫成 UI 操作流水帳 |
| SA6 Sequence Diagram | SA3、docs 架構 | 系統層級(Web / API / DB / 外部),**不到 Component** | 例外用 alt | 提早畫 Handler / Repository |
| SA7 State Diagram | SA2 有生命週期的實體 | 一實體一張;事件、守衛 | 狀態是 SA2 實體的屬性;依 guidelines 狀態機放 Domain | 把 UI 狀態(loading)畫進來 |

## 交接到 S1/S2

| SA 產物 | 進到 | 怎麼用 |
|---|---|---|
| SA2 實體 | `20-domain-model.md` 領域模型表 | 候選 Entity / VO;Aggregate 判準仍是 M5 |
| SA3 角色動作 | `20-domain-model.md` UC-xxx | 一個動作 ≈ 一個 UC;流程 → 主流程步驟 |
| SA7 狀態 | `20-domain-model.md` STM-DOM-xxx | 直接沿用,補守衛與動作 |
| SA6 | `30-architecture-c4.md` SEQ-xxx | 把系統邊界展開成 Component |
| survey existing / modify / new | `30-architecture-c4.md` Component 表 | existing 沿用名稱;modify 標「既有修改」;new 才是新 Component |

## Survey Mapping

`analyze.survey` 讀 SA2 的英文名與 SA3 的動作詞,掃 `survey.code_roots` 下的檔案,每個元素最多 N 個候選(`survey-candidates.md`,產生物)。人/LLM 定案 `survey-mapping.md`:

| 狀態 | 意義 | 證據要求 |
|---|---|---|
| existing | 沿用不改 | `path:line`,該行含元素符號 |
| modify | 既有要改 | 同上,說明欄寫改什麼 |
| new | 不存在 | 不填證據;若候選表有強命中 → WARN,要你確認 |

G-SV-evidence 會真的打開檔案、讀那一行、比對符號。證據錯一個字就 FAIL,這是刻意的:survey 的價值就在「能回溯」。
