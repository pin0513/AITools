# 分層命名對照表(跨 spec)

<!-- 由 analyze.glossary 產生,不手改。要修正某格,寫在 specs/naming-overrides.md(同欄位,有值的格子覆蓋這裡)-->

## 分層命名對照

| 名詞 | 符號 | UI | API | Application | Domain | Infrastructure | DB | 來源 spec |
|---|---|---|---|---|---|---|---|---|
| cancel | CancelOrder | CancelOrderDialog | POST /orders/{id}/cancel |  |  |  |  | order-cancel |
| GetOrder | GetOrder | getOrder |  |  |  |  |  | order-cancel |
| refund | IssueRefund |  | POST /orders/{id}/refund |  |  |  |  | order-cancel |
| view | ListCancellations |  | GET /orders/cancellations |  |  |  |  | order-cancel |
| order | Order | OrderDetailPage, CancelOrderDialog, orderStore, ordersApi, Order |  |  |  |  |  | order-cancel |
| OrderDetailPage | OrderDetailPage | OrderDetailPage |  |  |  |  |  | order-cancel |
| refund | Refund |  |  |  |  |  |  | order-cancel |
| Shipped rule | Shipped | Shipped |  |  |  |  |  | order-cancel |
