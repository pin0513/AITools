# 表單審核流程 — UI spec

> UI 的顆粒度是**畫面元素**(按鈕、欄位、連結),對到 API 的顆粒度(endpoint,見 `../40-api-contracts.md`)。
> 元素寫 mock 的 `#id` 或 `name`,工具會逐一對 mock 核對。按鈕可用性見 `20-domain-model.md` 的 STM-UI-001。

## 畫面清單
| 畫面 | 路由 | 元件 | Mock | 對應 REQ |
|---|---|---|---|---|
| 審核頁 | /submissions/{id} | | specs/in-progress/issue-c/mock/approval.html | REQ-001, REQ-002, REQ-003 |
| 填寫頁 | /forms/{id}/fill | | | REQ-001 |
| 審核清單 | /reviews | | | REQ-002 |

## 畫面元素
| 畫面 | 元素 | 類型 | 動作 | 呼叫 API | 啟用條件 | 對應 AC |
|---|---|---|---|---|---|---|
| 審核頁 | #approve | button | 核准 | API-002 | 狀態 = Pending 且操作者是審核者 | AC-002-1 |
| 審核頁 | #reject | button | 退回 | API-003 | 狀態 = Pending 且操作者是審核者 | AC-002-3 |
| 審核頁 | #reason | textarea | 輸入退回理由 | | 退回時必填,至少 10 字 | AC-002-2 |
| 審核頁 | #edit | button | 修改 | | 狀態 = Rejected(Pending / Approved 時停用) | AC-001-2, AC-003-2 |
| 審核頁 | #resubmit | button | 重新送出 | API-004 | 狀態 = Rejected | AC-003-1 |
| 審核頁 | dept | input | 無 | | 永遠唯讀(顯示填寫內容) | |
| 填寫頁 | submit | button | 送出 | API-001 | 必填欄位已填 | AC-001-1 |
| 審核清單 | 待審清單 | list | 載入待審清單 | API-005 | 操作者是審核者 | |

## 欄位驗證
| 畫面 | 欄位 | 規則 | 錯誤訊息 | 對應 AC |
|---|---|---|---|---|
| 審核頁 | #reason | 至少 10 字 | 退回理由至少 10 字(REASON_TOO_SHORT) | AC-002-2 |
