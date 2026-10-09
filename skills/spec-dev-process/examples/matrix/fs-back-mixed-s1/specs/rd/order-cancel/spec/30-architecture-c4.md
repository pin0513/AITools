# 訂單取消與退款 — architecture (C4)

## Context(L1)
### C4-L1
```mermaid
C4Context
  Person(u, "customer")
  System(sys, "訂單取消與退款")
  System_Ext(ext, "PaymentGateway")
  Rel(u, sys, "use")
  Rel(sys, ext, "call")
```

## Container(L2)
### C4-L2
```mermaid
C4Container
  Container(web, "Web", "React", "")
  Container(api, "API", ".NET", "")
  ContainerDb(db, "SQL Server", "", "")
```

## Component(L3)
| ID | 名稱 | Layer | Context | depends | external | 技術 |
|---|---|---|---|---|---|---|
| CMP-001 | OrderDetailPage | Page | Orders | CMP-002 |  | React |
| CMP-002 | ordersApi | ApiClient | Orders | CMP-003 |  |  |
| CMP-003 | OrdersController | Api | Orders | CMP-004, CMP-005, CMP-006 |  | ASP.NET Core |
| CMP-004 | CancelOrderCommandHandler | Application | Orders | CMP-007, CMP-008 |  | MediatR |
| CMP-005 | IssueRefundCommandHandler | Application | Orders | CMP-007, CMP-008, CMP-009 |  | MediatR |
| CMP-006 | ListCancellationsQueryHandler | Application | Orders | CMP-007, CMP-008 |  | MediatR |
| CMP-007 | Order (Aggregate) | Domain | Orders |  |  |  |
| CMP-008 | SqlOrderRepository : IOrderRepository | Infrastructure | Orders |  |  | EF Core |
| CMP-009 | PaymentGatewayClient : IPaymentGateway | Infrastructure | Orders |  | PaymentGateway |  |

### C4-L3
```mermaid
flowchart LR
  CMP001["OrderDetailPage<br/>Page"]
  CMP002["ordersApi<br/>ApiClient"]
  CMP003["OrdersController<br/>Api"]
  CMP004["CancelOrderCommandHandler<br/>Application"]
  CMP005["IssueRefundCommandHandler<br/>Application"]
  CMP006["ListCancellationsQueryHandler<br/>Application"]
  CMP007["Order (Aggregate)<br/>Domain"]
  CMP008["SqlOrderRepository<br/>Infrastructure"]
  CMP009["PaymentGatewayClient<br/>Infrastructure"]
  CMP001 --> CMP002
  CMP002 --> CMP003
  CMP003 --> CMP004
  CMP003 --> CMP005
  CMP003 --> CMP006
  CMP004 --> CMP007
  CMP004 --> CMP008
  CMP005 --> CMP007
  CMP005 --> CMP008
  CMP005 --> CMP009
  CMP006 --> CMP007
  CMP006 --> CMP008
```

