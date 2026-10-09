# Order cancellation and refund (PM spec)

## 1 Background and Goals
Today a customer must phone support to cancel an order. Goal: self-service cancel and automatic refund through the payment gateway.

## 2 Users
customer: wants to cancel an order quickly. support agent: needs the cancellation history. system: issues the refund.

## 3 Functional Requirements
### 3.1 A customer can cancel an order before it is shipped
A customer can cancel an order while it is placed. An order that is already shipped cannot be cancelled. After cancel, the order status becomes cancelled.

### 3.2 The system issues a refund through the payment gateway after cancellation
After an order is cancelled, the system issues a refund through the payment gateway. When the payment gateway fails, the system retries up to 3 times and keeps the order cancelled. A successful refund marks the order as refunded.

### 3.3 A support agent can view the cancellation history
A support agent can view the cancellation history of every order, including time and reason.

## 4 Non-functional Requirements
A refund must finish within 5 minutes after cancellation for 95% of order records.

## 5 Acceptance
- an order is placed → the customer cancels it → the order status is cancelled
- an order is shipped → the customer cancels it → the response is 409 ORDER_SHIPPED and the status is unchanged
- an order is cancelled and paid → the system issues the refund → the payment gateway is called and the order is refunded
- the payment gateway times out → the system issues the refund → it retries 3 times and the order stays cancelled
- order records were cancelled → the support agent opens the history → each row shows the order, time and reason
