# Survey 候選(由 analyze.survey 產生,不手改;定案寫 survey-mapping.md)

| 模型元素 | 候選檔案 | 行 | 片段 |
|---|---|---|---|
| Order | src/api/Orders.Infrastructure/SqlOrderRepository.cs | 7 | `public Task<Order?> GetAsync(Guid id, CancellationToken ct) => Task.FromResult<Order?>(null);` |
| Order | src/api/Orders.Application/GetOrderQueryHandler.cs | 6 | `public sealed record GetOrderQuery(Guid Id) : IRequest<Order?>;` |
| Order | src/api/Orders.Application/GetOrderQueryHandler.cs | 8 | `public sealed class GetOrderQueryHandler(IOrderRepository repo) : IRequestHandler<GetOrderQuery, Ord` |
| Order | src/api/Orders.Application/GetOrderQueryHandler.cs | 10 | `public Task<Order?> Handle(GetOrderQuery q, CancellationToken ct) => repo.GetAsync(q.Id, ct);` |
| Order | src/api/Orders.Domain/Order.cs | 5 | `public sealed class Order` |
| Refund | (無) | | |
| CancelOrder | (無) | | |
| IssueRefund | (無) | | |
| ListCancellations | (無) | | |
| 訂單 → Order/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi/OrdersController/CancelOrderCommandHandler/SqlOrderRepository/Orders | src/database/001_orders.sql | 2 | `CREATE TABLE Orders (` |
| 訂單 → Order/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi/OrdersController/CancelOrderCommandHandler/SqlOrderRepository/Orders | src/api/Orders.Infrastructure/PaymentGatewayClient.cs | 1 | `namespace Orders.Infrastructure;` |
| 訂單 → Order/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi/OrdersController/CancelOrderCommandHandler/SqlOrderRepository/Orders | src/api/Orders.Infrastructure/SqlOrderRepository.cs | 1 | `using Orders.Domain;` |
| 訂單 → Order/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi/OrdersController/CancelOrderCommandHandler/SqlOrderRepository/Orders | src/api/Orders.Infrastructure/SqlOrderRepository.cs | 3 | `namespace Orders.Infrastructure;` |
| 訂單 → Order/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi/OrdersController/CancelOrderCommandHandler/SqlOrderRepository/Orders | src/api/Orders.Infrastructure/SqlOrderRepository.cs | 5 | `public sealed class SqlOrderRepository : IOrderRepository` |
| Shipped rule | src/database/001_orders.sql | 4 | `Shipped nvarchar(50) NOT NULL` |
| Shipped rule | src/api/Orders.Domain/Order.cs | 3 | `public enum OrderStatus { Placed, Shipped }` |
| Shipped rule | src/web/src/types/Order.ts | 2 | `export type OrderStatus = 'Placed' ¦ 'Shipped';` |
| 退款單 → Refund/IssueRefundCommandHandler | (無) | | |
| GetOrder → GetOrder/GetOrderQueryHandler | src/api/Orders.Application/GetOrderQueryHandler.cs | 8 | `public sealed class GetOrderQueryHandler(IOrderRepository repo) : IRequestHandler<GetOrderQuery, Ord` |
| GetOrder → GetOrder/GetOrderQueryHandler | src/api/Orders.Api/Controllers/OrdersController.cs | 11 | `public async Task<IActionResult> GetOrder(Guid id, CancellationToken ct) => Ok(await sender.Send(new` |
| GetOrder → GetOrder/GetOrderQueryHandler | src/web/src/api/ordersApi.ts | 3 | `export async function getOrder(id: string): Promise<Order> {` |
| GetOrder → GetOrder/GetOrderQueryHandler | src/web/src/pages/OrderDetailPage.tsx | 1 | `import { getOrder } from '../api/ordersApi';` |
| GetOrder → GetOrder/GetOrderQueryHandler | src/web/src/pages/OrderDetailPage.tsx | 4 | `void getOrder(id);` |
| CancelOrder → CancelOrder/CancelOrderDialog/CancelOrderCommandHandler | (無) | | |
| IssueRefund → IssueRefund/IssueRefundCommandHandler | (無) | | |
| ListCancellations → ListCancellations/ListCancellationsQueryHandler | (無) | | |
| SqlOrderRepository | src/api/Orders.Infrastructure/SqlOrderRepository.cs | 5 | `public sealed class SqlOrderRepository : IOrderRepository` |
| PaymentGatewayClient | src/api/Orders.Infrastructure/PaymentGatewayClient.cs | 5 | `public sealed class PaymentGatewayClient : IPaymentGateway` |
| OrdersController | src/api/Orders.Api/Controllers/OrdersController.cs | 8 | `public sealed class OrdersController(ISender sender) : ControllerBase` |
| OrderDetailPage | src/web/src/pages/OrderDetailPage.tsx | 3 | `export function OrderDetailPage({ id }: { id: string }) {` |
| Order type → Order/type/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi/OrdersController/CancelOrderCommandHandler/SqlOrderRepository/Orders | src/database/001_orders.sql | 2 | `CREATE TABLE Orders (` |
| Order type → Order/type/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi/OrdersController/CancelOrderCommandHandler/SqlOrderRepository/Orders | src/api/Orders.Infrastructure/PaymentGatewayClient.cs | 1 | `namespace Orders.Infrastructure;` |
| Order type → Order/type/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi/OrdersController/CancelOrderCommandHandler/SqlOrderRepository/Orders | src/api/Orders.Infrastructure/SqlOrderRepository.cs | 1 | `using Orders.Domain;` |
| Order type → Order/type/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi/OrdersController/CancelOrderCommandHandler/SqlOrderRepository/Orders | src/api/Orders.Infrastructure/SqlOrderRepository.cs | 3 | `namespace Orders.Infrastructure;` |
| Order type → Order/type/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi/OrdersController/CancelOrderCommandHandler/SqlOrderRepository/Orders | src/api/Orders.Infrastructure/SqlOrderRepository.cs | 5 | `public sealed class SqlOrderRepository : IOrderRepository` |