## 追溯(AC → 技術元件)
| AC | CMP | via | 職責 |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | 顯示並觸發cancel |
| AC-001-1 | CMP-002 | SEQ-001 | 呼叫cancel API |
| AC-001-1 | CMP-003 | SEQ-001 | 接收cancel請求 |
| AC-001-1 | CMP-004 | SEQ-001 | 編排cancel |
| AC-001-1 | CMP-007 | SEQ-001 | cancel的業務規則與不變量 |
| AC-001-1 | CMP-008 | SEQ-001 | 持久化cancel結果 |
| AC-001-2 | CMP-001 | SEQ-001 | 顯示並觸發cancel |
| AC-001-2 | CMP-002 | SEQ-001 | 呼叫cancel API |
| AC-001-2 | CMP-003 | SEQ-001 | 接收cancel請求 |
| AC-001-2 | CMP-004 | SEQ-001 | 編排cancel |
| AC-001-2 | CMP-007 | SEQ-001 | cancel的業務規則與不變量 |
| AC-001-2 | CMP-008 | SEQ-001 | 持久化cancel結果 |
| AC-002-1 | CMP-001 | SEQ-002 | 顯示並觸發refund |
| AC-002-1 | CMP-002 | SEQ-002 | 呼叫refund API |
| AC-002-1 | CMP-003 | SEQ-002 | 接收refund請求 |
| AC-002-1 | CMP-005 | SEQ-002 | 編排refund |
| AC-002-1 | CMP-007 | SEQ-002 | refund的業務規則與不變量 |
| AC-002-1 | CMP-008 | SEQ-002 | 持久化refund結果 |
| AC-002-1 | CMP-009 | SEQ-002 | 為refund呼叫外部系統 |
| AC-002-2 | CMP-001 | SEQ-002 | 顯示並觸發refund |
| AC-002-2 | CMP-002 | SEQ-002 | 呼叫refund API |
| AC-002-2 | CMP-003 | SEQ-002 | 接收refund請求 |
| AC-002-2 | CMP-005 | SEQ-002 | 編排refund |
| AC-002-2 | CMP-007 | SEQ-002 | refund的業務規則與不變量 |
| AC-002-2 | CMP-008 | SEQ-002 | 持久化refund結果 |
| AC-002-2 | CMP-009 | SEQ-002 | 為refund呼叫外部系統 |
| AC-003-1 | CMP-001 | SEQ-003 | 顯示並觸發view |
| AC-003-1 | CMP-002 | SEQ-003 | 呼叫view API |
| AC-003-1 | CMP-003 | SEQ-003 | 接收view請求 |
| AC-003-1 | CMP-006 | SEQ-003 | 編排view |
| AC-003-1 | CMP-007 | SEQ-003 | view的業務規則與不變量 |
| AC-003-1 | CMP-008 | SEQ-003 | 持久化view結果 |
| AC-N01-1 | CMP-003 | API-002 | NFR P95 < 5 min |

## Sequence
### SEQ-001 (UC-001 / REQ-001)
```mermaid
sequenceDiagram
  actor U as Customer
  participant CMP001 as OrderDetailPage
  participant CMP002 as ordersApi
  participant CMP003 as OrdersController
  participant CMP004 as CancelOrderCommandHandler
  participant CMP007 as Order
  participant CMP008 as SqlOrderRepository
  U->>CMP001: CancelOrder
  CMP001->>CMP002: CancelOrder
  CMP002->>CMP003: CancelOrder
  CMP003->>CMP004: CancelOrder
  CMP004->>CMP007: CancelOrder
  CMP007-->>CMP004: ok
  CMP004->>CMP008: CancelOrder
  CMP008-->>CMP004: ok
  CMP004-->>CMP003: ok
  CMP003-->>CMP002: ok
  CMP002-->>CMP001: ok
  CMP001-->>U: ok
```

### SEQ-002 (UC-002 / REQ-002)
```mermaid
sequenceDiagram
  actor U as System
  participant CMP001 as OrderDetailPage
  participant CMP002 as ordersApi
  participant CMP003 as OrdersController
  participant CMP005 as IssueRefundCommandHandler
  participant CMP007 as Order
  participant CMP008 as SqlOrderRepository
  participant CMP009 as PaymentGatewayClient
  U->>CMP001: IssueRefund
  CMP001->>CMP002: IssueRefund
  CMP002->>CMP003: IssueRefund
  CMP003->>CMP005: IssueRefund
  CMP005->>CMP007: IssueRefund
  CMP007-->>CMP005: ok
  CMP005->>CMP008: IssueRefund
  CMP008-->>CMP005: ok
  CMP005->>CMP009: IssueRefund
  CMP009-->>CMP005: ok
  CMP005-->>CMP003: ok
  CMP003-->>CMP002: ok
  CMP002-->>CMP001: ok
  CMP001-->>U: ok
```

### SEQ-003 (UC-003 / REQ-003)
```mermaid
sequenceDiagram
  actor U as SupportAgent
  participant CMP001 as OrderDetailPage
  participant CMP002 as ordersApi
  participant CMP003 as OrdersController
  participant CMP006 as ListCancellationsQueryHandler
  participant CMP007 as Order
  participant CMP008 as SqlOrderRepository
  U->>CMP001: ListCancellations
  CMP001->>CMP002: ListCancellations
  CMP002->>CMP003: ListCancellations
  CMP003->>CMP006: ListCancellations
  CMP006->>CMP007: ListCancellations
  CMP007-->>CMP006: ok
  CMP006->>CMP008: ListCancellations
  CMP008-->>CMP006: ok
  CMP006-->>CMP003: ok
  CMP003-->>CMP002: ok
  CMP002-->>CMP001: ok
  CMP001-->>U: ok
```

