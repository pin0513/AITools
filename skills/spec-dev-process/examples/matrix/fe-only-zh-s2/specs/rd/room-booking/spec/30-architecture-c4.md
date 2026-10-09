# 會議室預約 — architecture (C4)

## Context(L1)
### C4-L1
```mermaid
C4Context
  Person(u, "員工")
  System(sys, "會議室預約")
  System_Ext(ext, "BackendAPI")
  Rel(u, sys, "use")
  Rel(sys, ext, "call")
```

## Container(L2)
### C4-L2
```mermaid
C4Container
  Container(web, "Web", "React", "")
```

## Component(L3)
| ID | 名稱 | Layer | Context | depends | external | 技術 |
|---|---|---|---|---|---|---|
| CMP-001 | RoomBookingPage | Page | Rooms | CMP-002, CMP-003, CMP-004, CMP-005 |  | React |
| CMP-002 | BookingForm | Component | Rooms | CMP-005 |  | React |
| CMP-003 | CheckInButton | Component | Rooms | CMP-005 |  | React |
| CMP-004 | DailyBookingTable | Component | Rooms | CMP-005 |  | React |
| CMP-005 | bookingStore | Store | Rooms | CMP-006 |  | Zustand |
| CMP-006 | roomsApi | ApiClient | Rooms |  | BackendAPI |  |

### C4-L3
```mermaid
flowchart LR
  CMP001["RoomBookingPage<br/>Page"]
  CMP002["BookingForm<br/>Component"]
  CMP003["CheckInButton<br/>Component"]
  CMP004["DailyBookingTable<br/>Component"]
  CMP005["bookingStore<br/>Store"]
  CMP006["roomsApi<br/>ApiClient"]
  CMP001 --> CMP002
  CMP001 --> CMP003
  CMP001 --> CMP004
  CMP001 --> CMP005
  CMP002 --> CMP005
  CMP003 --> CMP005
  CMP004 --> CMP005
  CMP005 --> CMP006
```

## 追溯(AC → 技術元件)
| AC | CMP | via | 職責 |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | 顯示並觸發預約 |
| AC-001-1 | CMP-002 | SEQ-001 | 預約的 UI 守衛 |
| AC-001-1 | CMP-005 | SEQ-001 | 預約的前端狀態轉移 |
| AC-001-1 | CMP-006 | SEQ-001 | 呼叫預約 API |
| AC-001-2 | CMP-001 | SEQ-001 | 顯示並觸發預約 |
| AC-001-2 | CMP-002 | SEQ-001 | 預約的 UI 守衛 |
| AC-001-2 | CMP-005 | SEQ-001 | 預約的前端狀態轉移 |
| AC-001-2 | CMP-006 | SEQ-001 | 呼叫預約 API |
| AC-002-1 | CMP-001 | SEQ-002 | 顯示並觸發報到 |
| AC-002-1 | CMP-003 | SEQ-002 | 報到的 UI 守衛 |
| AC-002-1 | CMP-005 | SEQ-002 | 報到的前端狀態轉移 |
| AC-002-1 | CMP-006 | SEQ-002 | 呼叫報到 API |
| AC-002-2 | CMP-001 | SEQ-002 | 顯示並觸發報到 |
| AC-002-2 | CMP-003 | SEQ-002 | 報到的 UI 守衛 |
| AC-002-2 | CMP-005 | SEQ-002 | 報到的前端狀態轉移 |
| AC-002-2 | CMP-006 | SEQ-002 | 呼叫報到 API |
| AC-003-1 | CMP-001 | SEQ-003 | 顯示並觸發查看 |
| AC-003-1 | CMP-004 | SEQ-003 | 查看的 UI 守衛 |
| AC-003-1 | CMP-005 | SEQ-003 | 查看的前端狀態轉移 |
| AC-003-1 | CMP-006 | SEQ-003 | 呼叫查看 API |
| AC-N01-1 | CMP-006 | API-001 | NFR 100 concurrent → 1 success |

## Sequence
### SEQ-001 (UC-001 / REQ-001)
```mermaid
sequenceDiagram
  actor U as Employee
  participant CMP001 as RoomBookingPage
  participant CMP002 as BookingForm
  participant CMP005 as bookingStore
  participant CMP006 as roomsApi
  U->>CMP001: BookRoom
  CMP001->>CMP002: BookRoom
  CMP002->>CMP005: BookRoom
  CMP005->>CMP006: BookRoom
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
  U->>CMP001: CheckInBooking
  CMP001->>CMP003: CheckInBooking
  CMP003->>CMP005: CheckInBooking
  CMP005->>CMP006: CheckInBooking
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
  U->>CMP001: ListDailyBookings
  CMP001->>CMP004: ListDailyBookings
  CMP004->>CMP005: ListDailyBookings
  CMP005->>CMP006: ListDailyBookings
  CMP001-->>U: ok
```

