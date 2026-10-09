# room-booking SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)

來源:pm_spec:pm-spec.md, mock:booking.html, ref:refs.md · CJK 候選 38 → 邊界熵後 22 → 去冗後 22

規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。

## 名詞候選

| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |
|---|---|---|---|---|---|---|
| booking | 13 | 22.0 | Booking | 0 | 升 | mock:booking.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 employee pm_spec:pm-spec.md§3.2 15 分鐘內 c |
| room | 10 | 14.0 | Room | 5 (src/api/Rooms.Application/ListRoomsQueryHandler.cs:6) | 升 | mock:booking.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 employee |
| 狀態 | 6 | 10.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 employee pm_spec:pm-spec.md§3.2 15 分鐘內 c pm_spec:pm-spec.md§5 驗收條件 |
| timeslot | 4 | 8.0 | TimeSlot | 0 | 升 | pm_spec:pm-spec.md§3.1 employee pm_spec:pm-spec.md§4 非功能需求 pm_spec:pm-spec.md§5 驗收條件 |
| calendarservice | 3 | 4.0 | CalendarService | 0 | 升 | pm_spec:pm-spec.md§3.1 employee pm_spec:pm-spec.md§3.2 15 分鐘內 c pm_spec:pm-spec.md§5 驗收條件 |
| room booking | 3 | 4.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 employee pm_spec:pm-spec.md§3.3 admin 可  pm_spec:pm-spec.md§5 驗收條件 |
| 重疊 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 employee pm_spec:pm-spec.md§5 驗收條件 |

## 動作候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| book | 9 | 14.0 | 升 | mock:booking.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 employee |
| check in | 6 | 9.0 | 升 | mock:booking.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 15 分鐘內 c |
| release | 3 | 4.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 15 分鐘內 c |
| view | 3 | 4.0 | 降 | mock:booking.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 admin 可  |
| 更新 | 2 | 3.0 | 降 | pm_spec:pm-spec.md§3.2 15 分鐘內 c pm_spec:pm-spec.md§5 驗收條件 |
| 組顯示 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§5 驗收條件 |

## 角色候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| employee | 7 | 11.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 employee pm_spec:pm-spec.md§3.2 15 分鐘內 c |
| admin | 3 | 5.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 admin 可  pm_spec:pm-spec.md§5 驗收條件 |
| system | 3 | 5.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 15 分鐘內 c pm_spec:pm-spec.md§5 驗收條件 |

## 狀態值候選(屬性,不建實體)

| 詞 | 詞頻 | 出現 |
|---|---|---|
| booked | 4 | mock:booking.html pm_spec:pm-spec.md§3.1 employee pm_spec:pm-spec.md§5 驗收條件 |
| released | 2 | pm_spec:pm-spec.md§3.2 15 分鐘內 c pm_spec:pm-spec.md§5 驗收條件 |
| 已更新 | 1 | pm_spec:pm-spec.md§5 驗收條件 |

## 英文符號

| 符號 | 詞頻 | codebase 命中 | 出現 |
|---|---|---|---|
| Booking | 13 | 0 | mock:booking.html pm_spec:pm-spec.md |
| Room | 10 | 5 (src/api/Rooms.Application/ListRoomsQueryHandler.cs:6) | mock:booking.html pm_spec:pm-spec.md |
| book | 9 | 0 | mock:booking.html pm_spec:pm-spec.md |
| employee | 7 | 0 | pm_spec:pm-spec.md |
| check | 6 | 0 | mock:booking.html pm_spec:pm-spec.md |
| TimeSlot | 4 | 0 | pm_spec:pm-spec.md |
| Booked | 4 | 0 | mock:booking.html pm_spec:pm-spec.md |
| admin | 3 | 0 | pm_spec:pm-spec.md |
| system | 3 | 0 | pm_spec:pm-spec.md |
| CalendarService | 3 | 0 | pm_spec:pm-spec.md |
| release | 3 | 0 | pm_spec:pm-spec.md |
| view | 3 | 0 | mock:booking.html pm_spec:pm-spec.md |
| Released | 2 | 0 | pm_spec:pm-spec.md |
| CheckedIn | 1 | 0 | pm_spec:pm-spec.md |
| SLOT_TAKEN | 1 | 0 | pm_spec:pm-spec.md |
| email | 1 | 0 | pm_spec:pm-spec.md |
| mock | 1 | 0 | mock:booking.html |
| status | 1 | 2 (src/api/Rooms.Domain/Room.cs:3) | mock:booking.html |
| shape | 1 | 0 | ref:refs.md |
