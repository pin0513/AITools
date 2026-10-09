# room-booking SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)

來源:pm_spec:pm-spec.md, mock:booking.html, ref:refs.md · CJK 候選 0 → 邊界熵後 0 → 去冗後 0

規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。

## 名詞候選

| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |
|---|---|---|---|---|---|---|
| booking | 14 | 14.0 | Booking | 0 | 升 | mock:booking.html pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 An emplo |
| meeting room | 9 | 9.0 | Room | 5 (src/api/Rooms.Application/ListRoomsQueryHandler.cs:6) | 升 | mock:booking.html pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 An emplo |
| slot | 5 | 5.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 An emplo pm_spec:pm-spec.md§4 Non-functi pm_spec:pm-spec.md§5 Acceptance |
| booking records | 4 | 4.0 |  | — | 升 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 An emplo pm_spec:pm-spec.md§3.3 An admin pm_spec:pm-spec.md§5 Acceptance |
| time slot | 4 | 4.0 | TimeSlot | 0 | 升 | pm_spec:pm-spec.md§3.1 An emplo pm_spec:pm-spec.md§4 Non-functi pm_spec:pm-spec.md§5 Acceptance |
| calendar service | 3 | 3.0 | CalendarService | 0 | 升 | pm_spec:pm-spec.md§3.1 An emplo pm_spec:pm-spec.md§3.2 check in pm_spec:pm-spec.md§5 Acceptance |
| daily | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§5 Acceptance |
| today | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§5 Acceptance |

## 動作候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| book | 7 | 7.0 | 升 | mock:booking.html pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 An emplo |
| check in | 4 | 4.0 | 升 | mock:booking.html pm_spec:pm-spec.md§3.2 check in pm_spec:pm-spec.md§5 Acceptance |
| view | 4 | 4.0 | 升 | mock:booking.html pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.3 An admin pm_spec:pm-spec.md§5 Acceptance |
| release | 3 | 3.0 | 升 | pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.2 check in |
| update | 2 | 2.0 | 降 | pm_spec:pm-spec.md§3.2 check in pm_spec:pm-spec.md§5 Acceptance |
| check | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 Background |
| sync | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.1 An emplo |

## 角色候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| employee | 7 | 7.0 | 升 | pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 An emplo pm_spec:pm-spec.md§3.2 check in |
| admin | 3 | 3.0 | 降 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.3 An admin pm_spec:pm-spec.md§5 Acceptance |
| system | 3 | 3.0 | 降 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.2 check in pm_spec:pm-spec.md§5 Acceptance |

## 狀態值候選(屬性,不建實體)

| 詞 | 詞頻 | 出現 |
|---|---|---|
| booked | 4 | mock:booking.html pm_spec:pm-spec.md§3.1 An emplo pm_spec:pm-spec.md§5 Acceptance |
| released | 2 | pm_spec:pm-spec.md§3.2 check in pm_spec:pm-spec.md§5 Acceptance |
| checked-in | 1 | pm_spec:pm-spec.md§5 Acceptance |

## 英文符號

| 符號 | 詞頻 | codebase 命中 | 出現 |
|---|---|---|---|
| booking | 14 | 0 | mock:booking.html pm_spec:pm-spec.md |
| meeting | 9 | 0 | mock:booking.html pm_spec:pm-spec.md |
| room | 9 | 5 (src/api/Rooms.Application/ListRoomsQueryHandler.cs:6) | mock:booking.html pm_spec:pm-spec.md |
| employee | 7 | 0 | pm_spec:pm-spec.md |
| book | 4 | 0 | mock:booking.html pm_spec:pm-spec.md |
| records | 4 | 0 | pm_spec:pm-spec.md |
| service | 4 | 0 | pm_spec:pm-spec.md |
| slot | 4 | 0 | pm_spec:pm-spec.md |
| time | 4 | 0 | pm_spec:pm-spec.md |
| view | 4 | 0 | mock:booking.html pm_spec:pm-spec.md |
| admin | 3 | 0 | pm_spec:pm-spec.md |
| booked | 3 | 0 | pm_spec:pm-spec.md |
| books | 3 | 0 | pm_spec:pm-spec.md |
| calendar | 3 | 0 | pm_spec:pm-spec.md |
| check | 3 | 0 | mock:booking.html pm_spec:pm-spec.md |
| minutes | 3 | 0 | pm_spec:pm-spec.md |
| release | 3 | 0 | pm_spec:pm-spec.md |
| system | 3 | 0 | pm_spec:pm-spec.md |
| after | 2 | 0 | pm_spec:pm-spec.md |
| checks | 2 | 0 | pm_spec:pm-spec.md |
| daily | 2 | 0 | pm_spec:pm-spec.md |
| must | 2 | 0 | pm_spec:pm-spec.md |
| released | 2 | 0 | pm_spec:pm-spec.md |
| same | 2 | 0 | pm_spec:pm-spec.md |
| today | 2 | 0 | pm_spec:pm-spec.md |
| will | 2 | 0 | pm_spec:pm-spec.md |
| within | 2 | 0 | pm_spec:pm-spec.md |
| Booked | 1 | 0 | mock:booking.html |
| Goal | 1 | 0 | pm_spec:pm-spec.md |
| Otherwise | 1 | 0 | pm_spec:pm-spec.md |
| SLOT_TAKEN | 1 | 0 | pm_spec:pm-spec.md |
| Two | 1 | 0 | pm_spec:pm-spec.md |
| another | 1 | 0 | pm_spec:pm-spec.md |
| automatic | 1 | 0 | pm_spec:pm-spec.md |
| checked | 1 | 0 | pm_spec:pm-spec.md |
| concurrent | 1 | 0 | pm_spec:pm-spec.md |
| conflict | 1 | 0 | pm_spec:pm-spec.md |
| double | 1 | 0 | pm_spec:pm-spec.md |
| email | 1 | 0 | pm_spec:pm-spec.md |
| every | 1 | 0 | pm_spec:pm-spec.md |
