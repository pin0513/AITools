# 訂單取消與退款 — requirements

## 需求清單
| ID | 需求 | 型態 | 來源錨點 | AC |
|---|---|---|---|---|
| REQ-001 | customer 可在出貨前 cancel Order | functional, state_heavy | PM§3.1 | AC-001-1, AC-001-2 |
| REQ-002 | cancel 後 system 經 PaymentGateway refund | functional, integration | PM§3.2 | AC-002-1, AC-002-2 |
| REQ-003 | support agent 可 view cancel 紀錄 | functional | PM§3.3 | AC-003-1 |

## 驗收條件
```gherkin
# AC-001-1
Given Order 狀態為 Placed
When customer cancel Order
Then Order 狀態為 Cancelled

# AC-001-2
Given Order 狀態為 Shipped
When customer cancel Order
Then 回應 409 ORDER_SHIPPED,狀態不變

# AC-002-1
Given Order 已 cancel 且已付款
When system refund
Then 呼叫 PaymentGateway, Order 狀態為 Refunded

# AC-002-2
Given PaymentGateway 逾時
When system refund
Then 重試 3 次, Order 維持 Cancelled

# AC-003-1
Given 有 Order 已 cancel
When support agent 開啟紀錄
Then 每列顯示 Order、時間與原因

```

## 非功能需求
| ID | 刺激 | 來源 | 環境 | 產物 | 回應 | 量測 | 綁定 CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | 95% 的 Order 在 cancel 後 5 分鐘內完成 refund。 | user | normal load | API-002 | ok | P95 < 5 min | API-002 | AC-N01-1 |

## 缺口(待 PM 確認)
| # | 問題 | 影響 REQ | 暫時假設 |
|---|---|---|---|
