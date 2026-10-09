# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["the employee books the meeting room"] --> B{"the time slot is free?"}
  B -->|yes| C["a booking is booked"]
  B -->|no| D["the response is 409 SLOT_TAKEN"]
```

### ACT-002 (REQ-002)
```mermaid
flowchart TD
  A["the employee checks in within 15 minutes"] --> B{"a booking is booked?"}
  B -->|yes| C["the booking is checked-in"]
  B -->|no| D["the booking is released and the calendar service is updated"]
```

### ACT-003 (REQ-003)
```mermaid
flowchart TD
  A["the admin opens the daily view"] --> B{"booking records exist today?"}
  B -->|yes| C["rows are grouped by meeting room"]
  B -->|no| E["—"]
```

