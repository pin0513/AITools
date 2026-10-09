# 表單審核流程 — 概觀

## 背景與目標
PM§1:送出的表單需經審核才算完成;目標上線三個月內需審核表單平均處理時間 < 2 個工作天。

## 範圍
| In | Out |
|---|---|
| 送審狀態、核准/退回+理由、退回後重送、逾時每日提醒、審核紀錄查看 | 審核者指派 UI(缺口 #1,暫以設定檔)、多級審核、代理審核 |

## 名詞表
| 名詞 | 定義 | 來源 |
|---|---|---|
| 填寫紀錄 | FormSubmission,一次送出的答案集合 | PM§3.1 |
| 審核紀錄 | ReviewRecord,一次核准或退回的不可變紀錄 | PM§3.2 |
| 工作天 | 週一至週五(缺口 #3) | PM§3.4 |

## 來源對照
| PM 來源 | RD 產物 |
|---|---|
| PM§1 背景與目標 | 00-overview.md |
| PM§3.1 送審 | REQ-001, UC-001, STM-DOM-001 |
| PM§3.2 審核 | REQ-002, UC-002, SEQ-001 |
| PM§3.3 退回後重送 | REQ-003, UC-003 |
| PM§3.4 逾時提醒 | REQ-004, UC-004, SEQ-002 |
| PM§4 非功能需求 | NFR-001, NFR-002, NFR-003 |
| mock/approval.html | STM-UI-001(pending/approved/rejected 按鈕可用性), 欄位: reason |
| SA sa/02 實體 | 20-domain-model 領域模型表 |
| SA sa/07 STM-SA-001 | STM-DOM-001 |
| survey-mapping.md | 30 Component 表(existing/modify/new) |

## 來源
- PM spec:`specs/in-progress/issue-c/pm-spec.md`(2026-10-09)
- Mock:`specs/in-progress/issue-c/mock/approval.html`
- 參考:`specs/in-progress/issue-c/refs.md`、`docs/architectures/overview.md`、`docs/guidelines/coding.md`
