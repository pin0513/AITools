# issue-c SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)

來源:pm_spec:pm-spec.md, mock:approval.html, ref:refs.md, ref:overview.md, ref:coding.md · CJK 候選 325 → 邊界熵後 111 → 去冗後 104

規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。

## 名詞候選

| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |
|---|---|---|---|---|---|---|
| 紀錄 | 10 | 14.0 |  | — | 升 | mock:approval.html pm_spec:pm-spec.md§3.1 送審 pm_spec:pm-spec.md§3.2 審核 pm_spec:pm-spec.md§3.3 退回後重送 |
| 表單 | 6 | 9.0 | Form | 5 (src/database/002_submissions.sql:4) | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 送審 pm_spec:pm-spec.md§4 非功能需求 |
| 審核紀錄 | 5 | 8.0 | ReviewRecord | 0 | 升 | mock:approval.html pm_spec:pm-spec.md§3.2 審核 pm_spec:pm-spec.md§4 非功能需求 pm_spec:pm-spec.md§5 驗收條件 |
| 理由 | 5 | 8.0 |  | — | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 審核 pm_spec:pm-spec.md§5 驗收條件 |
| 工作天 | 3 | 4.0 |  | — | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§3.4 逾時提醒 pm_spec:pm-spec.md§5 驗收條件 |
| 狀態 | 5 | 3.6 |  | — | 升 | pm_spec:pm-spec.md§5 驗收條件 ref:coding.md§開發規範 ref:refs.md§issue-c 參考文件 |
| 填理由 | 2 | 3.0 |  | — | 升 | pm_spec:pm-spec.md§3.2 審核 pm_spec:pm-spec.md§5 驗收條件 |
| 待審核紀錄 | 2 | 3.0 |  | — | 升 | pm_spec:pm-spec.md§3.2 審核 pm_spec:pm-spec.md§5 驗收條件 |
| 送出表單 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 送審 |
| 填寫紀錄 | 2 | 2.0 | FormSubmission | 5 (src/database/002_submissions.sql:2) | 升 | mock:approval.html pm_spec:pm-spec.md§3.1 送審 |
| 部門 | 2 | 2.0 |  | — | 降 | mock:approval.html pm_spec:pm-spec.md§1 背景與目標 |
| 外部系統只 | 2 | 0.8 |  | — | 降 | ref:overview.md§架構概觀 ref:refs.md§issue-c 參考文件 |
| 改狀態 | 2 | 0.8 |  | — | 降 | ref:coding.md§開發規範 ref:refs.md§issue-c 參考文件 |
| 狀態機放 | 2 | 0.8 |  | — | 降 | ref:coding.md§開發規範 ref:refs.md§issue-c 參考文件 |

## 動作候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| 審核 | 26 | 42.0 | 升 | mock:approval.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 送審 |
| 退回 | 9 | 12.0 | 升 | mock:approval.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 審核 pm_spec:pm-spec.md§3.3 退回後重送 |
| 送出 | 8 | 11.0 | 升 | mock:approval.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 送審 |
| 填寫 | 7 | 8.0 | 升 | mock:approval.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 送審 |
| 核准 | 6 | 8.0 | 升 | mock:approval.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 審核 pm_spec:pm-spec.md§3.3 退回後重送 |
| 修改 | 5 | 6.0 | 升 | mock:approval.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 送審 pm_spec:pm-spec.md§3.3 退回後重送 |
| 提醒 | 3 | 5.0 | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.4 逾時提醒 pm_spec:pm-spec.md§5 驗收條件 |
| 以審核 | 1 | 3.0 | 降 | pm_spec:pm-spec.md§4 非功能需求 |
| 指派 | 1 | 3.0 | 降 | pm_spec:pm-spec.md§4 非功能需求 |
| 重新送出 | 2 | 2.0 | 升 | mock:approval.html pm_spec:pm-spec.md§3.3 退回後重送 |
| 修改後重送 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 |
| 想知道審核 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 |
| 狀態顯示 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§5 驗收條件 |
| 單填寫送出 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |
| 填寫者送出 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.1 送審 |
| 天提醒審核 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.4 逾時提醒 |
| 平均處理 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |
| 核期間填寫 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.1 送審 |
| 求送出 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |
| 王審核 | 1 | 1.0 | 降 | mock:approval.html |
| 經審核 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |
| 通知 | 2 | 0.8 | 降 | ref:coding.md§開發規範 ref:refs.md§issue-c 參考文件 |

