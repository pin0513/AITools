# 會議室預約 — architecture (C4)

## Context(L1)
### C4-L1
```mermaid
C4Context
  Person(u, "employee")
  System(sys, "會議室預約")
  System_Ext(ext, "CalendarService")
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
| CMP-001 | RoomBookingPage | Page | Rooms | CMP-002, CMP-003, CMP-004, CMP-005 |  | React |
| CMP-002 | BookingForm | Component | Rooms | CMP-005 |  | React |
| CMP-003 | CheckInButton | Component | Rooms | CMP-005 |  | React |
| CMP-004 | DailyBookingTable | Component | Rooms | CMP-005 |  | React |
| CMP-005 | bookingStore | Store | Rooms | CMP-006 |  | Zustand |
| CMP-006 | roomsApi | ApiClient | Rooms | CMP-007 |  |  |
| CMP-007 | RoomsController | Api | Rooms | CMP-008, CMP-009, CMP-011 |  | ASP.NET Core |
| CMP-008 | BookRoomCommandHandler | Application | Rooms | CMP-012, CMP-013, CMP-014 |  | MediatR |
| CMP-009 | CheckInBookingCommandHandler | Application | Rooms | CMP-012, CMP-013 |  | MediatR |
| CMP-010 | ReleaseNoShowJob | Application | Rooms | CMP-012, CMP-013, CMP-014 |  | ASP.NET Core |
| CMP-011 | ListDailyBookingsQueryHandler | Application | Rooms | CMP-012, CMP-013 |  | MediatR |
| CMP-012 | Booking (Aggregate) | Domain | Rooms |  |  |  |
| CMP-013 | SqlRoomRepository : IRoomRepository | Infrastructure | Rooms |  |  | EF Core |
| CMP-014 | CalendarServiceClient : ICalendarService | Infrastructure | Rooms |  | CalendarService |  |

### C4-L3
```mermaid
flowchart LR
  CMP001["RoomBookingPage<br/>Page"]
  CMP002["BookingForm<br/>Component"]
  CMP003["CheckInButton<br/>Component"]
  CMP004["DailyBookingTable<br/>Component"]
  CMP005["bookingStore<br/>Store"]
  CMP006["roomsApi<br/>ApiClient"]
  CMP007["RoomsController<br/>Api"]
  CMP008["BookRoomCommandHandler<br/>Application"]
  CMP009["CheckInBookingCommandHandler<br/>Application"]
  CMP010["ReleaseNoShowJob<br/>Application"]
  CMP011["ListDailyBookingsQueryHandler<br/>Application"]
  CMP012["Booking (Aggregate)<br/>Domain"]
  CMP013["SqlRoomRepository<br/>Infrastructure"]
  CMP014["CalendarServiceClient<br/>Infrastructure"]
  CMP001 --> CMP002
  CMP001 --> CMP003
  CMP001 --> CMP004
  CMP001 --> CMP005
  CMP002 --> CMP005
  CMP003 --> CMP005
  CMP004 --> CMP005
  CMP005 --> CMP006
  CMP006 --> CMP007
  CMP007 --> CMP008
  CMP007 --> CMP009
  CMP007 --> CMP011
  CMP008 --> CMP012
  CMP008 --> CMP013
  CMP008 --> CMP014
  CMP009 --> CMP012
  CMP009 --> CMP013
  CMP010 --> CMP012
  CMP010 --> CMP013
  CMP010 --> CMP014
  CMP011 --> CMP012
  CMP011 --> CMP013
