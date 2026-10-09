# SA3 角色與動作

## 角色與動作
| 角色 | 動作 | 流程 | 對應 REQ |
|---|---|---|---|
| customer | CancelOrder(POST /orders/{id}/cancel) | cancel | REQ-001 |
| system | IssueRefund(POST /orders/{id}/refund) | refund | REQ-002 |
| support agent | ListCancellations(GET /orders/cancellations) | view | REQ-003 |
