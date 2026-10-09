# SA4 Use Case Diagram

## Use Case Diagram
### UCD-001 (REQ-001)
```mermaid
flowchart LR
  employee(["employee"]) --> book(("book"))
  employee(["employee"]) --> check_in(("check in"))
  system(["system"]) --> release(("release"))
  admin(["admin"]) --> view_daily(("view"))
```
