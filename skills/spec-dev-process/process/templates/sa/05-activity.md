# {feature-title} SA5 Activity Diagram

## Activity Diagram
### ACT-001 {流程名}(REQ-001)
```mermaid
flowchart TD
  A[開始] --> B{可取消?}
  B -->|是| C[Status=Cancelled] --> D([結束])
  B -->|否| E[409]
```
