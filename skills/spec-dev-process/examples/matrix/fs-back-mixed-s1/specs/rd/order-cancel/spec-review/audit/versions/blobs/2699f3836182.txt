# order-cancel SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)

來源:pm_spec:pm-spec.md, mock:order.html, ref:refs.md · CJK 候選 44 → 邊界熵後 23 → 去冗後 23

規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。

## 名詞候選

| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |
|---|---|---|---|---|---|---|
| order | 24 | 38.0 | Order | 5 (src/api/Orders.Infrastructure/SqlOrderRepository.cs:7) | 升 | mock:order.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 customer |
| 狀態 | 8 | 13.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 customer pm_spec:pm-spec.md§3.2 cancel 後 pm_spec:pm-spec.md§5 驗收條件 |
| paymentgateway | 5 | 7.0 | PaymentGateway | 0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§3.2 cancel 後 pm_spec:pm-spec.md§5 驗收條件 |
| order order | 3 | 5.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 customer pm_spec:pm-spec.md§5 驗收條件 |
| 紀錄 | 3 | 5.0 |  | — | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 support  pm_spec:pm-spec.md§5 驗收條件 |
| 原因 | 2 | 3.0 |  | — | 升 | pm_spec:pm-spec.md§3.3 support  pm_spec:pm-spec.md§5 驗收條件 |
| 維持 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 cancel 後 pm_spec:pm-spec.md§5 驗收條件 |
| 重試 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 cancel 後 pm_spec:pm-spec.md§5 驗收條件 |
| system paymentgateway | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§3.2 cancel 後 |
| 狀態改 | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 customer pm_spec:pm-spec.md§3.2 cancel 後 |

## 動作候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| cancel | 14 | 22.0 | 升 | mock:order.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 customer |
| refund | 7 | 12.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 cancel 後 pm_spec:pm-spec.md§4 非功能需求 |
| view | 3 | 4.0 | 降 | mock:order.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 support  |
| 列顯示 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§5 驗收條件 |

## 角色候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| customer | 6 | 9.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 customer pm_spec:pm-spec.md§5 驗收條件 |
| system | 6 | 9.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 cancel 後 pm_spec:pm-spec.md§5 驗收條件 |
| support agent | 3 | 5.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 support  pm_spec:pm-spec.md§5 驗收條件 |

## 狀態值候選(屬性,不建實體)

| 詞 | 詞頻 | 出現 |
|---|---|---|
| cancelled | 5 | pm_spec:pm-spec.md§3.1 customer pm_spec:pm-spec.md§3.2 cancel 後 pm_spec:pm-spec.md§5 驗收條件 |
| shipped | 3 | pm_spec:pm-spec.md§3.1 customer pm_spec:pm-spec.md§5 驗收條件 |
| placed | 3 | mock:order.html pm_spec:pm-spec.md§3.1 customer pm_spec:pm-spec.md§5 驗收條件 |
| refunded | 2 | pm_spec:pm-spec.md§3.2 cancel 後 pm_spec:pm-spec.md§5 驗收條件 |
| 已付款 | 1 | pm_spec:pm-spec.md§5 驗收條件 |

## 英文符號

| 符號 | 詞頻 | codebase 命中 | 出現 |
|---|---|---|---|
| Order | 23 | 5 (src/api/Orders.Infrastructure/SqlOrderRepository.cs:7) | mock:order.html pm_spec:pm-spec.md |
| cancel | 14 | 0 | mock:order.html pm_spec:pm-spec.md |
| refund | 7 | 0 | pm_spec:pm-spec.md |
| customer | 6 | 0 | pm_spec:pm-spec.md |
| system | 6 | 0 | pm_spec:pm-spec.md |
| Cancelled | 5 | 0 | pm_spec:pm-spec.md |
| PaymentGateway | 5 | 0 | pm_spec:pm-spec.md |
| agent | 3 | 0 | pm_spec:pm-spec.md |
| support | 3 | 0 | pm_spec:pm-spec.md |
| Placed | 3 | 3 (src/api/Orders.Domain/Order.cs:3) | mock:order.html pm_spec:pm-spec.md |
| view | 3 | 0 | mock:order.html pm_spec:pm-spec.md |
| Refunded | 2 | 0 | pm_spec:pm-spec.md |
| Shipped | 2 | 3 (src/database/001_orders.sql:4) | pm_spec:pm-spec.md |
| ORDER_SHIPPED | 1 | 0 | pm_spec:pm-spec.md |
| mock | 1 | 0 | mock:order.html |
| status | 1 | 2 (src/api/Orders.Domain/Order.cs:8) | mock:order.html |
| shape | 1 | 0 | ref:refs.md |
