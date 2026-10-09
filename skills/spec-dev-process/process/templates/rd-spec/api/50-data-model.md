# {feature-title} — 資料模型

## 資料表
### ERD-001
```mermaid
erDiagram
  Foo {
    uniqueidentifier Id PK
    nvarchar Name
    datetime2 UpdatedAt
  }
```

| 表 | 欄位 | 型別 | 鍵/索引 | 說明 |
|---|---|---|---|---|

## 擁有權
<!-- erDiagram 裡每個實體都要有一列且唯一 owner(B5) -->
| 表 | Owner Context | 其他 Context 存取方式 |
|---|---|---|
| Foo | Foo | 經 API-001 |

## 遷移
- 新增表/欄位:
- 既有資料處理:
- 保留期:
