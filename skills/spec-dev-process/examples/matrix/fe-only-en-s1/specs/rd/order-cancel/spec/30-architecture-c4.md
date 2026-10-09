# Order cancellation and refund — architecture (C4)

## Context (L1)
### C4-L1
```mermaid
C4Context
  Person(u, "customer")
  System(sys, "Order cancellation and refund")
  System_Ext(ext, "BackendAPI")
  Rel(u, sys, "use")
  Rel(sys, ext, "call")
```

## Container (L2)
### C4-L2
```mermaid
C4Container
  Container(web, "Web", "React", "")
```

## Component (L3)
| ID | Name | Layer | Context | depends | external | Tech |
|---|---|---|---|---|---|---|
| CMP-001 | OrderDetailPage | Page | Orders | CMP-002, CMP-003, CMP-004 |  | React |
| CMP-002 | CancelOrderDialog | Component | Orders | CMP-004 |  | React |
| CMP-003 | CancellationHistoryTable | Component | Orders | CMP-004 |  | React |
| CMP-004 | orderStore | Store | Orders | CMP-005 |  | Zustand |
| CMP-005 | ordersApi | ApiClient | Orders |  | BackendAPI |  |

### C4-L3
```mermaid
flowchart LR
  CMP001["OrderDetailPage<br/>Page"]
  CMP002["CancelOrderDialog<br/>Component"]
  CMP003["CancellationHistoryTable<br/>Component"]
  CMP004["orderStore<br/>Store"]
  CMP005["ordersApi<br/>ApiClient"]
  CMP001 --> CMP002
  CMP001 --> CMP003
  CMP001 --> CMP004
  CMP002 --> CMP004
  CMP003 --> CMP004
  CMP004 --> CMP005
```

## Traceability
| AC | CMP | via | Responsibility |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | render and trigger cancel |
| AC-001-1 | CMP-002 | SEQ-001 | UI guard for cancel |
| AC-001-1 | CMP-004 | SEQ-001 | client state transition for cancel |
| AC-001-1 | CMP-005 | SEQ-001 | call the API for cancel |
| AC-001-2 | CMP-001 | SEQ-001 | render and trigger cancel |
| AC-001-2 | CMP-002 | SEQ-001 | UI guard for cancel |
| AC-001-2 | CMP-004 | SEQ-001 | client state transition for cancel |
| AC-001-2 | CMP-005 | SEQ-001 | call the API for cancel |
| AC-002-1 | CMP-001 | SEQ-001 | render and trigger refund |
| AC-002-1 | CMP-004 | SEQ-001 | client state transition for refund |
| AC-002-1 | CMP-005 | SEQ-001 | call the API for refund |
| AC-002-2 | CMP-001 | SEQ-001 | render and trigger refund |
| AC-002-2 | CMP-004 | SEQ-001 | client state transition for refund |
| AC-002-2 | CMP-005 | SEQ-001 | call the API for refund |
| AC-003-1 | CMP-001 | SEQ-001 | render and trigger view |
| AC-003-1 | CMP-003 | SEQ-001 | UI guard for view |
| AC-003-1 | CMP-004 | SEQ-001 | client state transition for view |
| AC-003-1 | CMP-005 | SEQ-001 | call the API for view |
| AC-N01-1 | CMP-005 | API-002 | NFR P95 < 5 min |

## Sequence
### SEQ-001 (UC-001 / REQ-001)
```mermaid
sequenceDiagram
  actor U as Customer
  participant CMP001 as OrderDetailPage
  participant CMP002 as CancelOrderDialog
  participant CMP004 as orderStore
  participant CMP005 as ordersApi
  U->>CMP001: CancelOrder
  CMP001->>CMP002: CancelOrder
  CMP002->>CMP004: CancelOrder
  CMP004->>CMP005: CancelOrder
  CMP001-->>U: ok
```
