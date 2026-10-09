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
  Container(web, "Web", "React", "")
  Container(api, "API", ".NET", "")
  ContainerDb(db, "SQL Server", "", "")
```

## Component(L3)
| ID | 名稱 | Layer | Context | depends | external | 技術 |
|---|---|---|---|---|---|---|
| CMP-001 | RewardsPage | Page | Loyalty | CMP-002 |  | React |
| CMP-002 | pointsApi | ApiClient | Loyalty | CMP-003 |  |  |
| CMP-003 | PointsController | Api | Loyalty | CMP-004, CMP-006 |  | ASP.NET Core |
| CMP-004 | RedeemRewardCommandHandler | Application | Loyalty | CMP-007, CMP-008, CMP-009 |  | MediatR |
| CMP-005 | ExpirePointsJob | Application | Loyalty | CMP-007, CMP-008 |  | ASP.NET Core |
| CMP-006 | ListTransactionsQueryHandler | Application | Loyalty | CMP-007, CMP-008 |  | MediatR |
| CMP-007 | Redemption (Aggregate) | Domain | Loyalty |  |  |  |
| CMP-008 | SqlPointsAccountRepository : IPointsAccountRepository | Infrastructure | Loyalty |  |  | EF Core |
| CMP-009 | RewardVendorClient : IRewardVendor | Infrastructure | Loyalty |  | RewardVendor |  |

### C4-L3
```mermaid
flowchart LR
  CMP001["RewardsPage<br/>Page"]
  CMP002["pointsApi<br/>ApiClient"]
  CMP003["PointsController<br/>Api"]
  CMP004["RedeemRewardCommandHandler<br/>Application"]
  CMP005["ExpirePointsJob<br/>Application"]
  CMP006["ListTransactionsQueryHandler<br/>Application"]
  CMP007["Redemption (Aggregate)<br/>Domain"]
  CMP008["SqlPointsAccountRepository<br/>Infrastructure"]
  CMP009["RewardVendorClient<br/>Infrastructure"]
  CMP001 --> CMP002
  CMP002 --> CMP003
  CMP003 --> CMP004
  CMP003 --> CMP006
  CMP004 --> CMP007
  CMP004 --> CMP008
  CMP004 --> CMP009
  CMP005 --> CMP007
  CMP005 --> CMP008
  CMP006 --> CMP007
  CMP006 --> CMP008
```

## 追溯(AC → 技術元件)
| AC | CMP | via | 職責 |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | 顯示並觸發兌換 |
| AC-001-1 | CMP-002 | SEQ-001 | 呼叫兌換 API |
| AC-001-1 | CMP-003 | SEQ-001 | 接收兌換請求 |
| AC-001-1 | CMP-004 | SEQ-001 | 編排兌換 |
| AC-001-1 | CMP-007 | SEQ-001 | 兌換的業務規則與不變量 |
| AC-001-1 | CMP-008 | SEQ-001 | 持久化兌換結果 |
| AC-001-1 | CMP-009 | SEQ-001 | 為兌換呼叫外部系統 |
| AC-001-2 | CMP-001 | SEQ-001 | 顯示並觸發兌換 |
| AC-001-2 | CMP-002 | SEQ-001 | 呼叫兌換 API |
| AC-001-2 | CMP-003 | SEQ-001 | 接收兌換請求 |
| AC-001-2 | CMP-004 | SEQ-001 | 編排兌換 |
| AC-001-2 | CMP-007 | SEQ-001 | 兌換的業務規則與不變量 |
| AC-001-2 | CMP-008 | SEQ-001 | 持久化兌換結果 |
| AC-001-2 | CMP-009 | SEQ-001 | 為兌換呼叫外部系統 |
| AC-002-1 | CMP-002 | SEQ-002 | 呼叫到期 API |
| AC-002-1 | CMP-005 | SEQ-002 | 編排到期 |
| AC-002-1 | CMP-007 | SEQ-002 | 到期的業務規則與不變量 |
| AC-002-1 | CMP-008 | SEQ-002 | 持久化到期結果 |
| AC-003-1 | CMP-001 | SEQ-003 | 顯示並觸發查看 |
| AC-003-1 | CMP-002 | SEQ-003 | 呼叫查看 API |
| AC-003-1 | CMP-003 | SEQ-003 | 接收查看請求 |
| AC-003-1 | CMP-006 | SEQ-003 | 編排查看 |
| AC-003-1 | CMP-007 | SEQ-003 | 查看的業務規則與不變量 |
| AC-003-1 | CMP-008 | SEQ-003 | 持久化查看結果 |
| AC-N01-1 | CMP-003 | API-001 | NFR balance never negative |

## Sequence
### SEQ-001 (UC-001 / REQ-001)
```mermaid
sequenceDiagram
  actor U as Member
  participant CMP001 as RewardsPage
  participant CMP002 as pointsApi
  participant CMP003 as PointsController
  participant CMP004 as RedeemRewardCommandHandler
  participant CMP007 as Redemption
  participant CMP008 as SqlPointsAccountRepository
  participant CMP009 as RewardVendorClient
  U->>CMP001: RedeemReward
  CMP001->>CMP002: RedeemReward
  CMP002->>CMP003: RedeemReward
  CMP003->>CMP004: RedeemReward
  CMP004->>CMP007: RedeemReward
  CMP007->>CMP008: RedeemReward
  CMP008->>CMP009: RedeemReward
  CMP001-->>U: ok
```

### SEQ-002 (UC-002 / REQ-002)
```mermaid
sequenceDiagram
  actor U as System
  participant CMP002 as pointsApi
  participant CMP005 as ExpirePointsJob
  participant CMP007 as Redemption
  participant CMP008 as SqlPointsAccountRepository
  U->>CMP002: ExpirePoints
  CMP002->>CMP005: ExpirePoints
  CMP005->>CMP007: ExpirePoints
  CMP007->>CMP008: ExpirePoints
  CMP002-->>U: ok
```

### SEQ-003 (UC-003 / REQ-003)
```mermaid
sequenceDiagram
  actor U as Member
  participant CMP001 as RewardsPage
  participant CMP002 as pointsApi
  participant CMP003 as PointsController
  participant CMP006 as ListTransactionsQueryHandler
  participant CMP007 as Redemption
  participant CMP008 as SqlPointsAccountRepository
  U->>CMP001: ListTransactions
  CMP001->>CMP002: ListTransactions
  CMP002->>CMP003: ListTransactions
  CMP003->>CMP006: ListTransactions
  CMP006->>CMP007: ListTransactions
  CMP007->>CMP008: ListTransactions
  CMP001-->>U: ok
```

