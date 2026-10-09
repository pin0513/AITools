# SA4 Use Case Diagram

## Use Case Diagram
### UCD-001 (REQ-001, REQ-002, REQ-003)
```mermaid
flowchart LR
  customer(["customer"]) --> cancel(("cancel"))
  system(["system"]) --> issue_refund(("refund"))
  support_agent(["support agent"]) --> view_history(("view"))
```
