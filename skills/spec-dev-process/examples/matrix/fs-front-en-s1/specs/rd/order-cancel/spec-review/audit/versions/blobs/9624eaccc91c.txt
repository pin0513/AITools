# Order cancellation and refund — requirements

## Requirements
| ID | Requirement | Type | Source Anchor | AC |
|---|---|---|---|---|
| REQ-001 | A customer can cancel an order before it is shipped | functional, state_heavy | PM§3.1 | AC-001-1, AC-001-2 |
| REQ-002 | The system issues a refund through the payment gateway after cancellation | functional, integration | PM§3.2 | AC-002-1, AC-002-2 |
| REQ-003 | A support agent can view the cancellation history | functional | PM§3.3 | AC-003-1 |

## Acceptance Criteria
```gherkin
# AC-001-1
Given an order is placed
When the customer cancels it
Then the order status is cancelled

# AC-001-2
Given an order is shipped
When the customer cancels it
Then the response is 409 ORDER_SHIPPED and the status is unchanged

# AC-002-1
Given an order is cancelled and paid
When the system issues the refund
Then the payment gateway is called and the order is refunded

# AC-002-2
Given the payment gateway times out
When the system issues the refund
Then it retries 3 times and the order stays cancelled

# AC-003-1
Given order records were cancelled
When the support agent opens the history
Then each row shows the order, time and reason

```

## Non-functional Requirements
| ID | Stimulus | Source | Environment | Artifact | Response | Measure | Bound CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | A refund must finish within 5 minutes after cancellation for 95% of order records. | user | normal load | API-002 | ok | P95 < 5 min | API-002 | AC-N01-1 |

## Gaps
| # | Question | Affects REQ | Assumption |
|---|---|---|---|
