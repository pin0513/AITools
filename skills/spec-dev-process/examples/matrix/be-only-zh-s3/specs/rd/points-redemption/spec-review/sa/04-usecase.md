# SA4 Use Case Diagram

## Use Case Diagram
### UCD-001 (REQ-001)
```mermaid
flowchart LR
  member(["會員"]) --> redeem(("兌換"))
  system(["系統"]) --> expire(("到期"))
  member(["會員"]) --> view_tx(("查看"))
```
