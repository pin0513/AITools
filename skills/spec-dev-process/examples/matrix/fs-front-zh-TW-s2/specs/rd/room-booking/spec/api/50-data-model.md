# 會議室預約 — data model

## 資料表
### ERD-001
```mermaid
erDiagram
  Rooms ||--o{ Booking : has
  Rooms {
    uniqueidentifier Id PK
  }
  Booking {
    uniqueidentifier Id PK
  }
```

## 擁有權
| 表 | Owner Context | 其他 Context 存取方式 |
|---|---|---|
| Rooms | Rooms | — |
| Booking | Rooms | — |
