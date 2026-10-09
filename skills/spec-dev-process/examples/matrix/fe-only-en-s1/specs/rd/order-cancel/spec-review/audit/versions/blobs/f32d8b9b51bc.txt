# SA3 Roles and Actions

## Roles and Actions
| Role | Action | Flow | REQ |
|---|---|---|---|
| customer | CancelOrder(POST /orders/{id}/cancel) | cancel | REQ-001 |
| system | IssueRefund(POST /orders/{id}/refund) | refund | REQ-002 |
| support agent | ListCancellations(GET /orders/cancellations) | view | REQ-003 |