```

## 追溯(AC → 技術元件)
| AC | CMP | via | 職責 |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | 顯示並觸發book |
| AC-001-1 | CMP-002 | SEQ-001 | book的 UI 守衛 |
| AC-001-1 | CMP-005 | SEQ-001 | book的前端狀態轉移 |
| AC-001-1 | CMP-006 | SEQ-001 | 呼叫book API |
| AC-001-1 | CMP-007 | SEQ-001 | 接收book請求 |
| AC-001-1 | CMP-008 | SEQ-001 | 編排book |
| AC-001-1 | CMP-012 | SEQ-001 | book的業務規則與不變量 |
| AC-001-1 | CMP-013 | SEQ-001 | 持久化book結果 |
| AC-001-1 | CMP-014 | SEQ-001 | 為book呼叫外部系統 |
| AC-001-2 | CMP-001 | SEQ-001 | 顯示並觸發book |
| AC-001-2 | CMP-002 | SEQ-001 | book的 UI 守衛 |
| AC-001-2 | CMP-005 | SEQ-001 | book的前端狀態轉移 |
| AC-001-2 | CMP-006 | SEQ-001 | 呼叫book API |
| AC-001-2 | CMP-007 | SEQ-001 | 接收book請求 |
| AC-001-2 | CMP-008 | SEQ-001 | 編排book |
| AC-001-2 | CMP-012 | SEQ-001 | book的業務規則與不變量 |
| AC-001-2 | CMP-013 | SEQ-001 | 持久化book結果 |
| AC-001-2 | CMP-014 | SEQ-001 | 為book呼叫外部系統 |
| AC-002-1 | CMP-001 | SEQ-002 | 顯示並觸發check in |
| AC-002-1 | CMP-003 | SEQ-002 | check in的 UI 守衛 |
| AC-002-1 | CMP-005 | SEQ-002 | check in的前端狀態轉移 |
| AC-002-1 | CMP-006 | SEQ-002 | 呼叫check in API |
| AC-002-1 | CMP-007 | SEQ-002 | 接收check in請求 |
| AC-002-1 | CMP-009 | SEQ-002 | 編排check in |
| AC-002-1 | CMP-012 | SEQ-002 | check in的業務規則與不變量 |
| AC-002-1 | CMP-013 | SEQ-002 | 持久化check in結果 |
| AC-002-1 | CMP-010 | SEQ-002 | 編排release |
| AC-002-1 | CMP-014 | SEQ-002 | 為release呼叫外部系統 |
| AC-002-2 | CMP-001 | SEQ-002 | 顯示並觸發check in |
| AC-002-2 | CMP-003 | SEQ-002 | check in的 UI 守衛 |
| AC-002-2 | CMP-005 | SEQ-002 | check in的前端狀態轉移 |
| AC-002-2 | CMP-006 | SEQ-002 | 呼叫check in API |
| AC-002-2 | CMP-007 | SEQ-002 | 接收check in請求 |
| AC-002-2 | CMP-009 | SEQ-002 | 編排check in |
| AC-002-2 | CMP-012 | SEQ-002 | check in的業務規則與不變量 |
| AC-002-2 | CMP-013 | SEQ-002 | 持久化check in結果 |
| AC-002-2 | CMP-010 | SEQ-002 | 編排release |
| AC-002-2 | CMP-014 | SEQ-002 | 為release呼叫外部系統 |
| AC-003-1 | CMP-001 | SEQ-003 | 顯示並觸發view |
| AC-003-1 | CMP-004 | SEQ-003 | view的 UI 守衛 |
| AC-003-1 | CMP-005 | SEQ-003 | view的前端狀態轉移 |
| AC-003-1 | CMP-006 | SEQ-003 | 呼叫view API |
| AC-003-1 | CMP-007 | SEQ-003 | 接收view請求 |
| AC-003-1 | CMP-011 | SEQ-003 | 編排view |
| AC-003-1 | CMP-012 | SEQ-003 | view的業務規則與不變量 |
| AC-003-1 | CMP-013 | SEQ-003 | 持久化view結果 |
| AC-N01-1 | CMP-007 | API-001 | NFR 100 concurrent → 1 success |

## Sequence
### SEQ-001 (UC-001 / REQ-001)
```mermaid
sequenceDiagram
  actor U as Employee
  participant CMP001 as RoomBookingPage
  participant CMP002 as BookingForm
  participant CMP005 as bookingStore
  participant CMP006 as roomsApi
  participant CMP007 as RoomsController
  participant CMP008 as BookRoomCommandHandler
  participant CMP012 as Booking
  participant CMP013 as SqlRoomRepository
  participant CMP014 as CalendarServiceClient
  U->>CMP001: BookRoom
  CMP001->>CMP002: BookRoom
  CMP002->>CMP005: BookRoom
  CMP005->>CMP006: BookRoom
  CMP006->>CMP007: BookRoom
  CMP007->>CMP008: BookRoom
  CMP008->>CMP012: BookRoom
  CMP012-->>CMP008: ok
  CMP008->>CMP013: BookRoom
  CMP013-->>CMP008: ok
  CMP008->>CMP014: BookRoom
  CMP014-->>CMP008: ok
  CMP008-->>CMP007: ok
  CMP007-->>CMP006: ok
  CMP006-->>CMP005: ok
  CMP005-->>CMP002: ok
  CMP002-->>CMP001: ok
  CMP001-->>U: ok
```

### SEQ-002 (UC-002 / REQ-002)
```mermaid
sequenceDiagram
  actor U as Employee
  participant CMP001 as RoomBookingPage
  participant CMP003 as CheckInButton
  participant CMP005 as bookingStore
  participant CMP006 as roomsApi
  participant CMP007 as RoomsController
  participant CMP009 as CheckInBookingCommandHandler
  participant CMP012 as Booking
  participant CMP013 as SqlRoomRepository
  U->>CMP001: CheckInBooking
  CMP001->>CMP003: CheckInBooking
  CMP003->>CMP005: CheckInBooking
  CMP005->>CMP006: CheckInBooking
  CMP006->>CMP007: CheckInBooking
  CMP007->>CMP009: CheckInBooking
  CMP009->>CMP012: CheckInBooking
  CMP012-->>CMP009: ok
  CMP009->>CMP013: CheckInBooking
  CMP013-->>CMP009: ok
  CMP009-->>CMP007: ok
  CMP007-->>CMP006: ok
  CMP006-->>CMP005: ok
  CMP005-->>CMP003: ok
  CMP003-->>CMP001: ok
  CMP001-->>U: ok
```

### SEQ-003 (UC-003 / REQ-003)
```mermaid
sequenceDiagram
  actor U as Admin
  participant CMP001 as RoomBookingPage
  participant CMP004 as DailyBookingTable
  participant CMP005 as bookingStore
  participant CMP006 as roomsApi
  participant CMP007 as RoomsController
  participant CMP011 as ListDailyBookingsQueryHandler
  participant CMP012 as Booking
  participant CMP013 as SqlRoomRepository
  U->>CMP001: ListDailyBookings
  CMP001->>CMP004: ListDailyBookings
  CMP004->>CMP005: ListDailyBookings
  CMP005->>CMP006: ListDailyBookings
  CMP006->>CMP007: ListDailyBookings
  CMP007->>CMP011: ListDailyBookings
  CMP011->>CMP012: ListDailyBookings
  CMP012-->>CMP011: ok
  CMP011->>CMP013: ListDailyBookings
  CMP013-->>CMP011: ok
  CMP011-->>CMP007: ok
  CMP007-->>CMP006: ok
  CMP006-->>CMP005: ok
  CMP005-->>CMP004: ok
  CMP004-->>CMP001: ok
  CMP001-->>U: ok
```

