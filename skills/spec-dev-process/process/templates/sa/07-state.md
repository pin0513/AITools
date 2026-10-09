# {feature-title} SA7 State Diagram

## State Diagram
### STM-SA-001 {實體}.Status(REQ-001)
```mermaid
stateDiagram-v2
  [*] --> Created
  Created --> Cancelled: Cancel
  Cancelled --> [*]
```
