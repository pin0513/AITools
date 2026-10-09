# Meeting room booking — test design

## Test Components
| ID | Name | kind | CMP Refs | AC Refs |
|---|---|---|---|---|
| TST-001 | RoomBookingPageTests | e2e | CMP-001 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-002 | roomsApiTests | contract | CMP-002 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-003 | RoomsControllerTests | integration | CMP-003 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-004 | BookRoomCommandHandlerTests | unit | CMP-004 | AC-001-1, AC-001-2 |
| TST-005 | CheckInBookingCommandHandlerTests | unit | CMP-005 | AC-002-1, AC-002-2 |
| TST-006 | ReleaseNoShowJobTests | unit | CMP-006 | AC-002-1, AC-002-2 |
| TST-007 | ListDailyBookingsQueryHandlerTests | unit | CMP-007 | AC-003-1 |
| TST-008 | BookingTests | unit | CMP-008 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-009 | SqlRoomRepositoryTests | integration | CMP-009 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-010 | CalendarServiceClientTests | contract | CMP-010 | AC-001-1, AC-001-2, AC-002-1, AC-002-2 |
| TST-011 | NFR-001FitnessTest | e2e | CMP-003 | AC-N01-1 |

## Fitness Function
| NFR | Measurement | Threshold | Where |
|---|---|---|---|
| NFR-001 | k6 / Playwright | 100 concurrent → 1 success | CI nightly |
