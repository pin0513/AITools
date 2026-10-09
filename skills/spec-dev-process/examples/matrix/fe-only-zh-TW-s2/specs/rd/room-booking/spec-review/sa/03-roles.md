# SA3 角色與動作

## 角色與動作
| 角色 | 動作 | 流程 | 對應 REQ |
|---|---|---|---|
| 員工 | BookRoom(POST /rooms/{id}/bookings) | 預約 | REQ-001 |
| 員工 | CheckInBooking(POST /bookings/{id}/check-in) | 報到 | REQ-002 |
| 系統 | ReleaseNoShow(job) | 釋放 | REQ-002 |
| 管理員 | ListDailyBookings(GET /bookings/daily) | 查看 | REQ-003 |
