# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["the employee books the meeting room"] --> B{"the time slot is free?"}
  B -->|yes| C["a booking is booked"]
  B -->|no| D["the response is 409 SLOT_TAKEN"]
```
