# CHANGELOG

> 原始碼在 git:`pin0513/aitools` 的 `skills/spec-dev-process/`(分支 `feat/pm-to-rd-spec-workflow`)。每版列出「要重驗什麼」,方便針對性重驗。
> 固定對照組(MAYOFORM-1818 去識別版)在 `tests/rules/cases/G-SV-evidence.yaml` 的 `control_*`,每次改版自動重跑。

## 2.8.0(2026-10-10)— 依使用回饋(v2.7.1):只要好核對,不卡人;各司其職

**收斂(要重驗)**:input 是 md、tools 給 AI 呼叫、rules 是 YAML、看板只給人看。
- 移除 `serve` 站台與提問串(`threads.md`、`G-RV-threads`);看板拿掉所有表單、瀏覽器暫存、指令產生器。
- 看板每個待確認事項附一行唯讀的工具呼叫;確認由 AI 呼叫 `spec-dev.py signoff --id … --duty … --hash … --by …`。


**UI 與 API 各自的顆粒度(新)**
- `ui/41`「畫面元素」表(按鈕 / 欄位 / 連結,元素寫 mock 的 `#id` 或 `name`);`api/40` 介面清單可選「呼叫者」欄。
- `G-UI-API`:元素 → endpoint 存在、AC 存在、有動作要有 AC、mock 可互動元素全列、表上元素 mock 找得到、endpoint 要有呼叫者。沒有畫面元素表就不核對。
- 看板「UI × API」分頁;testcase1 補 `ui/41-ui-spec.md`(抓到一個真實缺口:審核清單「載入待審清單」沒有 AC)。

**判定改變(要重驗)**
- `G-SV-evidence` 證據分強弱:字面鎖定且不在函式宣告行 = **強**(`verified`);只比對到名字 = **弱**(`verified_weak`,放行但看板標出);
  指在**函式 / 方法宣告行** = `decl_only` **WARN**「這一行只證明函式存在,不證明行為」(類別、資料表宣告不算)。
  同一列另有證據指在行為行且通過時,宣告行不再 WARN。→ 對照組 B 從「放行」變 WARN。
- 純中文元素名可經**分層命名對照表**、SA0 **lexicon** 自動對到符號(原本只有詞彙表、SA2)。→ 有對照時 D 與 F 同為 FAIL;沒有對照仍是 WARN。
- matrix 驗收的證據計數改數「已放行」(強 + 弱)。

**看板**
- 總覽最前面新增「已放行」:existing / modify 憑什麼放行、強弱、`existing／modify 只有弱證據:N` KPI。
- 靜態面板也能點「檔:行」看原文:追蹤中的文件內嵌全文,survey 引用的程式碼內嵌前後 6 行;不需要伺服器。

**CLI**
- `spec-dev.py signoff --id` 別名;誰都可以簽,名字只是紀錄;hash 鎖定看過的版本。
- `spec-dev.py review <dir> --watch`:md 一改就重建看板。

**維護**
- `install.sh` 不再 `rm -rf`:目標是實體資料夾就拒絕,`--force` 先備份成 `<目標>.bak-<時間>` 再覆蓋。
- 測試分組 `tests/run.py fast|slow|all`;安裝只跑快的(約 20 秒)。
- 本檔。

## 2.7.1(2026-10-09)
- 頁面語系 `zh-Hant-TW`;測試矩陣語言代碼 `zh` → `zh-TW`(案例資料夾 `*-zh-TW-*`)。**要重驗**:只影響矩陣資料夾名稱。

## 2.7.0(2026-10-09)— 文件版本追蹤進看板
- `review.versions`:文件 / 段落 / 需求上游鍵(`pm:REQ-x`、`req:REQ-x`)指紋,有變才記一版(`audit/versions.jsonl` + 內容定址 blob,不靠 git)。
- 確認記下版本;依據的上游之後變了 → 「上游已變,請重看」(G-DG-signoff WARN),點了直接開 diff。看板「版本」分頁。

## 2.6.0(2026-10-09)— spec-reviewer 子系統
- S6:自動圖(追溯圖、沿依賴的循序圖)、mermaid 解析、圖與表核對、審計(來源 / 過程 / 目標 / hash)、瀏覽器渲染驗證。
- 確認事項以事情區分(是不是要的 / 測得出來 / 做得出來),同一人可做多項,「不需要」附理由算做完。
- 看板分頁 + modal(圖與名詞表預設不展開)。(2.6.0 的 `serve` 站台與提問串已在 2.8.0 移除)

## 2.5.0(2026-10-09)
- 證據鏈每條需求都有圖;mermaid 可靠載入(jsDelivr → unpkg → 提示);名詞 / 已知資產查找;真瀏覽器測試。
- 每筆發現只印一次(stage 印計數、總表列明細、INFO 預設收起)。

## 2.4.0(2026-10-09)
- 測試矩陣(語言 × 情境 × 架構形狀,成對覆蓋 15 份)+ 突變驗收;RD spec 分層(核心 + ui/ + api/);分層命名對照表。

## 2.3.0(2026-10-09)
- SA0 前置解析:中英斷詞、詞頻 × 章節權重、glossary-mapping。

## 2.2.0(2026-10-09)
- survey 證據中英支援(中文元素名改 WARN 請人確認;`"字面文字"` 鎖定);跨 spec 詞彙表。

## 2.1.0(2026-10-09)
- SA 建模(可抽換方法論)+ survey mapping + testcase1 端到端;看板證據鏈。

## 2.0.0(2026-10-09)
- 四層架構:process / tools / rules / tests。
