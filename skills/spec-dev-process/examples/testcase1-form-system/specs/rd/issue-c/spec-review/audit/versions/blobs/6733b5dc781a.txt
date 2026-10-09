# 表單審核流程 — 架構(C4)

## Context(L1)
### C4-L1
```mermaid
C4Context
  Person(sub, "填寫者")
  Person(rev, "審核者")
  System(sys, "表單系統")
  System_Ext(smtp, "SMTP")
  Rel(sub, sys, "送審、重送")
  Rel(rev, sys, "核准、退回")
  Rel(sys, smtp, "退回通知、逾時提醒", "INotifier")
```

## Container(L2)
### C4-L2
```mermaid
C4Container
  Container(web, "Forms Web", "React", "FormFill(modify)、ReviewPanel(new)")
  Container(api, "Forms API", ".NET 8", "Api/Application/Domain/Infrastructure")
  Container(job, "ReviewReminderJob", ".NET Hosted Service", "每日 09:00")
  ContainerDb(db, "SQL Server", "", "Form, FormSubmission, ReviewRecord, ReviewReminder")
  System_Ext(smtp, "SMTP", "")
  Rel(web, api, "HTTPS")
  Rel(api, db, "EF Core")
  Rel(job, db, "EF Core")
  Rel(api, smtp, "INotifier")
  Rel(job, smtp, "INotifier")
```

## Component(L3)
survey 狀態:existing 沿用、modify 既有修改、new 新增(見 spec-review/survey-mapping.md)。

| ID | 名稱 | Layer | Context | depends | external | 技術 |
|---|---|---|---|---|---|---|
| CMP-001 | SubmissionsController(new) | Api | Forms | CMP-002, CMP-003, CMP-004, CMP-009 | | ASP.NET Core |
| CMP-002 | ApproveSubmissionCommandHandler(new) | Application | Forms | CMP-005, CMP-006 | | MediatR |
| CMP-003 | RejectSubmissionCommandHandler(new) | Application | Forms | CMP-005, CMP-006, CMP-007 | | MediatR |
| CMP-004 | ResubmitSubmissionCommandHandler(new) | Application | Forms | CMP-005, CMP-006 | | MediatR |
| CMP-005 | FormSubmission (Aggregate, modify) | Domain | Forms | | | |
| CMP-006 | SqlFormSubmissionRepository : IFormSubmissionRepository(modify) | Infrastructure | Forms | | | EF Core |
| CMP-007 | EmailNotifier : INotifier(existing) | Infrastructure | Forms | | SMTP | |
| CMP-008 | ReviewReminderJob(new) | Application | Forms | CMP-005, CMP-006, CMP-007, CMP-010 | | ASP.NET Core |
| CMP-009 | PendingReviewsQueryHandler(new) | Application | Forms | CMP-006 | | MediatR |
| CMP-010 | WorkdayCalendar : IWorkdayCalendar(new) | Infrastructure | Forms | | | |

### C4-L3
```mermaid
C4Component
  Component(c1, "SubmissionsController", "Api")
  Component(c2, "ApproveSubmissionCommandHandler", "Application")
  Component(c3, "RejectSubmissionCommandHandler", "Application")
  Component(c4, "ResubmitSubmissionCommandHandler", "Application")
  Component(c9, "PendingReviewsQueryHandler", "Application")
  Component(c8, "ReviewReminderJob", "Application")
  Component(c5, "FormSubmission", "Domain")
  Component(c6, "SqlFormSubmissionRepository", "Infrastructure", "IFormSubmissionRepository")
  Component(c7, "EmailNotifier", "Infrastructure", "INotifier")
  Component(c10, "WorkdayCalendar", "Infrastructure", "IWorkdayCalendar")
  Rel(c1, c2, "Send")
  Rel(c1, c3, "Send")
  Rel(c1, c4, "Send")
  Rel(c1, c9, "Send")
  Rel(c2, c5, "Approve")
  Rel(c3, c5, "Reject")
  Rel(c4, c5, "Resubmit")
  Rel(c2, c6, "")
  Rel(c3, c6, "")
  Rel(c4, c6, "")
  Rel(c9, c6, "")
  Rel(c3, c7, "notify submitter")
  Rel(c8, c6, "ListOverdue")
  Rel(c8, c7, "remind")
  Rel(c8, c10, "workdays")
```

