# 會議室預約 (PM spec)

## 1 背景與目標
目前 employee 用 email book Room,每週都有重複 book。目標:自助 book,檢查衝突,並自動 release 未 check in 的 Room。

## 2 使用者與情境
employee:想 book Room。 admin:需要每日 view。 system: release 未 check in 的 Booking。

## 3 功能需求
### 3.1 employee 可 book Room, TimeSlot 不得重疊
employee 可以為某個 TimeSlot book Room。同一 Room 的兩張 Booking 不得重疊。新 Booking 狀態為 Booked,並同步到 CalendarService。

### 3.2 15 分鐘內 check in,否則 system release Room
employee 必須在開始後 15 分鐘內 check in。否則 system release Booking,狀態改為 Released,並更新 CalendarService。

### 3.3 admin 可 view 每日 Booking
admin 可以 view 每間 Room 當天的所有 Booking。

## 4 非功能需求
同一 TimeSlot 有 100 個並行 book 請求時,只有一張 Booking 成功。

## 5 驗收條件
- TimeSlot 空閒 → employee book Room → Booking 狀態為 Booked
- TimeSlot 與其他 Booking 重疊 → employee book Room → 回應 409 SLOT_TAKEN
- Booking 狀態為 Booked → employee 在 15 分鐘內 check in → Booking 狀態為 CheckedIn
- 15 分鐘內未 check in → system 排程執行 → Booking 狀態為 Released, CalendarService 已更新
- 今天有 Booking → admin 開啟每日檢視 → 依 Room 分組顯示
