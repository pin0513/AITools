# order-cancel SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)

來源:pm_spec:pm-spec.md, mock:order.html, ref:refs.md · CJK 候選 246 → 邊界熵後 78 → 去冗後 78

規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。

## 名詞候選

| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |
|---|---|---|---|---|---|---|
| 訂單 | 23 | 36.0 | Order | 5 (src/api/Orders.Infrastructure/SqlOrderRepository.cs:7) | 升 | mock:order.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 顧客可在出貨前取 |
| 狀態 | 8 | 13.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 顧客可在出貨前取 pm_spec:pm-spec.md§3.2 取消後系統經付款 pm_spec:pm-spec.md§5 驗收條件 |
| 訂單狀態 | 7 | 11.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 顧客可在出貨前取 pm_spec:pm-spec.md§3.2 取消後系統經付款 pm_spec:pm-spec.md§5 驗收條件 |
| 顧客 | 6 | 9.0 |  | — | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 顧客可在出貨前取 pm_spec:pm-spec.md§5 驗收條件 |
| 取消訂單 | 5 | 8.0 |  | — | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 顧客可在出貨前取 pm_spec:pm-spec.md§5 驗收條件 |
| 付款閘道 | 5 | 7.0 | PaymentGateway | 0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§3.2 取消後系統經付款 pm_spec:pm-spec.md§5 驗收條件 |
| 客服 | 4 | 6.0 |  | — | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 客服人員可查看取 pm_spec:pm-spec.md§5 驗收條件 |
| 紀錄 | 3 | 5.0 |  | — | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 客服人員可查看取 pm_spec:pm-spec.md§5 驗收條件 |
| 客取消訂單 | 2 | 4.0 |  | — | 升 | pm_spec:pm-spec.md§5 驗收條件 |
| 顧客取消訂 | 2 | 4.0 |  | — | 降 | pm_spec:pm-spec.md§5 驗收條件 |
| 原因 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.3 客服人員可查看取 pm_spec:pm-spec.md§5 驗收條件 |
| 取消紀錄 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 客服人員可查看取 |
| 訂單維持 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 取消後系統經付款 pm_spec:pm-spec.md§5 驗收條件 |
| 重試 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 取消後系統經付款 pm_spec:pm-spec.md§5 驗收條件 |
| 訂單狀態改 | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 顧客可在出貨前取 pm_spec:pm-spec.md§3.2 取消後系統經付款 |
| order | 1 | 2.0 | Order | 5 (src/api/Orders.Infrastructure/SqlOrderRepository.cs:7) | 升 | pm_spec:pm-spec.md§5 驗收條件 |

## 動作候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| 取消 | 19 | 29.0 | 升 | mock:order.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 顧客可在出貨前取 |
| 退款 | 9 | 15.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 取消後系統經付款 pm_spec:pm-spec.md§4 非功能需求 |
| 付款 | 6 | 9.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§3.2 取消後系統經付款 pm_spec:pm-spec.md§5 驗收條件 |
| 查看 | 3 | 4.0 | 升 | mock:order.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 客服人員可查看取 |
| 系統退款 | 2 | 4.0 | 升 | pm_spec:pm-spec.md§5 驗收條件 |
| 出貨 | 2 | 3.0 | 升 | pm_spec:pm-spec.md§3.1 顧客可在出貨前取 pm_spec:pm-spec.md§5 驗收條件 |
| 完成退款 | 1 | 3.0 | 降 | pm_spec:pm-spec.md§4 非功能需求 |
| 想快速取消 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 |
| 負責退款 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 |
| 以查看 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.3 客服人員可查看取 |
| 客自助取消 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |
| 款閘道退款 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.2 取消後系統經付款 |
| 系統經付款 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |
| 統透過付款 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.2 取消後系統經付款 |
| 道自動退款 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |

## 角色候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| 系統 | 6 | 9.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 取消後系統經付款 pm_spec:pm-spec.md§5 驗收條件 |
| 客服人員 | 3 | 5.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 客服人員可查看取 pm_spec:pm-spec.md§5 驗收條件 |

## 狀態值候選(屬性,不建實體)

| 詞 | 詞頻 | 出現 |
|---|---|---|
| 已下單 | 2 | pm_spec:pm-spec.md§3.1 顧客可在出貨前取 pm_spec:pm-spec.md§5 驗收條件 |
| 已取消 | 2 | pm_spec:pm-spec.md§3.1 顧客可在出貨前取 pm_spec:pm-spec.md§5 驗收條件 |
| 已退款 | 2 | pm_spec:pm-spec.md§3.2 取消後系統經付款 pm_spec:pm-spec.md§5 驗收條件 |
| shipped | 1 | pm_spec:pm-spec.md§5 驗收條件 |
| 已付款 | 1 | pm_spec:pm-spec.md§5 驗收條件 |
| 已出貨 | 1 | pm_spec:pm-spec.md§5 驗收條件 |
| placed | 1 | mock:order.html |
| 可取消 | 1 | pm_spec:pm-spec.md§3.1 顧客可在出貨前取 |

## 英文符號

| 符號 | 詞頻 | codebase 命中 | 出現 |
|---|---|---|---|
| ORDER_SHIPPED | 1 | 0 | pm_spec:pm-spec.md |
| Placed | 1 | 3 (src/api/Orders.Domain/Order.cs:3) | mock:order.html |
| mock | 1 | 0 | mock:order.html |
| status | 1 | 2 (src/api/Orders.Domain/Order.cs:8) | mock:order.html |
| shape | 1 | 0 | ref:refs.md |
