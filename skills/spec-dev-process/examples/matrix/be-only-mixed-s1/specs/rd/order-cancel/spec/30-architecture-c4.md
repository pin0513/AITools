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
  Container(api, "API", ".NET", "")
  ContainerDb(db, "SQL Server", "", "")
```

## Component(L3)
| ID | 名稱 | Layer | Context | depends | external | 技術 |
|---|---|---|---|---|---|---|
| CMP-001 | OrdersController | Api | Orders | CMP-002, CMP-003, CMP-004 |  | ASP.NET Core |
| CMP-002 | CancelOrderCommandHandler | Application | Orders | CMP-005, CMP-006 |  | MediatR |
| CMP-003 | IssueRefundCommandHandler | Application | Orders | CMP-005, CMP-006, CMP-007 |  | MediatR |
| CMP-004 | ListCancellationsQueryHandler | Application | Orders | CMP-005, CMP-006 |  | MediatR |
| CMP-005 | Order (Aggregate) | Domain | Orders |  |  |  |
| CMP-006 | SqlOrderRepository : IOrderRepository | Infrastructure | Orders |  |  | EF Core |
| CMP-007 | PaymentGatewayClient : IPaymentGateway | Infrastructure | Orders |  | PaymentGateway |  |

### C4-L3
```mermaid
flowchart LR
  CMP001["OrdersController<br/>Api"]
  CMP002["CancelOrderCommandHandler<br/>Application"]
  CMP003["IssueRefundCommandHandler<br/>Application"]
  CMP004["ListCancellationsQueryHandler<br/>Application"]
  CMP005["Order (Aggregate)<br/>Domain"]
  CMP006["SqlOrderRepository<br/>Infrastructure"]
  CMP007["PaymentGatewayClient<br/>Infrastructure"]
  CMP001 --> CMP002
  CMP001 --> CMP003
  CMP001 --> CMP004
  CMP002 --> CMP005
  CMP002 --> CMP006
  CMP003 --> CMP005
  CMP003 --> CMP006
  CMP003 --> CMP007
  CMP004 --> CMP005
  CMP004 --> CMP006
```

## 追溯(AC → 技術元件)
| AC | CMP | via | 職責 |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | 接收cancel請求 |
| AC-001-1 | CMP-002 | SEQ-001 | 編排cancel |
| AC-001-1 | CMP-005 | SEQ-001 | cancel的業務規則與不變量 |
| AC-001-1 | CMP-006 | SEQ-001 | 持久化cancel結果 |
| AC-001-2 | CMP-001 | SEQ-001 | 接收cancel請求 |
| AC-001-2 | CMP-002 | SEQ-001 | 編排cancel |
| AC-001-2 | CMP-005 | SEQ-001 | cancel的業務規則與不變量 |
| AC-001-2 | CMP-006 | SEQ-001 | 持久化cancel結果 |
| AC-002-1 | CMP-001 | SEQ-002 | 接收refund請求 |
| AC-002-1 | CMP-003 | SEQ-002 | 編排refund |
| AC-002-1 | CMP-005 | SEQ-002 | refund的業務規則與不變量 |
| AC-002-1 | CMP-006 | SEQ-002 | 持久化refund結果 |
| AC-002-1 | CMP-007 | SEQ-002 | 為refund呼叫外部系統 |
| AC-002-2 | CMP-001 | SEQ-002 | 接收refund請求 |
| AC-002-2 | CMP-003 | SEQ-002 | 編排refund |
| AC-002-2 | CMP-005 | SEQ-002 | refund的業務規則與不變量 |
| AC-002-2 | CMP-006 | SEQ-002 | 持久化refund結果 |
| AC-002-2 | CMP-007 | SEQ-002 | 為refund呼叫外部系統 |
| AC-003-1 | CMP-001 | SEQ-003 | 接收view請求 |
| AC-003-1 | CMP-004 | SEQ-003 | 編排view |
| AC-003-1 | CMP-005 | SEQ-003 | view的業務規則與不變量 |
| AC-003-1 | CMP-006 | SEQ-003 | 持久化view結果 |
| AC-N01-1 | CMP-001 | API-002 | NFR P95 < 5 min |

## Sequence
### SEQ-001 (UC-001 / REQ-001)
```mermaid
sequenceDiagram
  actor U as Customer
  participant CMP001 as OrdersController
  participant CMP002 as CancelOrderCommandHandler
  participant CMP005 as Order
  participant CMP006 as SqlOrderRepository
  U->>CMP001: CancelOrder
  CMP001->>CMP002: CancelOrder
  CMP002->>CMP005: CancelOrder
  CMP005-->>CMP002: ok
  CMP002->>CMP006: CancelOrder
  CMP006-->>CMP002: ok
  CMP002-->>CMP001: ok
  CMP001-->>U: ok
```

### SEQ-002 (UC-002 / REQ-002)
```mermaid
sequenceDiagram
  actor U as System
  participant CMP001 as OrdersController
  participant CMP003 as IssueRefundCommandHandler
  participant CMP005 as Order
  participant CMP006 as SqlOrderRepository
  participant CMP007 as PaymentGatewayClient
  U->>CMP001: IssueRefund
  CMP001->>CMP003: IssueRefund
  CMP003->>CMP005: IssueRefund
  CMP005-->>CMP003: ok
  CMP003->>CMP006: IssueRefund
  CMP006-->>CMP003: ok
  CMP003->>CMP007: IssueRefund
  CMP007-->>CMP003: ok
  CMP003-->>CMP001: ok
  CMP001-->>U: ok
```

### SEQ-003 (UC-003 / REQ-003)
```mermaid
sequenceDiagram
  actor U as SupportAgent
  participant CMP001 as OrdersController
  participant CMP004 as ListCancellationsQueryHandler
  participant CMP005 as Order
  participant CMP006 as SqlOrderRepository
  U->>CMP001: ListCancellations
  CMP001->>CMP004: ListCancellations
  CMP004->>CMP005: ListCancellations
  CMP005-->>CMP004: ok
  CMP004->>CMP006: ListCancellations
  CMP006-->>CMP004: ok
  CMP004-->>CMP001: ok
  CMP001-->>U: ok
```

