# 會員點數兌換 — architecture (C4)

## Context(L1)
### C4-L1
```mermaid
C4Context
  Person(u, "member")
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
| CMP-001 | RewardsPage | Page | Loyalty | CMP-002, CMP-003, CMP-004 |  | React |
| CMP-002 | RedeemDialog | Component | Loyalty | CMP-004 |  | React |
| CMP-003 | TransactionList | Component | Loyalty | CMP-004 |  | React |
| CMP-004 | rewardsStore | Store | Loyalty | CMP-005 |  | Zustand |
| CMP-005 | pointsApi | ApiClient | Loyalty | CMP-006 |  |  |
| CMP-006 | PointsController | Api | Loyalty | CMP-007, CMP-009 |  | ASP.NET Core |
| CMP-007 | RedeemRewardCommandHandler | Application | Loyalty | CMP-010, CMP-011 |  | MediatR |
| CMP-008 | ExpirePointsJob | Application | Loyalty | CMP-010 |  | ASP.NET Core |
| CMP-009 | ListTransactionsQueryHandler | Application | Loyalty | CMP-010 |  | MediatR |
| CMP-010 | SqlPointsAccountRepository : IPointsAccountRepository | Infrastructure | Loyalty |  |  | EF Core |
| CMP-011 | RewardVendorClient : IRewardVendor | Infrastructure | Loyalty |  | RewardVendor |  |

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
  CMP010["SqlPointsAccountRepository<br/>Infrastructure"]
  CMP011["RewardVendorClient<br/>Infrastructure"]
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
  CMP008 --> CMP010
  CMP009 --> CMP010
```

## 追溯(AC → 技術元件)
| AC | CMP | via | 職責 |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | 顯示並觸發redeem |
| AC-001-1 | CMP-002 | SEQ-001 | redeem的 UI 守衛 |
| AC-001-1 | CMP-004 | SEQ-001 | redeem的前端狀態轉移 |
| AC-001-1 | CMP-005 | SEQ-001 | 呼叫redeem API |
| AC-001-1 | CMP-006 | SEQ-001 | 接收redeem請求 |
| AC-001-1 | CMP-007 | SEQ-001 | 編排redeem |
| AC-001-1 | CMP-010 | SEQ-001 | 持久化redeem結果 |
| AC-001-1 | CMP-011 | SEQ-001 | 為redeem呼叫外部系統 |
| AC-001-2 | CMP-001 | SEQ-001 | 顯示並觸發redeem |
| AC-001-2 | CMP-002 | SEQ-001 | redeem的 UI 守衛 |
| AC-001-2 | CMP-004 | SEQ-001 | redeem的前端狀態轉移 |
| AC-001-2 | CMP-005 | SEQ-001 | 呼叫redeem API |
| AC-001-2 | CMP-006 | SEQ-001 | 接收redeem請求 |
| AC-001-2 | CMP-007 | SEQ-001 | 編排redeem |
| AC-001-2 | CMP-010 | SEQ-001 | 持久化redeem結果 |
| AC-001-2 | CMP-011 | SEQ-001 | 為redeem呼叫外部系統 |
| AC-002-1 | CMP-004 | SEQ-002 | expire的前端狀態轉移 |
| AC-002-1 | CMP-005 | SEQ-002 | 呼叫expire API |
| AC-002-1 | CMP-008 | SEQ-002 | 編排expire |
| AC-002-1 | CMP-010 | SEQ-002 | 持久化expire結果 |
| AC-003-1 | CMP-001 | SEQ-003 | 顯示並觸發view |
| AC-003-1 | CMP-003 | SEQ-003 | view的 UI 守衛 |
| AC-003-1 | CMP-004 | SEQ-003 | view的前端狀態轉移 |
| AC-003-1 | CMP-005 | SEQ-003 | 呼叫view API |
| AC-003-1 | CMP-006 | SEQ-003 | 接收view請求 |
| AC-003-1 | CMP-009 | SEQ-003 | 編排view |
| AC-003-1 | CMP-010 | SEQ-003 | 持久化view結果 |
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
  participant CMP010 as SqlPointsAccountRepository
  participant CMP011 as RewardVendorClient
  U->>CMP001: RedeemReward
  CMP001->>CMP002: RedeemReward
  CMP002->>CMP004: RedeemReward
  CMP004->>CMP005: RedeemReward
  CMP005->>CMP006: RedeemReward
  CMP006->>CMP007: RedeemReward
  CMP007->>CMP010: RedeemReward
  CMP010->>CMP011: RedeemReward
  CMP001-->>U: ok
```

### SEQ-002 (UC-002 / REQ-002)
```mermaid
sequenceDiagram
  actor U as System
  participant CMP004 as rewardsStore
  participant CMP005 as pointsApi
  participant CMP008 as ExpirePointsJob
  participant CMP010 as SqlPointsAccountRepository
  U->>CMP004: ExpirePoints
  CMP004->>CMP005: ExpirePoints
  CMP005->>CMP008: ExpirePoints
  CMP008->>CMP010: ExpirePoints
  CMP004-->>U: ok
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
  participant CMP010 as SqlPointsAccountRepository
  U->>CMP001: ListTransactions
  CMP001->>CMP003: ListTransactions
  CMP003->>CMP004: ListTransactions
  CMP004->>CMP005: ListTransactions
  CMP005->>CMP006: ListTransactions
  CMP006->>CMP009: ListTransactions
  CMP009->>CMP010: ListTransactions
  CMP001-->>U: ok
```

