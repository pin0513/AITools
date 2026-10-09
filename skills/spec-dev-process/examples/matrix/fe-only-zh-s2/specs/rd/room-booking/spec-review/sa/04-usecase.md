# SA4 Use Case Diagram

## Use Case Diagram
### UCD-001 (REQ-001, REQ-002, REQ-003)
```mermaid
flowchart LR
  employee(["員工"]) --> book(("預約"))
  employee(["員工"]) --> check_in(("報到"))
  system(["系統"]) --> release(("釋放"))
  admin(["管理員"]) --> view_daily(("查看"))
```
