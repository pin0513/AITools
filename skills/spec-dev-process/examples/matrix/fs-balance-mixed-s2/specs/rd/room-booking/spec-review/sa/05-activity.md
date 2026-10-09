# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["employee book Room"] --> B{"TimeSlot 空閒?"}
  B -->|yes| C["Booking 狀態為 Booked"]
  B -->|no| D["回應 409 SLOT_TAKEN"]
```

### ACT-002 (REQ-002)
```mermaid
flowchart TD
  A["employee 在 15 分鐘內 check in"] --> B{"Booking 狀態為 Booked?"}
  B -->|yes| C["Booking 狀態為 CheckedIn"]
  B -->|no| D["Booking 狀態為 Released, CalendarService 已更新"]
```

### ACT-003 (REQ-003)
```mermaid
flowchart TD
  A["admin 開啟每日檢視"] --> B{"今天有 Booking?"}
  B -->|yes| C["依 Room 分組顯示"]
  B -->|no| E["—"]
```

