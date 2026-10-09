# SA3 角色與動作

## 角色與動作
| 角色 | 動作 | 流程 | 對應 REQ |
|---|---|---|---|
| employee | BookRoom(POST /rooms/{id}/bookings) | book | REQ-001 |
| employee | CheckInBooking(POST /bookings/{id}/check-in) | check in | REQ-002 |
| system | ReleaseNoShow(job) | release | REQ-002 |
| admin | ListDailyBookings(GET /bookings/daily) | view | REQ-003 |