## 追溯(AC → 技術元件)
| AC | CMP | via | 職責 |
|---|---|---|---|
| AC-001-1 | CMP-005 | STM-DOM-001 | Submit 設 Status=Pending(既有 Create 改) |
| AC-001-2 | CMP-004 | UC-003 | Pending 時拒絕修改 → 409 |
| AC-001-2 | CMP-005 | STM-DOM-001 | 守衛:只有 Rejected 可 Resubmit |
| AC-002-1 | CMP-001 | SEQ-001 | POST approve,取 actor |
| AC-002-1 | CMP-002 | SEQ-001 | 編排:載入、審核者檢查、Approve、儲存 |
| AC-002-1 | CMP-005 | SEQ-001 | Approve:狀態轉移 + ReviewRecord |
| AC-002-1 | CMP-006 | SEQ-001 | 持久化 ReviewRecord |
| AC-002-2 | CMP-005 | SEQ-001 | Reject 守衛 reason.Length ≥ 10 |
| AC-002-2 | CMP-001 | SEQ-001 | DomainException → 400 REASON_TOO_SHORT |
| AC-002-3 | CMP-003 | SEQ-001 | 編排:Reject、儲存、發 SubmissionRejected |
| AC-002-3 | CMP-005 | SEQ-001 | Reject:Rejected + ReviewRecord + 事件 |
| AC-002-3 | CMP-007 | SEQ-001 | 通知填寫者 |
| AC-003-1 | CMP-004 | UC-003 | 編排:驗答案、Resubmit、儲存 |
| AC-003-1 | CMP-005 | STM-DOM-001 | Resubmit:Rejected → Pending,ResubmitCount++ |
| AC-003-2 | CMP-005 | STM-DOM-001 | Approved 不可 Resubmit → 409 |
| AC-004-1 | CMP-008 | SEQ-002 | 每日:查逾時、排除已提醒、通知、寫 ReviewReminder |
| AC-004-1 | CMP-010 | SEQ-002 | 工作天計算(缺口 #3) |
| AC-004-1 | CMP-006 | SEQ-002 | ListOverdueAsync |
| AC-004-1 | CMP-007 | SEQ-002 | 發提醒 |
| AC-004-2 | CMP-005 | SEQ-002 | ReviewReminder (ReviewerId, Date) 唯一 |
| AC-004-2 | CMP-008 | SEQ-002 | 排除今日已提醒 |
| AC-N01-1 | CMP-001 | API-002 | 回應時間量測點 |
| AC-N02-1 | CMP-006 | ERD-001 | 無 Delete/Update 方法;DB 觸發器拒絕 |
| AC-N03-1 | CMP-002 | SEQ-001 | 非審核者 → 403 |
| AC-N03-1 | CMP-003 | SEQ-001 | 非審核者 → 403 |

## Sequence
### SEQ-001 審核(UC-002 / REQ-002)
```mermaid
sequenceDiagram
  actor R as Reviewer
  participant C as SubmissionsController
  participant H as RejectSubmissionCommandHandler
  participant Repo as IFormSubmissionRepository
  participant S as FormSubmission
  participant N as INotifier
  R->>C: POST /submissions/{id}/reject {reason}
  C->>H: Send(RejectSubmissionCommand)
  H->>Repo: GetAsync(id)
  alt Status != Pending
    H-->>C: InvalidState
    C-->>R: 409
  else actor not in Form.ReviewerIds
    H-->>C: Forbidden
    C-->>R: 403
  else
    H->>S: Reject(actor, reason)
    alt reason < 10
      S-->>H: DomainException REASON_TOO_SHORT
      C-->>R: 400
    else
      S-->>H: SubmissionRejected
      H->>Repo: SaveAsync
      H->>N: NotifyAsync(submitter, "rejected")
      C-->>R: 200
    end
  end
```

### SEQ-002 逾時提醒(UC-004 / REQ-004)
```mermaid
sequenceDiagram
  participant J as ReviewReminderJob
  participant W as IWorkdayCalendar
  participant Repo as IFormSubmissionRepository
  participant S as FormSubmission
  participant N as INotifier
  J->>W: Subtract(today, 3)
  J->>Repo: ListOverdueAsync(cutoff)
  loop each submission
    J->>S: RemindersDueToday(reviewerIds, today)
    loop each reviewer not yet reminded
      J->>N: NotifyAsync(reviewer, "overdue")
      alt notify fails
        J->>J: log, skip reminder record
      else
        J->>S: AddReminder(reviewer, today)
      end
    end
    J->>Repo: SaveAsync
  end
```
