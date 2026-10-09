# Loyalty points redemption — data model

## Tables
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

## Ownership
| Table | Owner Context | Access From Other Contexts |
|---|---|---|
| PointsAccounts | Loyalty | — |
| Redemption | Loyalty | — |
