# SA3 角色與動作

## 角色與動作
| 角色 | 動作 | 流程 | 對應 REQ |
|---|---|---|---|
| 顧客 | CancelOrder(POST /orders/{id}/cancel) | 取消 | REQ-001 |
| 系統 | IssueRefund(POST /orders/{id}/refund) | 退款 | REQ-002 |
| 客服人員 | ListCancellations(GET /orders/cancellations) | 查看 | REQ-003 |
