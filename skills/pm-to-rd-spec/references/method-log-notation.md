---
name: method-log-notation
description: 方法論 log 的儲存格式(JSONL)與面板單行表示法;每一次需求轉換都要留一筆,面板預設隱藏
---

# 方法論 Log 表示法

目的:讓每一條 RD spec 內容都能回答「這是用什麼方法、從哪一段 PM spec 推出來的、推得多有把握、還缺什麼」。

## 儲存格式:`method-log.jsonl`

一行一筆 JSON,append-only,不得改寫舊行;修正用新行 + `supersedes`。

```json
{"seq":1,"req":"REQ-002","stage":"S1","method":"UseCase","rule":"M1","in":"PM§3.2","out":"UC-002","confidence":0.9,"gaps":[],"note":""}
{"seq":2,"req":"REQ-002","stage":"S2","method":"UML.Sequence","rule":"M4","in":"UC-002","out":"SEQ-002","confidence":0.8,"gaps":["重試次數未定義"],"note":"假設 3 次,待 PM 確認"}
{"seq":3,"req":"REQ-002","stage":"S3","method":"Boundary.B4","rule":"B4","in":"CMP-004","out":"PASS","confidence":1.0,"gaps":[],"note":"BlobAdapter 在 Infrastructure"}
{"seq":4,"req":"REQ-002","stage":"S2","method":"UML.Sequence","rule":"M4","in":"UC-002","out":"SEQ-002","confidence":0.95,"gaps":[],"note":"PM 確認重試 3 次","supersedes":2}
```

| 欄位 | 必填 | 說明 |
|---|---|---|
| `seq` | 是 | 單調遞增整數 |
| `req` | 是 | 需求 ID;跨需求的架構決策用 `"*"` |
| `stage` | 是 | S0–S6 |
| `method` | 是 | 方法論名稱,命名空間用 `.` 分隔(`UML.Sequence`、`DDD.Aggregate`、`Boundary.B2`) |
| `rule` | 是 | 路由表或邊界規則的 id(M1–M17、B1–B8) |
| `in` | 是 | 輸入錨點:`PM§3.2`、`UC-002`、`CMP-004`、`mock/avatar.html#state-2` |
| `out` | 是 | 輸出錨點或核對結果:`SEQ-002`、`PASS`、`WARN`、`FAIL` |
| `confidence` | 是 | 0–1;< 0.7 面板以黃底標示 |
| `gaps` | 是 | 字串陣列;非空代表要回問 PM 或需 Spike |
| `note` | 否 | 假設、決策理由 |
| `supersedes` | 否 | 被取代的 `seq` |

## 面板單行表示法

面板 D 區把每筆 JSONL 渲染成一行,格式固定,方便肉眼掃與 grep:

```
[REQ-002] S1 UseCase        PM§3.2  → UC-002   rule=M1  conf=0.90
[REQ-002] S2 UML.Sequence   UC-002  → SEQ-002  rule=M4  conf=0.80  gap="重試次數未定義"
[REQ-002] S3 Boundary.B4    CMP-004 → PASS     rule=B4  conf=1.00  "BlobAdapter 在 Infrastructure"
```

規則:
- 被 `supersedes` 取代的行以刪除線顯示,不刪除。
- `conf < 0.7` 黃底;`out` 為 `FAIL` 紅底;`gaps` 非空在行尾加 `gap="..."`。
- 預設整區收合(`<details>` 未展開);展開後可依 `req`、`stage`、`rule` 篩選。

## 面板用 log 做的三個檢查

| 檢查 | 條件 | 面板表現 |
|---|---|---|
| 無方法論需求 | 某 REQ 在 S1/S2 的 log 筆數 = 0 | 矩陣該列整列標 FAIL,KPI「未覆蓋 REQ」+1 |
| 低信心設計 | 任一筆 `confidence < 0.7` 且未被 supersedes | 該 REQ 列前加 ⚠ |
| 待確認缺口 | 任一筆 `gaps` 非空且未被 supersedes | 摘要列出「待 PM 確認 N 項」,點開列出 gaps |
