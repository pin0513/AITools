# issue-c SA3 角色、動作、流程

## 角色與動作
| 角色 | 動作 | 流程 | 對應 REQ |
|---|---|---|---|
| Submitter | Submit(POST /forms/{id}/submissions) | 送審:填答 → 送出 → Pending | REQ-001 |
| Submitter | Edit(限 Rejected) | 退回修改:看理由 → 改答案 | REQ-003 |
| Submitter | Resubmit(POST /submissions/{id}/resubmit) | 重送:Rejected → Pending | REQ-003 |
| Reviewer | ListPending(GET /reviews/pending) | 看待審清單 | REQ-002 |
| Reviewer | Approve(POST /submissions/{id}/approve) | 審核:Pending → Approved,寫 ReviewRecord | REQ-002 |
| Reviewer | Reject(POST /submissions/{id}/reject, reason ≥ 10) | 審核:Pending → Rejected,寫 ReviewRecord | REQ-002 |
| System | Remind(排程,每日) | 逾時:Pending > 3 工作天 → INotifier → ReviewReminder | REQ-004 |

流程摘要:送審 → (提醒)* → 審核 → 核准 | 退回 → 修改 → 重送 → 審核 …
