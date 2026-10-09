# 訂單取消與退款 — API spec

## 介面清單
| ID | Method | Path | Request | Response | 對應 REQ | 綁定 NFR | CMP |
|---|---|---|---|---|---|---|---|
| API-001 | POST | /orders/{id}/cancel | json | 200 | REQ-001 |  | CMP-001 |
| API-002 | POST | /orders/{id}/refund | json | 200 | REQ-002 | NFR-001 | CMP-001 |
| API-003 | GET | /orders/cancellations | json | 200 | REQ-003 |  | CMP-001 |

## 外部依賴與失敗模式
| 外部系統 | 呼叫點 CMP | 逾時 | 重試 | 降級 | 補償 |
|---|---|---|---|---|---|
| PaymentGateway | CMP-007 | 5s | 3 | 503 | retry next run |
