# Meeting room booking — test design

## Test Components
| ID | Name | kind | CMP Refs | AC Refs |
|---|---|---|---|---|
| TST-001 | RoomsControllerTests | integration | CMP-001 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-002 | BookRoomCommandHandlerTests | unit | CMP-002 | AC-001-1, AC-001-2 |
| TST-003 | CheckInBookingCommandHandlerTests | unit | CMP-003 | AC-002-1, AC-002-2 |
| TST-004 | ReleaseNoShowJobTests | unit | CMP-004 | AC-002-1, AC-002-2 |
| TST-005 | ListDailyBookingsQueryHandlerTests | unit | CMP-005 | AC-003-1 |
| TST-006 | BookingTests | unit | CMP-006 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-007 | SqlRoomRepositoryTests | integration | CMP-007 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-008 | CalendarServiceClientTests | contract | CMP-008 | AC-001-1, AC-001-2, AC-002-1, AC-002-2 |
| TST-009 | NFR-001FitnessTest | e2e | CMP-001 | AC-N01-1 |

## Fitness Function
| NFR | Measurement | Threshold | Where |
|---|---|---|---|
| NFR-001 | k6 / Playwright | 100 concurrent → 1 success | CI nightly |
