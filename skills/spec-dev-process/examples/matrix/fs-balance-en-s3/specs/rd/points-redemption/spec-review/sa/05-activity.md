# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["the member redeems it"] --> B{"the balance covers the reward?"}
  B -->|yes| C["a redemption is created and the reward vendor is called"]
  B -->|no| D["the response is 422 INSUFFICIENT_POINTS and nothing is deducted"]
```

### ACT-002 (REQ-002)
```mermaid
flowchart TD
  A["the monthly job runs"] --> B{"points were earned 13 months ago?"}
  B -->|yes| C["an expiry points transaction is written and the balance drops"]
  B -->|no| E["—"]
```

### ACT-003 (REQ-003)
```mermaid
flowchart TD
  A["the member opens the history"] --> B{"the member has a points transaction?"}
  B -->|yes| C["each points transaction shows date, type and points"]
  B -->|no| E["—"]
```

