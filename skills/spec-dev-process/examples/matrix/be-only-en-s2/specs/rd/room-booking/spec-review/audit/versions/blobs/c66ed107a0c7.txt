# Meeting room booking — architecture (C4)

## Context (L1)
### C4-L1
```mermaid
C4Context
  Person(u, "employee")
  System(sys, "Meeting room booking")
  System_Ext(ext, "CalendarService")
  Rel(u, sys, "use")
  Rel(sys, ext, "call")
```

## Container (L2)
### C4-L2
```mermaid
C4Container
  Container(api, "API", ".NET", "")
  ContainerDb(db, "SQL Server", "", "")
```

## Component (L3)
| ID | Name | Layer | Context | depends | external | Tech |
|---|---|---|---|---|---|---|
| CMP-001 | RoomsController | Api | Rooms | CMP-002, CMP-003, CMP-005 |  | ASP.NET Core |
| CMP-002 | BookRoomCommandHandler | Application | Rooms | CMP-006, CMP-007, CMP-008 |  | MediatR |
| CMP-003 | CheckInBookingCommandHandler | Application | Rooms | CMP-006, CMP-007 |  | MediatR |
| CMP-004 | ReleaseNoShowJob | Application | Rooms | CMP-006, CMP-007, CMP-008 |  | ASP.NET Core |
| CMP-005 | ListDailyBookingsQueryHandler | Application | Rooms | CMP-006, CMP-007 |  | MediatR |
| CMP-006 | Booking (Aggregate) | Domain | Rooms |  |  |  |
| CMP-007 | SqlRoomRepository : IRoomRepository | Infrastructure | Rooms |  |  | EF Core |
| CMP-008 | CalendarServiceClient : ICalendarService | Infrastructure | Rooms |  | CalendarService |  |

### C4-L3
```mermaid
flowchart LR
  CMP001["RoomsController<br/>Api"]
  CMP002["BookRoomCommandHandler<br/>Application"]
  CMP003["CheckInBookingCommandHandler<br/>Application"]
  CMP004["ReleaseNoShowJob<br/>Application"]
  CMP005["ListDailyBookingsQueryHandler<br/>Application"]
  CMP006["Booking (Aggregate)<br/>Domain"]
  CMP007["SqlRoomRepository<br/>Infrastructure"]
  CMP008["CalendarServiceClient<br/>Infrastructure"]
  CMP001 --> CMP002
  CMP001 --> CMP003
  CMP001 --> CMP005
  CMP002 --> CMP006
  CMP002 --> CMP007
  CMP002 --> CMP008
  CMP003 --> CMP006
  CMP003 --> CMP007
  CMP004 --> CMP006
  CMP004 --> CMP007
  CMP004 --> CMP008
  CMP005 --> CMP006
  CMP005 --> CMP007
```

## Traceability
| AC | CMP | via | Responsibility |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | receive the book request |
| AC-001-1 | CMP-002 | SEQ-001 | orchestrate book |
| AC-001-1 | CMP-006 | SEQ-001 | enforce the book invariant |
| AC-001-1 | CMP-007 | SEQ-001 | persist the book result |
| AC-001-1 | CMP-008 | SEQ-001 | call the external system for book |
| AC-001-2 | CMP-001 | SEQ-001 | receive the book request |
| AC-001-2 | CMP-002 | SEQ-001 | orchestrate book |
| AC-001-2 | CMP-006 | SEQ-001 | enforce the book invariant |
| AC-001-2 | CMP-007 | SEQ-001 | persist the book result |
| AC-001-2 | CMP-008 | SEQ-001 | call the external system for book |
| AC-002-1 | CMP-001 | SEQ-002 | receive the check in request |
| AC-002-1 | CMP-003 | SEQ-002 | orchestrate check in |
| AC-002-1 | CMP-006 | SEQ-002 | enforce the check in invariant |
| AC-002-1 | CMP-007 | SEQ-002 | persist the check in result |
| AC-002-1 | CMP-004 | SEQ-002 | orchestrate release |
| AC-002-1 | CMP-008 | SEQ-002 | call the external system for release |
| AC-002-2 | CMP-001 | SEQ-002 | receive the check in request |
| AC-002-2 | CMP-003 | SEQ-002 | orchestrate check in |
| AC-002-2 | CMP-006 | SEQ-002 | enforce the check in invariant |
| AC-002-2 | CMP-007 | SEQ-002 | persist the check in result |
| AC-002-2 | CMP-004 | SEQ-002 | orchestrate release |
| AC-002-2 | CMP-008 | SEQ-002 | call the external system for release |
| AC-003-1 | CMP-001 | SEQ-003 | receive the view request |
| AC-003-1 | CMP-005 | SEQ-003 | orchestrate view |
| AC-003-1 | CMP-006 | SEQ-003 | enforce the view invariant |
| AC-003-1 | CMP-007 | SEQ-003 | persist the view result |
| AC-N01-1 | CMP-001 | API-001 | NFR 100 concurrent → 1 success |

## Sequence
### SEQ-001 (UC-001 / REQ-001)
```mermaid
sequenceDiagram
  actor U as Employee
  participant CMP001 as RoomsController
  participant CMP002 as BookRoomCommandHandler
  participant CMP006 as Booking
  participant CMP007 as SqlRoomRepository
  participant CMP008 as CalendarServiceClient
  U->>CMP001: BookRoom
  CMP001->>CMP002: BookRoom
  CMP002->>CMP006: BookRoom
  CMP006-->>CMP002: ok
  CMP002->>CMP007: BookRoom
  CMP007-->>CMP002: ok
  CMP002->>CMP008: BookRoom
  CMP008-->>CMP002: ok
  CMP002-->>CMP001: ok
  CMP001-->>U: ok
```

### SEQ-002 (UC-002 / REQ-002)
```mermaid
sequenceDiagram
  actor U as Employee
  participant CMP001 as RoomsController
  participant CMP003 as CheckInBookingCommandHandler
  participant CMP006 as Booking
  participant CMP007 as SqlRoomRepository
  U->>CMP001: CheckInBooking
  CMP001->>CMP003: CheckInBooking
  CMP003->>CMP006: CheckInBooking
  CMP006-->>CMP003: ok
  CMP003->>CMP007: CheckInBooking
  CMP007-->>CMP003: ok
  CMP003-->>CMP001: ok
  CMP001-->>U: ok
```

### SEQ-003 (UC-003 / REQ-003)
```mermaid
sequenceDiagram
  actor U as Admin
  participant CMP001 as RoomsController
  participant CMP005 as ListDailyBookingsQueryHandler
  participant CMP006 as Booking
  participant CMP007 as SqlRoomRepository
  U->>CMP001: ListDailyBookings
  CMP001->>CMP005: ListDailyBookings
  CMP005->>CMP006: ListDailyBookings
  CMP006-->>CMP005: ok
  CMP005->>CMP007: ListDailyBookings
  CMP007-->>CMP005: ok
  CMP005-->>CMP001: ok
  CMP001-->>U: ok
```

