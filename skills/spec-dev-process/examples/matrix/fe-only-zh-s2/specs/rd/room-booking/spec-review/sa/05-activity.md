# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["員工預約會議室"] --> B{"時段空閒?"}
  B -->|yes| C["預約單狀態為已預約"]
  B -->|no| D["回應 409 SLOT_TAKEN"]
```
