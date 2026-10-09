# room-booking SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)

來源:pm_spec:pm-spec.md, mock:booking.html, ref:refs.md · CJK 候選 213 → 邊界熵後 67 → 去冗後 64

規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。

## 名詞候選

| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |
|---|---|---|---|---|---|---|
| 預約單 | 13 | 22.0 | Booking | 0 | 升 | mock:booking.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 員工可預約會議室 pm_spec:pm-spec.md§3.2 15 分鐘內報到 |
| 會議室 | 10 | 14.0 | Room | 3 (src/web/src/types/Room.ts:4) | 升 | mock:booking.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 員工可預約會議室 |
| 員工 | 7 | 11.0 |  | — | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 員工可預約會議室 pm_spec:pm-spec.md§3.2 15 分鐘內報到 |
| 狀態 | 6 | 10.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 員工可預約會議室 pm_spec:pm-spec.md§3.2 15 分鐘內報到 pm_spec:pm-spec.md§5 驗收條件 |
| 預約單狀態 | 5 | 9.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 員工可預約會議室 pm_spec:pm-spec.md§5 驗收條件 |
| 預約會議室 | 5 | 8.0 |  | — | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 員工可預約會議室 pm_spec:pm-spec.md§5 驗收條件 |
| 時段 | 4 | 8.0 | TimeSlot | 0 | 升 | pm_spec:pm-spec.md§3.1 員工可預約會議室 pm_spec:pm-spec.md§4 非功能需求 pm_spec:pm-spec.md§5 驗收條件 |
| 行事曆服務 | 3 | 4.0 | CalendarService | 0 | 升 | pm_spec:pm-spec.md§3.1 員工可預約會議室 pm_spec:pm-spec.md§3.2 15 分鐘內報到 pm_spec:pm-spec.md§5 驗收條件 |
| 員工預約會 | 2 | 4.0 |  | — | 降 | pm_spec:pm-spec.md§5 驗收條件 |
| 工預約會議 | 2 | 4.0 |  | — | 降 | pm_spec:pm-spec.md§5 驗收條件 |
| 張預約單 | 2 | 4.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 員工可預約會議室 pm_spec:pm-spec.md§4 非功能需求 |
| 重疊 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 員工可預約會議室 pm_spec:pm-spec.md§5 驗收條件 |

## 動作候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| 預約 | 25 | 41.0 | 升 | mock:booking.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 員工可預約會議室 |
| 報到 | 7 | 11.0 | 升 | mock:booking.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 15 分鐘內報到 |
| 釋放 | 5 | 7.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 15 分鐘內報到 pm_spec:pm-spec.md§5 驗收條件 |
| 查看 | 3 | 4.0 | 升 | mock:booking.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 管理員可查看每日 |
| 更新 | 2 | 3.0 | 升 | pm_spec:pm-spec.md§3.2 15 分鐘內報到 pm_spec:pm-spec.md§5 驗收條件 |
| 鐘內報到 | 2 | 3.0 | 升 | pm_spec:pm-spec.md§3.2 15 分鐘內報到 pm_spec:pm-spec.md§5 驗收條件 |
| 室分組顯示 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§5 驗收條件 |
| 日查看 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 |
| 以查看 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.3 管理員可查看每日 |
| 統釋放預約 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.2 15 分鐘內報到 |
| 自助預約 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |
| 自動釋放 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |
| 重複預約 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |

## 角色候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| 管理員 | 3 | 5.0 | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 管理員可查看每日 pm_spec:pm-spec.md§5 驗收條件 |
| 系統 | 3 | 5.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 15 分鐘內報到 pm_spec:pm-spec.md§5 驗收條件 |

## 狀態值候選(屬性,不建實體)

| 詞 | 詞頻 | 出現 |
|---|---|---|
| 已預約 | 3 | pm_spec:pm-spec.md§3.1 員工可預約會議室 pm_spec:pm-spec.md§5 驗收條件 |
| 已釋放 | 2 | pm_spec:pm-spec.md§3.2 15 分鐘內報到 pm_spec:pm-spec.md§5 驗收條件 |
| 已報到 | 1 | pm_spec:pm-spec.md§5 驗收條件 |
| booked | 1 | mock:booking.html |

## 英文符號

| 符號 | 詞頻 | codebase 命中 | 出現 |
|---|---|---|---|
| SLOT_TAKEN | 1 | 0 | pm_spec:pm-spec.md |
| Booked | 1 | 0 | mock:booking.html |
| email | 1 | 0 | pm_spec:pm-spec.md |
| mock | 1 | 0 | mock:booking.html |
| status | 1 | 1 (src/web/src/types/Room.ts:6) | mock:booking.html |
| shape | 1 | 0 | ref:refs.md |
