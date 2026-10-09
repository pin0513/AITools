import { getOrder } from '../api/ordersApi';

export function OrderDetailPage({ id }: { id: string }) {
  void getOrder(id);
  return <main />;
}
