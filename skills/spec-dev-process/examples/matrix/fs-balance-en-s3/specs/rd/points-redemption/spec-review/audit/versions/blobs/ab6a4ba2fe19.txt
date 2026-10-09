# Loyalty points redemption — architecture (C4)

## Context (L1)
### C4-L1
```mermaid
C4Context
  Person(u, "member")
  System(sys, "Loyalty points redemption")
  System_Ext(ext, "RewardVendor")
  Rel(u, sys, "use")
  Rel(sys, ext, "call")
```

## Container (L2)
### C4-L2
```mermaid
C4Container
  Container(web, "Web", "React", "")
  Container(api, "API", ".NET", "")
  ContainerDb(db, "SQL Server", "", "")
```

## Component (L3)
| ID | Name | Layer | Context | depends | external | Tech |
|---|---|---|---|---|---|---|
| CMP-001 | RewardsPage | Page | Loyalty | CMP-002, CMP-003, CMP-004 |  | React |
| CMP-002 | RedeemDialog | Component | Loyalty | CMP-004 |  | React |
| CMP-003 | TransactionList | Component | Loyalty | CMP-004 |  | React |
| CMP-004 | rewardsStore | Store | Loyalty | CMP-005 |  | Zustand |
| CMP-005 | pointsApi | ApiClient | Loyalty | CMP-006 |  |  |
| CMP-006 | PointsController | Api | Loyalty | CMP-007, CMP-009 |  | ASP.NET Core |
| CMP-007 | RedeemRewardCommandHandler | Application | Loyalty | CMP-010, CMP-011, CMP-012 |  | MediatR |
| CMP-008 | ExpirePointsJob | Application | Loyalty | CMP-010, CMP-011 |  | ASP.NET Core |
| CMP-009 | ListTransactionsQueryHandler | Application | Loyalty | CMP-010, CMP-011 |  | MediatR |
| CMP-010 | Redemption (Aggregate) | Domain | Loyalty |  |  |  |
| CMP-011 | SqlPointsAccountRepository : IPointsAccountRepository | Infrastructure | Loyalty |  |  | EF Core |
| CMP-012 | RewardVendorClient : IRewardVendor | Infrastructure | Loyalty |  | RewardVendor |  |

### C4-L3
```mermaid
flowchart LR
  CMP001["RewardsPage<br/>Page"]
  CMP002["RedeemDialog<br/>Component"]
  CMP003["TransactionList<br/>Component"]
  CMP004["rewardsStore<br/>Store"]
  CMP005["pointsApi<br/>ApiClient"]
  CMP006["PointsController<br/>Api"]
  CMP007["RedeemRewardCommandHandler<br/>Application"]
  CMP008["ExpirePointsJob<br/>Application"]
  CMP009["ListTransactionsQueryHandler<br/>Application"]
  CMP010["Redemption (Aggregate)<br/>Domain"]
  CMP011["SqlPointsAccountRepository<br/>Infrastructure"]
  CMP012["RewardVendorClient<br/>Infrastructure"]
  CMP001 --> CMP002
  CMP001 --> CMP003
  CMP001 --> CMP004
  CMP002 --> CMP004
  CMP003 --> CMP004
  CMP004 --> CMP005
  CMP005 --> CMP006
  CMP006 --> CMP007
  CMP006 --> CMP009
  CMP007 --> CMP010
  CMP007 --> CMP011
  CMP007 --> CMP012
  CMP008 --> CMP010
  CMP008 --> CMP011
  CMP009 --> CMP010
  CMP009 --> CMP011
```

