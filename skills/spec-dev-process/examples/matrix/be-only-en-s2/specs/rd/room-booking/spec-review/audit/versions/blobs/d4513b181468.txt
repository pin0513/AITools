# Meeting room booking — API spec

## API List
| ID | Method | Path | Request | Response | REQ | Bound NFR | CMP |
|---|---|---|---|---|---|---|---|
| API-001 | POST | /rooms/{id}/bookings | json | 200 | REQ-001 | NFR-001 | CMP-001 |
| API-002 | POST | /bookings/{id}/check-in | json | 200 | REQ-002 |  | CMP-001 |
| API-003 | GET | /bookings/daily | json | 200 | REQ-003 |  | CMP-001 |

## External Dependencies and Failure Modes
| External System | Caller CMP | Timeout | Retry | Fallback | Compensation |
|---|---|---|---|---|---|
| CalendarService | CMP-008 | 5s | 3 | 503 | retry next run |
