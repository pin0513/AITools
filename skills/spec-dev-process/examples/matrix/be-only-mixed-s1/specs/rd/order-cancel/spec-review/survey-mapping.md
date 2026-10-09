# Survey Mapping

## 對應表
| 模型元素 | 類型 | 狀態 | 對應 codebase | 證據 | 說明 |
|---|---|---|---|---|---|
| 訂單 (Order) | Aggregate | modify | Order | src/api/Orders.Domain/Order.cs:5 | |
| Shipped rule | Rule | existing | Order.Shipped | src/api/Orders.Domain/Order.cs:3 "Shipped" | |
| 退款單 (Refund) | Entity | new | Refund | | |
| GetOrder | Query | existing | GetOrderQueryHandler | src/api/Orders.Application/GetOrderQueryHandler.cs:8 | |
| CancelOrder | Command | new | CancelOrder | | |
| IssueRefund | Command | new | IssueRefund | | |
| ListCancellations | Query | new | ListCancellations | | |
| SqlOrderRepository | Adapter | modify | SqlOrderRepository | src/api/Orders.Infrastructure/SqlOrderRepository.cs:5 | |
| PaymentGatewayClient | Adapter | existing | PaymentGatewayClient | src/api/Orders.Infrastructure/PaymentGatewayClient.cs:5 | |
| OrdersController | Api | modify | OrdersController | src/api/Orders.Api/Controllers/OrdersController.cs:8 | |
