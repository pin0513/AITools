# 訂單取消與退款 (PM spec)

## 1 背景與目標
目前 customer 要 cancel Order 必須打電話給客服。目標: customer 自助 cancel,並由 system 經 PaymentGateway 自動 refund。

## 2 使用者與情境
customer:想快速 cancel Order。 support agent:需要 view cancel 紀錄。 system:負責 refund。

## 3 功能需求
### 3.1 customer 可在出貨前 cancel Order
customer 可以在 Order 狀態為 Placed 時 cancel Order。 Order 一旦 Shipped 就不可 cancel。 cancel 後 Order 狀態改為 Cancelled。

### 3.2 cancel 後 system 經 PaymentGateway refund
Order Cancelled 後, system 透過 PaymentGateway refund。 PaymentGateway 失敗時 system 最多重試 3 次, Order 維持 Cancelled。 refund 成功後 Order 狀態改為 Refunded。

### 3.3 support agent 可 view cancel 紀錄
support agent 可以 view 每筆 Order 的 cancel 紀錄,包含時間與原因。

## 4 非功能需求
95% 的 Order 在 cancel 後 5 分鐘內完成 refund。

## 5 驗收條件
- Order 狀態為 Placed → customer cancel Order → Order 狀態為 Cancelled
- Order 狀態為 Shipped → customer cancel Order → 回應 409 ORDER_SHIPPED,狀態不變
- Order 已 cancel 且已付款 → system refund → 呼叫 PaymentGateway, Order 狀態為 Refunded
- PaymentGateway 逾時 → system refund → 重試 3 次, Order 維持 Cancelled
- 有 Order 已 cancel → support agent 開啟紀錄 → 每列顯示 Order、時間與原因