## 角色候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| 審核者 | 7 | 13.0 | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 審核 pm_spec:pm-spec.md§3.4 逾時提醒 pm_spec:pm-spec.md§4 非功能需求 |
| 填寫者 | 4 | 5.0 | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 送審 pm_spec:pm-spec.md§3.3 退回後重送 |
| 系統 | 4 | 3.8 | 降 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.4 逾時提醒 ref:overview.md§架構概觀 ref:refs.md§issue-c 參考文件 |
| 部門主管 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |

## 狀態值候選(屬性,不建實體)

| 詞 | 詞頻 | 出現 |
|---|---|---|
| 待審核 | 7 | mock:approval.html pm_spec:pm-spec.md§3.1 送審 pm_spec:pm-spec.md§3.2 審核 pm_spec:pm-spec.md§3.4 逾時提醒 |
| 可刪除 | 1 | pm_spec:pm-spec.md§4 非功能需求 |
| 未審核 | 1 | pm_spec:pm-spec.md§2 使用者與情境 |
| 已核准 | 1 | pm_spec:pm-spec.md§3.3 退回後重送 |

## 英文符號

| 符號 | 詞頻 | codebase 命中 | 出現 |
|---|---|---|---|
| Forms | 6 | 5 (src/api/Forms.Infrastructure/SqlFormRepository.cs:1) | ref:overview.md ref:refs.md |
| Domain | 4 | 5 (src/api/Forms.Infrastructure/SqlFormRepository.cs:1) | ref:coding.md ref:overview.md ref:refs.md |
| Handler | 3 | 0 | ref:coding.md ref:overview.md ref:refs.md |
| SMTP | 3 | 1 (src/api/Forms.Infrastructure/EmailNotifier.cs:8) | ref:coding.md ref:overview.md ref:refs.md |
| issue | 1 | 5 (src/database/002_submissions.sql:1) | pm_spec:pm-spec.md |
| mock | 1 | 0 | mock:approval.html |
| Aggregate | 2 | 1 (src/api/Forms.Domain/Form.cs:5) | ref:coding.md ref:overview.md |
| Bounded | 2 | 0 | ref:overview.md ref:refs.md |
| Context | 2 | 0 | ref:overview.md ref:refs.md |
| Controller | 2 | 0 | ref:coding.md ref:overview.md |
| INotifier | 2 | 2 (src/api/Forms.Infrastructure/EmailNotifier.cs:4) | ref:refs.md |
| Infrastructure | 2 | 4 (src/api/Forms.Infrastructure/SqlFormRepository.cs:2) | ref:coding.md ref:overview.md |
| MediatR | 2 | 3 (src/api/Forms.Api/Controllers/FormsController.cs:2) | ref:coding.md ref:overview.md |
| Repository | 2 | 0 | ref:coding.md ref:overview.md |
| Application | 1 | 3 (src/api/Forms.Api/Controllers/FormsController.cs:1) | ref:overview.md |
| Architecture | 1 | 0 | ref:overview.md |
| Clean | 1 | 0 | ref:overview.md |
| Command | 1 | 0 | ref:coding.md |
| Core | 1 | 0 | ref:overview.md |
| FormSubmission | 1 | 5 (src/database/002_submissions.sql:2) | ref:refs.md |
| Notifier | 1 | 0 | ref:overview.md |
| Query | 1 | 0 | ref:coding.md |
| React | 1 | 0 | ref:overview.md |
| SQL | 1 | 0 | ref:overview.md |
| Server | 1 | 0 | ref:overview.md |
| enum | 1 | 1 (src/api/Forms.Domain/Form.cs:3) | ref:coding.md |
| forms | 1 | 5 (src/api/Forms.Infrastructure/SqlFormRepository.cs:1) | ref:refs.md |
| submissions | 1 | 5 (src/api/Forms.Api/Controllers/FormsController.cs:15) | ref:refs.md |
