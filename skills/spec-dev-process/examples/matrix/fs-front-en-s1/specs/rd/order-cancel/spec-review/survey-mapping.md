# Survey Mapping

## Mapping
| Element | Element Type | Status | Code Target | Evidence | Note |
|---|---|---|---|---|---|
| Order | Aggregate | modify | Order | src/api/Orders.Domain/Order.cs:5 | |
| Shipped rule | Rule | existing | Order.Shipped | src/api/Orders.Domain/Order.cs:3 "Shipped" | |
| Refund | Entity | new | Refund | | |
| GetOrder | Query | existing | GetOrderQueryHandler | src/api/Orders.Application/GetOrderQueryHandler.cs:8 | |
| CancelOrder | Command | new | CancelOrder | | |
| IssueRefund | Command | new | IssueRefund | | |
| ListCancellations | Query | new | ListCancellations | | |
| SqlOrderRepository | Adapter | modify | SqlOrderRepository | src/api/Orders.Infrastructure/SqlOrderRepository.cs:5 | |
| PaymentGatewayClient | Adapter | existing | PaymentGatewayClient | src/api/Orders.Infrastructure/PaymentGatewayClient.cs:5 | |
| OrdersController | Api | modify | OrdersController | src/api/Orders.Api/Controllers/OrdersController.cs:8 | |
| OrderDetailPage | Page | modify | OrderDetailPage | src/web/src/pages/OrderDetailPage.tsx:3 | |
| Order type | Type | existing | Order | src/web/src/types/Order.ts:4 | |
