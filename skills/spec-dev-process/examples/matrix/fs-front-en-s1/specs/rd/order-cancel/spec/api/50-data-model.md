# Order cancellation and refund — data model

## Tables
### ERD-001
```mermaid
erDiagram
  Orders ||--o{ Refund : has
  Orders {
    uniqueidentifier Id PK
  }
  Refund {
    uniqueidentifier Id PK
  }
```

## Ownership
| Table | Owner Context | Access From Other Contexts |
|---|---|---|
| Orders | Orders | — |
| Refund | Orders | — |
