# 會員點數兌換 — architecture (C4)

## Context(L1)
### C4-L1
```mermaid
C4Context
  Person(u, "會員")
  System(sys, "會員點數兌換")
  System_Ext(ext, "RewardVendor")
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
| CMP-001 | PointsController | Api | Loyalty | CMP-002, CMP-004 |  | ASP.NET Core |
| CMP-002 | RedeemRewardCommandHandler | Application | Loyalty | CMP-005, CMP-006, CMP-007 |  | MediatR |
| CMP-003 | ExpirePointsJob | Application | Loyalty | CMP-005, CMP-006 |  | ASP.NET Core |
| CMP-004 | ListTransactionsQueryHandler | Application | Loyalty | CMP-005, CMP-006 |  | MediatR |
| CMP-005 | Redemption (Aggregate) | Domain | Loyalty |  |  |  |
| CMP-006 | SqlPointsAccountRepository : IPointsAccountRepository | Infrastructure | Loyalty |  |  | EF Core |
| CMP-007 | RewardVendorClient : IRewardVendor | Infrastructure | Loyalty |  | RewardVendor |  |

### C4-L3
```mermaid
flowchart LR
  CMP001["PointsController<br/>Api"]
  CMP002["RedeemRewardCommandHandler<br/>Application"]
  CMP003["ExpirePointsJob<br/>Application"]
  CMP004["ListTransactionsQueryHandler<br/>Application"]
  CMP005["Redemption (Aggregate)<br/>Domain"]
  CMP006["SqlPointsAccountRepository<br/>Infrastructure"]
  CMP007["RewardVendorClient<br/>Infrastructure"]
  CMP001 --> CMP002
  CMP001 --> CMP004
  CMP002 --> CMP005
  CMP002 --> CMP006
  CMP002 --> CMP007
  CMP003 --> CMP005
  CMP003 --> CMP006
  CMP004 --> CMP005
  CMP004 --> CMP006
```

## 追溯(AC → 技術元件)
| AC | CMP | via | 職責 |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | 接收兌換請求 |
| AC-001-1 | CMP-002 | SEQ-001 | 編排兌換 |
| AC-001-1 | CMP-005 | SEQ-001 | 兌換的業務規則與不變量 |
| AC-001-1 | CMP-006 | SEQ-001 | 持久化兌換結果 |
| AC-001-1 | CMP-007 | SEQ-001 | 為兌換呼叫外部系統 |
| AC-001-2 | CMP-001 | SEQ-001 | 接收兌換請求 |
| AC-001-2 | CMP-002 | SEQ-001 | 編排兌換 |
| AC-001-2 | CMP-005 | SEQ-001 | 兌換的業務規則與不變量 |
| AC-001-2 | CMP-006 | SEQ-001 | 持久化兌換結果 |
| AC-001-2 | CMP-007 | SEQ-001 | 為兌換呼叫外部系統 |
| AC-002-1 | CMP-003 | SEQ-002 | 編排到期 |
| AC-002-1 | CMP-005 | SEQ-002 | 到期的業務規則與不變量 |
| AC-002-1 | CMP-006 | SEQ-002 | 持久化到期結果 |
| AC-003-1 | CMP-001 | SEQ-003 | 接收查看請求 |
| AC-003-1 | CMP-004 | SEQ-003 | 編排查看 |
| AC-003-1 | CMP-005 | SEQ-003 | 查看的業務規則與不變量 |
| AC-003-1 | CMP-006 | SEQ-003 | 持久化查看結果 |
| AC-N01-1 | CMP-001 | API-001 | NFR balance never negative |

## Sequence
### SEQ-001 (UC-001 / REQ-001)
```mermaid
sequenceDiagram
  actor U as Member
  participant CMP001 as PointsController
  participant CMP002 as RedeemRewardCommandHandler
  participant CMP005 as Redemption
  participant CMP006 as SqlPointsAccountRepository
  participant CMP007 as RewardVendorClient
  U->>CMP001: RedeemReward
  CMP001->>CMP002: RedeemReward
  CMP002->>CMP005: RedeemReward
  CMP005-->>CMP002: ok
  CMP002->>CMP006: RedeemReward
  CMP006-->>CMP002: ok
  CMP002->>CMP007: RedeemReward
  CMP007-->>CMP002: ok
  CMP002-->>CMP001: ok
  CMP001-->>U: ok
```

### SEQ-002 (UC-002 / REQ-002)
```mermaid
sequenceDiagram
  actor U as System
  participant CMP003 as ExpirePointsJob
  participant CMP005 as Redemption
  participant CMP006 as SqlPointsAccountRepository
  U->>CMP003: ExpirePoints
  CMP003->>CMP005: ExpirePoints
  CMP005-->>CMP003: ok
  CMP003->>CMP006: ExpirePoints
  CMP006-->>CMP003: ok
  CMP003-->>U: ok
```

### SEQ-003 (UC-003 / REQ-003)
```mermaid
sequenceDiagram
  actor U as Member
  participant CMP001 as PointsController
  participant CMP004 as ListTransactionsQueryHandler
  participant CMP005 as Redemption
  participant CMP006 as SqlPointsAccountRepository
  U->>CMP001: ListTransactions
  CMP001->>CMP004: ListTransactions
  CMP004->>CMP005: ListTransactions
  CMP005-->>CMP004: ok
  CMP004->>CMP006: ListTransactions
  CMP006-->>CMP004: ok
  CMP004-->>CMP001: ok
  CMP001-->>U: ok
```

