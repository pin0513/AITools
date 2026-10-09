# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["員工預約會議室"] --> B{"時段空閒?"}
  B -->|yes| C["預約單狀態為已預約"]
  B -->|no| D["回應 409 SLOT_TAKEN"]
```

### ACT-002 (REQ-002)
```mermaid
flowchart TD
  A["員工在 15 分鐘內報到"] --> B{"預約單狀態為已預約?"}
  B -->|yes| C["預約單狀態為已報到"]
  B -->|no| D["預約單狀態為已釋放,行事曆服務已更新"]
```

### ACT-003 (REQ-003)
```mermaid
flowchart TD
  A["管理員開啟每日檢視"] --> B{"今天有預約單?"}
  B -->|yes| C["依會議室分組顯示"]
  B -->|no| E["—"]
```

