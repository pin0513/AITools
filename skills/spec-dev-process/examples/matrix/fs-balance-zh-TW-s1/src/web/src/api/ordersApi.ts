import type { Order } from '../types/Order';

export async function getOrder(id: string): Promise<Order> {
  return fetch(`/orders/${id}`).then(r => r.json());
}
