// shared front-end types (previous issue)
export type OrderStatus = 'Placed' | 'Shipped';

export type Order = {
  id: string;
  status: OrderStatus;
};
