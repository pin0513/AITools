# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["employee book Room"] --> B{"TimeSlot 空閒?"}
  B -->|yes| C["Booking 狀態為 Booked"]
  B -->|no| D["回應 409 SLOT_TAKEN"]
```
