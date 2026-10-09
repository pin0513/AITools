---
name: method-log-notation
description: 方法論 log 的儲存格式(JSONL)與面板單行表示法;每一次需求轉換都要留一筆,面板預設隱藏
---

# 方法論 Log 表示法

目的:讓每一條 RD spec 內容都能回答「這是用什麼方法、從哪一段 PM spec 推出來的、推得多有把握、還缺什麼」。

## 儲存格式:`method-log.jsonl`

一行一筆 JSON,append-only,不得改寫舊行;修正用新行 + `supersedes`。

```json
{"seq":1,"req":"REQ-002","stage":"S1","method":"UseCase","rule":"M1","in":"PM§3.2","out":"UC-002","evidence":"explicit","gaps":[],"note":""}
{"seq":2,"req":"REQ-002","stage":"S2","method":"UML.Sequence","rule":"M4","in":"UC-002","out":"SEQ-002","evidence":"assumed","gaps":["重試次數未定義"],"note":"假設 3 次,待 PM 確認"}
{"seq":3,"req":"*","stage":"S3","method":"Spike.ImageSharp","rule":"B8","in":"CMP-005","out":"OPEN","evidence":"explicit","gaps":["授權是否符合商用"],"note":"time-box 1 天;結案時 out 寫 PASS/採用"}
{"seq":4,"req":"REQ-002","stage":"S2","method":"UML.Sequence","rule":"M4","in":"UC-002","out":"SEQ-002","evidence":"explicit","gaps":[],"note":"PM 確認重試 3 次","supersedes":2}
```

| 欄位 | 必填 | 說明 |
|---|---|---|
| `seq` | 是 | 單調遞增整數 |
| `req` | 是 | 需求 ID;跨需求的架構決策用 `"*"` |
| `stage` | 是 | S0–S6 |
| `method` | 是 | 方法論名稱,命名空間用 `.` 分隔(`UML.Sequence`、`DDD.Aggregate`、`Boundary.B2`) |
| `rule` | 是 | 路由表或邊界規則的 id(M1–M17、B1–B8) |
| `in` | 是 | 輸入錨點:`PM§3.2`、`UC-002`、`CMP-004`、`mock/avatar.html#state-2` |
| `out` | 是 | 輸出錨點:`SEQ-002`;Spike 用 `OPEN` / `PASS` |
| `evidence` | 是 | `explicit`(PM 明寫)/ `inferred`(由既有規範、平台、團隊慣例推得,note 寫依據)/ `assumed`(自行假設,**必須同時列入 10-requirements 缺口表**)。不用數字:自評的 0.8 無法校準,枚舉可以查 |
| `gaps` | 是 | 字串陣列;非空代表要回問 PM 或需 Spike |
| `note` | 否 | 假設、決策理由 |
| `supersedes` | 否 | 被取代的 `seq` |

## 面板單行表示法

面板 D 區把每筆 JSONL 渲染成一行,格式固定,方便肉眼掃與 grep:

```
[REQ-002] S1 UseCase        PM§3.2  → UC-002   rule=M1  ev=explicit
[REQ-002] S2 UML.Sequence   UC-002  → SEQ-002  rule=M4  ev=assumed   gap="重試次數未定義"
[*]       S3 Spike.ImageSharp CMP-005 → OPEN   rule=B8  ev=explicit  gap="授權是否符合商用"
```

規則:
- 被 `supersedes` 取代的行以刪除線顯示,不刪除。
- `ev=assumed` 黃底;`out` 為 `FAIL` 紅底;`gaps` 非空在行尾加 `gap="..."`。
- **S3 的 B1–B8 不寫 log**:那是 `spec-dev.py check` 算的,寫進 `boundary-report.md`。log 只記 LLM 的判斷(型態判定、方法論套用、Spike)。
- 預設整區收合(`<details>` 未展開);展開後可依 `req`、`stage`、`rule` 篩選。

## 面板用 log 做的三個檢查

| 檢查 | 條件 | 面板表現 |
|---|---|---|
| 無方法論需求 | 某 REQ 在 S1/S2 的 log 筆數 = 0 | Gate FAIL,矩陣該列標 FAIL,KPI「未覆蓋 REQ」+1 |
| 假設未經確認 | 任一筆 `evidence=assumed` 未被 supersedes | Gate WARN,該 REQ 列標 WARN;KPI 顯示 assumed 數 |
| Spike 未結案 | `method=Spike.*` 且 `out` 不是 PASS/採用 | B8 對該 CMP 出 WARN |
