# Survey 候選(由 analyze.survey 產生,不手改;定案寫 survey-mapping.md)

| 模型元素 | 候選檔案 | 行 | 片段 |
|---|---|---|---|
| Order | src/web/src/types/Order.ts | 4 | `export type Order = {` |
| Order | src/web/src/api/ordersApi.ts | 1 | `import type { Order } from '../types/Order';` |
| Order | src/web/src/api/ordersApi.ts | 3 | `export async function getOrder(id: string): Promise<Order> {` |
| Refund | (無) | | |
| CancelOrder | (無) | | |
| IssueRefund | (無) | | |
| ListCancellations | (無) | | |
| Order → Order/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi | src/web/src/types/Order.ts | 4 | `export type Order = {` |
| Order → Order/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi | src/web/src/api/ordersApi.ts | 1 | `import type { Order } from '../types/Order';` |
| Order → Order/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi | src/web/src/api/ordersApi.ts | 3 | `export async function getOrder(id: string): Promise<Order> {` |
| Order → Order/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi | src/web/src/pages/OrderDetailPage.tsx | 1 | `import { getOrder } from '../api/ordersApi';` |
| Order → Order/OrderDetailPage/CancelOrderDialog/orderStore/ordersApi | src/web/src/pages/OrderDetailPage.tsx | 3 | `export function OrderDetailPage({ id }: { id: string }) {` |
| Shipped rule | src/web/src/types/Order.ts | 2 | `export type OrderStatus = 'Placed' ¦ 'Shipped';` |
| GetOrder → GetOrder/getOrder | src/web/src/api/ordersApi.ts | 3 | `export async function getOrder(id: string): Promise<Order> {` |
| GetOrder → GetOrder/getOrder | src/web/src/pages/OrderDetailPage.tsx | 1 | `import { getOrder } from '../api/ordersApi';` |
| GetOrder → GetOrder/getOrder | src/web/src/pages/OrderDetailPage.tsx | 4 | `void getOrder(id);` |
| CancelOrder → CancelOrder/CancelOrderDialog | (無) | | |
| OrderDetailPage | src/web/src/pages/OrderDetailPage.tsx | 3 | `export function OrderDetailPage({ id }: { id: string }) {` |
