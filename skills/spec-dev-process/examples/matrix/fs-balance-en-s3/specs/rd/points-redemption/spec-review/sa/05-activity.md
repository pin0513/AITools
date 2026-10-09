# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["the member redeems it"] --> B{"the balance covers the reward?"}
  B -->|yes| C["a redemption is created and the reward vendor is called"]
  B -->|no| D["the response is 422 INSUFFICIENT_POINTS and nothing is deducted"]
```
