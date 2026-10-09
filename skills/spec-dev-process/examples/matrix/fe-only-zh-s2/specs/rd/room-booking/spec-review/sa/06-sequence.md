# SA6 Sequence Diagram

## Sequence Diagram
### SEQ-SA-001 (REQ-001)
```mermaid
sequenceDiagram
  actor U as Employee
  participant Web
  participant BackendAPI
  U->>Web: BookRoom
  Web->>BackendAPI: BookRoom
  Web-->>U: ok
```
