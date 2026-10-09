# 表單審核流程 — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 7 · 技術元件 10 · 測試元件 11 · 技術邊界 PASS 43/43 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | · | CMP-004 | CMP-005 | · | TST-001, TST-004 | · | · | · | ✓ |
| REQ-002 | CMP-001 | CMP-002, CMP-003 | CMP-005 | CMP-006, CMP-007 | TST-001, TST-002, TST-003, TST-009 | TST-005 | TST-008 | · | ⚠ |
| REQ-003 | · | CMP-004 | CMP-005 | · | TST-001, TST-004 | · | · | · | ✓ |
| REQ-004 | · | CMP-008 | CMP-005 | CMP-006, CMP-007, CMP-010 | TST-001, TST-006, TST-010 | TST-007 | TST-008 | · | ⚠ |
| NFR-001 | CMP-001 | · | · | · | · | TST-005 | · | TST-011 | ⚠ |
| NFR-002 | · | · | CMP-005 | CMP-006 | · | TST-007 | · | · | ✓ |
| NFR-003 | · | CMP-002, CMP-003 | · | · | TST-002, TST-003 | · | · | · | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-005(Submit 設 Status=Pending(既有 Create 改)) | TST-001 |
| AC-001-2 | REQ-001 | CMP-004(Pending 時拒絕修改 → 409), CMP-005(守衛:只有 Rejected 可 Resubmit) | TST-001, TST-004 |
| AC-002-1 | REQ-002 | CMP-001(POST approve,取 actor), CMP-002(編排:載入、審核者檢查、Approve、儲存), CMP-005(Approve:狀態轉移 + ReviewRecord), CMP-006(持久化 ReviewRecord) | TST-001, TST-002, TST-005, TST-009 |
| AC-002-2 | REQ-002 | CMP-005(Reject 守衛 reason.Length ≥ 10), CMP-001(DomainException → 400 REASON_TOO_SHORT) | TST-001, TST-003, TST-005 |
| AC-002-3 | REQ-002 | CMP-003(編排:Reject、儲存、發 SubmissionRejected), CMP-005(Reject:Rejected + ReviewRecord + 事件), CMP-007(通知填寫者) | TST-001, TST-003, TST-008 |
| AC-003-1 | REQ-003 | CMP-004(編排:驗答案、Resubmit、儲存), CMP-005(Resubmit:Rejected → Pending,ResubmitCount++) | TST-001, TST-004 |
| AC-003-2 | REQ-003 | CMP-005(Approved 不可 Resubmit → 409) | TST-001, TST-004 |
| AC-004-1 | REQ-004 | CMP-008(每日:查逾時、排除已提醒、通知、寫 ReviewReminder), CMP-010(工作天計算(缺口 #3)), CMP-006(ListOverdueAsync), CMP-007(發提醒) | TST-006, TST-007, TST-008, TST-010 |
| AC-004-2 | REQ-004 | CMP-005(ReviewReminder (ReviewerId, Date) 唯一), CMP-008(排除今日已提醒) | TST-001, TST-006 |
| AC-N01-1 | NFR-001 | CMP-001(回應時間量測點) | TST-005, TST-011 |
| AC-N02-1 | NFR-002 | CMP-006(無 Delete/Update 方法;DB 觸發器拒絕) | TST-007 |
| AC-N03-1 | NFR-003 | CMP-002(非審核者 → 403), CMP-003(非審核者 → 403) | TST-002, TST-003 |

## Gate 問題

| 等級 | 規則 | 訊息 |
|---|---|---|
| INFO | G-SA-steps | SA0 sa/00-lexicon.md 齊全(0 張圖) |
| INFO | G-SA-steps | SA1 sa/01-break-words.md 齊全(0 張圖) |
| INFO | G-SA-steps | SA2 sa/02-entities-relations.md 齊全(1 張圖) |
| INFO | G-SA-steps | SA3 sa/03-roles.md 齊全(0 張圖) |
| INFO | G-SA-steps | SA4 sa/04-usecase.md 齊全(1 張圖) |
| INFO | G-SA-steps | SA5 sa/05-activity.md 齊全(1 張圖) |
| INFO | G-SA-steps | SA6 sa/06-sequence.md 齊全(1 張圖) |
| INFO | G-SA-steps | SA7 sa/07-state.md 齊全(1 張圖) |
| INFO | G-GL-consistency | 「表單」→ Form 與 issue-b 一致 |
| INFO | G-GL-consistency | 「填寫紀錄」→ FormSubmission 與 issue-b 一致 |
| INFO | G-SV-evidence | Form → src/api/Forms.Domain/Form.cs:6 已驗證(符號 Form) |
| INFO | G-SV-evidence | FormSubmission → src/api/Forms.Domain/FormSubmission.cs:4 已驗證(符號 FormSubmission) |
| INFO | G-SV-evidence | 必填檢查 → src/api/Forms.Domain/FormSubmission.cs:16 "FIELD_REQUIRED" 已驗證(字面 "FIELD_REQUIRED") |
| INFO | G-SV-evidence | 填寫紀錄 → src/database/002_submissions.sql:2 已驗證(glossary 解析 FormSubmission) |
| INFO | G-SV-evidence | Submit (SubmitFormCommandHandler) → src/api/Forms.Api/Controllers/FormsController.cs:16 已驗證(符號 Submit) |
| INFO | G-SV-evidence | Submit (SubmitFormCommandHandler) → src/api/Forms.Application/Forms/SubmitFormCommandHandler.cs:8 已驗證(符號 SubmitFormCommandHandler) |
| INFO | G-SV-evidence | INotifier → src/api/Forms.Infrastructure/EmailNotifier.cs:4 已驗證(符號 INotifier) |
| INFO | G-SV-evidence | IFormSubmissionRepository → src/api/Forms.Domain/IFormRepository.cs:10 已驗證(符號 IFormSubmissionRepository) |
| INFO | G-SV-evidence | SqlFormSubmissionRepository → src/api/Forms.Infrastructure/SqlFormRepository.cs:14 已驗證(符號 SqlFormSubmissionRepository) |
| INFO | G-SV-evidence | FormsDbContext → src/api/Forms.Infrastructure/Persistence/FormsDbContext.cs:6 已驗證(符號 FormsDbContext) |
| INFO | G-SV-evidence | FormSubmission table → src/database/002_submissions.sql:2 已驗證(符號 FormSubmission) |
| INFO | G-SV-evidence | FormFill → src/web/src/pages/FormFill.tsx:2 已驗證(符號 FormFill) |
| INFO | G-SV-evidence | submitForm → src/web/src/api/client.ts:4 已驗證(符號 submitForm) |
| WARN | G-M-assumed | REQ-002 S1 UseCase 證據=assumed:審核者指派方式 PM 未展開 |
| WARN | G-M-assumed | REQ-002 S2 Contract 證據=assumed:PM 未明寫退回通知 |
| WARN | G-M-assumed | REQ-004 S1 QualityScenario 證據=assumed:工作天是否含國定假日 |
| WARN | G-M-assumed | NFR-001 S1 QualityScenario 證據=assumed:沒有數字 |