## Traceability
| AC | CMP | via | Responsibility |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | render and trigger redeem |
| AC-001-1 | CMP-002 | SEQ-001 | UI guard for redeem |
| AC-001-1 | CMP-004 | SEQ-001 | client state transition for redeem |
| AC-001-1 | CMP-005 | SEQ-001 | call the API for redeem |
| AC-001-1 | CMP-006 | SEQ-001 | receive the redeem request |
| AC-001-1 | CMP-007 | SEQ-001 | orchestrate redeem |
| AC-001-1 | CMP-010 | SEQ-001 | enforce the redeem invariant |
| AC-001-1 | CMP-011 | SEQ-001 | persist the redeem result |
| AC-001-1 | CMP-012 | SEQ-001 | call the external system for redeem |
| AC-001-2 | CMP-001 | SEQ-001 | render and trigger redeem |
| AC-001-2 | CMP-002 | SEQ-001 | UI guard for redeem |
| AC-001-2 | CMP-004 | SEQ-001 | client state transition for redeem |
| AC-001-2 | CMP-005 | SEQ-001 | call the API for redeem |
| AC-001-2 | CMP-006 | SEQ-001 | receive the redeem request |
| AC-001-2 | CMP-007 | SEQ-001 | orchestrate redeem |
| AC-001-2 | CMP-010 | SEQ-001 | enforce the redeem invariant |
| AC-001-2 | CMP-011 | SEQ-001 | persist the redeem result |
| AC-001-2 | CMP-012 | SEQ-001 | call the external system for redeem |
| AC-002-1 | CMP-004 | SEQ-002 | client state transition for expire |
| AC-002-1 | CMP-005 | SEQ-002 | call the API for expire |
| AC-002-1 | CMP-008 | SEQ-002 | orchestrate expire |
| AC-002-1 | CMP-010 | SEQ-002 | enforce the expire invariant |
| AC-002-1 | CMP-011 | SEQ-002 | persist the expire result |
| AC-003-1 | CMP-001 | SEQ-003 | render and trigger view |
| AC-003-1 | CMP-003 | SEQ-003 | UI guard for view |
| AC-003-1 | CMP-004 | SEQ-003 | client state transition for view |
| AC-003-1 | CMP-005 | SEQ-003 | call the API for view |
| AC-003-1 | CMP-006 | SEQ-003 | receive the view request |
| AC-003-1 | CMP-009 | SEQ-003 | orchestrate view |
| AC-003-1 | CMP-010 | SEQ-003 | enforce the view invariant |
| AC-003-1 | CMP-011 | SEQ-003 | persist the view result |
| AC-N01-1 | CMP-006 | API-001 | NFR balance never negative |

## Sequence
### SEQ-001 (UC-001 / REQ-001)
```mermaid
sequenceDiagram
  actor U as Member
  participant CMP001 as RewardsPage
  participant CMP002 as RedeemDialog
  participant CMP004 as rewardsStore
  participant CMP005 as pointsApi
  participant CMP006 as PointsController
  participant CMP007 as RedeemRewardCommandHandler
  participant CMP010 as Redemption
  participant CMP011 as SqlPointsAccountRepository
  participant CMP012 as RewardVendorClient
  U->>CMP001: RedeemReward
  CMP001->>CMP002: RedeemReward
  CMP002->>CMP004: RedeemReward
  CMP004->>CMP005: RedeemReward
  CMP005->>CMP006: RedeemReward
  CMP006->>CMP007: RedeemReward
  CMP007->>CMP010: RedeemReward
  CMP010-->>CMP007: ok
  CMP007->>CMP011: RedeemReward
  CMP011-->>CMP007: ok
  CMP007->>CMP012: RedeemReward
  CMP012-->>CMP007: ok
  CMP007-->>CMP006: ok
  CMP006-->>CMP005: ok
  CMP005-->>CMP004: ok
  CMP004-->>CMP002: ok
  CMP002-->>CMP001: ok
  CMP001-->>U: ok
```

### SEQ-002 (UC-002 / REQ-002)
```mermaid
sequenceDiagram
  actor U as System
  participant CMP004 as rewardsStore
  participant CMP005 as pointsApi
  participant CMP008 as ExpirePointsJob
  participant CMP010 as Redemption
  participant CMP011 as SqlPointsAccountRepository
  U->>CMP004: ExpirePoints
  CMP004->>CMP005: ExpirePoints
  CMP005-->>CMP004: ok
  CMP004-->>U: ok
  U->>CMP008: ExpirePoints
  CMP008->>CMP010: ExpirePoints
  CMP010-->>CMP008: ok
  CMP008->>CMP011: ExpirePoints
  CMP011-->>CMP008: ok
  CMP008-->>U: ok
```

### SEQ-003 (UC-003 / REQ-003)
```mermaid
sequenceDiagram
  actor U as Member
  participant CMP001 as RewardsPage
  participant CMP003 as TransactionList
  participant CMP004 as rewardsStore
  participant CMP005 as pointsApi
  participant CMP006 as PointsController
  participant CMP009 as ListTransactionsQueryHandler
  participant CMP010 as Redemption
  participant CMP011 as SqlPointsAccountRepository
  U->>CMP001: ListTransactions
  CMP001->>CMP003: ListTransactions
  CMP003->>CMP004: ListTransactions
  CMP004->>CMP005: ListTransactions
  CMP005->>CMP006: ListTransactions
  CMP006->>CMP009: ListTransactions
  CMP009->>CMP010: ListTransactions
  CMP010-->>CMP009: ok
  CMP009->>CMP011: ListTransactions
  CMP011-->>CMP009: ok
  CMP009-->>CMP006: ok
  CMP006-->>CMP005: ok
  CMP005-->>CMP004: ok
  CMP004-->>CMP003: ok
  CMP003-->>CMP001: ok
  CMP001-->>U: ok
```

