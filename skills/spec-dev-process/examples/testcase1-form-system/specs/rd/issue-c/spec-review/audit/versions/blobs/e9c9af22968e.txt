# 架構概觀
Clean Architecture 四層:Forms.Api(Controller)→ Forms.Application(MediatR Handler)→ Forms.Domain(Aggregate)← Forms.Infrastructure(EF Core Repository、Notifier)。
單一 Bounded Context:Forms。資料庫 SQL Server;前端 React。外部系統只有 SMTP(經 `INotifier`)。
