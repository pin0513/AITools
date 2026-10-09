---
name: sa-modeling
description: SA 建模階段的方法論 A(uml-wordbreak)人讀說明:七步各自的輸入、方法、判準與常見錯誤;資料版在 rules/methodology/sa/uml-wordbreak.yaml
---

# SA 建模:方法論 A(UML word-break)

目的:在寫 RD spec 之前,先把 PM 素材變成一組**可核對的模型**(實體、角色、流程、狀態),讓後面的 Component 設計有依據,也讓 survey 有東西可以對回 codebase。方法論可抽換:`config.sa_modeling.methodology` 指到 `rules/methodology/sa/` 下另一個 YAML 即可;pipeline 的 SA stage 產出清單由該 YAML 的 `steps[*].output` 決定。

## SA0 前置解析(工具層,先於七步)

`analyze.lexicon` 在 SA stage 開始前自動執行(pipeline 的 `pre_tools`),產出 `spec-review/sa/00-lexicon.md` 與 `lexicon.json`。**SA1 之後 LLM 只讀這份,不讀整份 PM 原文與 codebase**。

| 步 | 做什麼 | 資料 |
|---|---|---|
| 斷詞 | 中文:在功能字(的、或、與…)切開 → 2–5 字 n-gram → 邊界熵濾碎片(左/右鄰字唯一且延伸詞同頻者丟)→ 去冗。英文:`[A-Za-z][A-Za-z0-9_]{2,}` | `rules/methodology/sa/lexicon-zh.yaml` |
| 分類 | 狀態值(待/已/未/可 + 動詞)→ 角色(者/員/主管/系統…結尾,摺疊「提醒審核者」這類片語)→ 動作(整詞是動詞或以動詞結尾)→ 其他為名詞 | 同上 |
| 重要性 | 詞頻 × 章節權重(功能需求 3、驗收 2…)× 文件權重(PM/mock 1、參考 0.4) | 同上 |
| glossary-mapping | 名詞對專案詞彙表取符號;有符號者掃 codebase 取命中數與第一個位置 | `specs/glossary.md`、`survey.code_roots` |
| 升/降 | 有符號、或權重前 60% 且詞頻 ≥ 2 且出現在 PM/mock → 升;其餘降 | — |

實測(testcase1 issue-c,對照人工 SA1):CJK 候選 325 → 邊界熵 111 → 去冗 104;召回 名詞 5/6、動作 7/7、角色 4/4;狀態值 4/4 分類正確。

能力邊界:
- **這是候選產生器,不是分類器**。升級名詞裡仍有「紀錄」「填理由」這類非實體,要 LLM 在 SA1 剔除。
- **詞頻是先驗,不是重要性的結論**。「指派」只出現一次被降級,卻是缺口 #1 的核心。降級不等於丟棄;SA1 撿回降級詞要在歸類欄寫理由。
- 已知漏:「看待審清單」中的「待」被當切分字,「待審清單」切不出來。要更好的中文斷詞需裝 jieba / CKIP,會打破零相依,目前不做。

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

G-SV-evidence 會真的打開檔案、讀那一行、比對符號(或 `path:line "字面文字"` 的文字)。證據錯一個字就 FAIL,這是刻意的:survey 的價值就在「能回溯」。

### 能力邊界(要知道的)

| 它能抓 | 它抓不到 | 怎麼補 |
|---|---|---|
| 宣稱 existing/modify 卻沒附檔案與行號 | — | — |
| 行號指錯行(那行沒有該符號) | 行號對、符號在,但那個符號根本不是這個功能(代理指標 ≠ 結論) | 證據指到**行為所在行**並用 `"字面文字"` 鎖定(運算子清單裡的那一項,不是函式宣告) |
| 元素標 new 但 codebase 有同名候選 | 元素標 new 但 codebase 用別的名字實作了同一功能 | 看 `survey-candidates.md` 時把動作詞也掃進來(SA3 的動作欄) |
| — | 純中文元素名(無 ASCII 符號) | 寫成「中文 (CodeSymbol)」;否則 WARN 請人確認 |

結論:這條規則把「有沒有附證據」從人工審查裡拿掉,讓人只需要審「證據對不對」。它不取代讀碼。

### 中英文元素與跨 spec 詞彙表

| 元素寫法 | 符號怎麼來 | 結果 |
|---|---|---|
| `FormSubmission` | 元素名本身的 ASCII 符號 | 驗 |
| `填寫紀錄 (FormSubmission)` | 括號內符號 | 驗 |
| `填寫紀錄` | 專案詞彙表 `specs/glossary.md`(名詞 → 符號)→ 本 spec SA2 實體表(實體 → 英文) | 驗;都查不到 → WARN 請人確認 |
| 任何 + `path:line "字面文字"` | 不用符號,驗該行含字面文字 | 驗(最強,指到行為行) |

詞彙表由 `analyze.glossary` 從 `glossary.spec_roots` 下每個 `<issue>/spec` 抽取(00 名詞表的「名詞 (Symbol)」、SA2 實體表、survey 的「中文 (Symbol)」),合併後寫到 `glossary.path`;同名詞不同符號列入衝突表,`G-GL-consistency` 對本 spec 的 SA2 出 FAIL(同名詞不同符號)或 WARN(同符號不同名詞)。已完成的舊 spec 只要補一份 `00-overview.md` 名詞表(或 SA2)就能進詞彙表,不必整份回填。
