# 分層命名對照表(跨 spec)

<!-- 由 analyze.glossary 產生,不手改。要修正某格,寫在 specs/naming-overrides.md(同欄位,有值的格子覆蓋這裡)-->

## 分層命名對照

| 名詞 | 符號 | UI | API | Application | Domain | Infrastructure | DB | 來源 spec |
|---|---|---|---|---|---|---|---|---|
| cancel | CancelOrder | CancelOrderDialog | POST /orders/{id}/cancel | CancelOrderCommandHandler |  |  |  | order-cancel |
| GetOrder | GetOrder |  |  | GetOrderQueryHandler |  |  |  | order-cancel |
| refund | IssueRefund |  | POST /orders/{id}/refund | IssueRefundCommandHandler |  |  |  | order-cancel |
| view | ListCancellations |  | GET /orders/cancellations | ListCancellationsQueryHandler |  |  |  | order-cancel |
| order | Order | OrderDetailPage, CancelOrderDialog, orderStore, ordersApi, Order | OrdersController | CancelOrderCommandHandler | Order | SqlOrderRepository | Orders | order-cancel |
| OrderDetailPage | OrderDetailPage | OrderDetailPage |  |  |  |  |  | order-cancel |
| OrdersController | OrdersController |  | OrdersController |  |  |  |  | order-cancel |
| PaymentGatewayClient | PaymentGatewayClient |  |  |  |  | PaymentGatewayClient |  | order-cancel |
| refund | Refund |  |  | IssueRefundCommandHandler |  |  | Refund | order-cancel |
| Shipped rule | Shipped |  |  |  | Shipped |  |  | order-cancel |
| SqlOrderRepository | SqlOrderRepository |  |  |  |  | SqlOrderRepository |  | order-cancel |
