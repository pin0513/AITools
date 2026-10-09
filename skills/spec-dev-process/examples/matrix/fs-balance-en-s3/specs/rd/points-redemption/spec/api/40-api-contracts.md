# Loyalty points redemption — API spec

## API List
| ID | Method | Path | Request | Response | REQ | Bound NFR | CMP |
|---|---|---|---|---|---|---|---|
| API-001 | POST | /members/{id}/redemptions | json | 200 | REQ-001 | NFR-001 | CMP-006 |
| API-002 | GET | /members/{id}/transactions | json | 200 | REQ-003 |  | CMP-006 |

## External Dependencies and Failure Modes
| External System | Caller CMP | Timeout | Retry | Fallback | Compensation |
|---|---|---|---|---|---|
| RewardVendor | CMP-012 | 5s | 3 | 503 | retry next run |
