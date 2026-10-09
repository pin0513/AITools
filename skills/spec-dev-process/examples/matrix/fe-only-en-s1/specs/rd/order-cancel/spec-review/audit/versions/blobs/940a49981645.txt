# Order cancellation and refund — API spec

## API List
| ID | Method | Path | Request | Response | REQ | Bound NFR | CMP |
|---|---|---|---|---|---|---|---|
| API-001 | POST | /orders/{id}/cancel | json | 200 | REQ-001 |  | CMP-005 |
| API-002 | POST | /orders/{id}/refund | json | 200 | REQ-002 | NFR-001 | CMP-005 |
| API-003 | GET | /orders/cancellations | json | 200 | REQ-003 |  | CMP-005 |

## External Dependencies and Failure Modes
| External System | Caller CMP | Timeout | Retry | Fallback | Compensation |
|---|---|---|---|---|---|
| BackendAPI | CMP-005 | 5s | 2 | show error | — |
