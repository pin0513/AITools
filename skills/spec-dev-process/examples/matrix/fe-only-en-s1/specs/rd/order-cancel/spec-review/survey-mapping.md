# Survey Mapping

## Mapping
| Element | Element Type | Status | Code Target | Evidence | Note |
|---|---|---|---|---|---|
| Order | Aggregate | modify | Order | src/web/src/types/Order.ts:4 | |
| Shipped rule | Rule | existing | Order.Shipped | src/web/src/types/Order.ts:2 "Shipped" | |
| Refund | Entity | new | Refund | | |
| GetOrder | Query | existing | getOrder | src/web/src/api/ordersApi.ts:3; src/web/src/api/ordersApi.ts:4 "/orders" | |
| CancelOrder | Command | new | CancelOrder | | |
| IssueRefund | Command | new | IssueRefund | | |
| ListCancellations | Query | new | ListCancellations | | |
| OrderDetailPage | Page | modify | OrderDetailPage | src/web/src/pages/OrderDetailPage.tsx:3; src/web/src/pages/OrderDetailPage.tsx:4 "getOrder(id)" | |
