# 會員點數兌換 — data model

## 資料表
### ERD-001
```mermaid
erDiagram
  PointsAccounts ||--o{ Redemption : has
  PointsAccounts {
    uniqueidentifier Id PK
  }
  Redemption {
    uniqueidentifier Id PK
  }
```

## 擁有權
| 表 | Owner Context | 其他 Context 存取方式 |
|---|---|---|
| PointsAccounts | Loyalty | — |
| Redemption | Loyalty | — |
