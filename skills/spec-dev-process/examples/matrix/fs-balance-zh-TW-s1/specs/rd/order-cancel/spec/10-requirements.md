# 訂單取消與退款 — requirements

## 需求清單
| ID | 需求 | 型態 | 來源錨點 | AC |
|---|---|---|---|---|
| REQ-001 | 顧客可在出貨前取消訂單 | functional, state_heavy | PM§3.1 | AC-001-1, AC-001-2 |
| REQ-002 | 取消後系統經付款閘道退款 | functional, integration | PM§3.2 | AC-002-1, AC-002-2 |
| REQ-003 | 客服人員可查看取消紀錄 | functional | PM§3.3 | AC-003-1 |

## 驗收條件
```gherkin
# AC-001-1
Given 訂單狀態為已下單
When 顧客取消訂單
Then 訂單狀態為已取消

# AC-001-2
Given 訂單狀態為已出貨
When 顧客取消訂單
Then 回應 409 ORDER_SHIPPED,狀態不變

# AC-002-1
Given 訂單已取消且已付款
When 系統退款
Then 呼叫付款閘道,訂單狀態為已退款

# AC-002-2
Given 付款閘道逾時
When 系統退款
Then 重試 3 次,訂單維持已取消

# AC-003-1
Given 有訂單已取消
When 客服人員開啟紀錄
Then 每列顯示訂單、時間與原因

```

## 非功能需求
| ID | 刺激 | 來源 | 環境 | 產物 | 回應 | 量測 | 綁定 CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | 95% 的訂單在取消後 5 分鐘內完成退款。 | user | normal load | API-002 | ok | P95 < 5 min | API-002 | AC-N01-1 |

## 缺口(待 PM 確認)
| # | 問題 | 影響 REQ | 暫時假設 |
|---|---|---|---|
