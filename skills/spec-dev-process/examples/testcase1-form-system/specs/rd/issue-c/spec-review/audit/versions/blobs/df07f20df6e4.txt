# 開發規範
- 狀態機放 Domain,用 enum + 方法轉移;Handler 不得直接改狀態欄位。
- 新 API 走 MediatR Command/Query;Controller 不含業務邏輯。
- 每個 Aggregate 一個 Repository 介面(定義在 Domain),Infrastructure 實作。
- 通知一律經 `INotifier`,不直接呼叫 SMTP。
