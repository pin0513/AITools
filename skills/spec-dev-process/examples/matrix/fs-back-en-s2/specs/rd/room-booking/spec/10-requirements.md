# Meeting room booking — requirements

## Requirements
| ID | Requirement | Type | Source Anchor | AC |
|---|---|---|---|---|
| REQ-001 | An employee can book a meeting room without overlapping time slot | functional, domain_rich | PM§3.1 | AC-001-1, AC-001-2 |
| REQ-002 | check in within 15 minutes or the system will release the meeting room | functional, state_heavy, integration | PM§3.2 | AC-002-1, AC-002-2 |
| REQ-003 | An admin can view daily booking records | functional | PM§3.3 | AC-003-1 |

## Acceptance Criteria
```gherkin
# AC-001-1
Given the time slot is free
When the employee books the meeting room
Then a booking is booked

# AC-001-2
Given the time slot overlaps another booking
When the employee books the meeting room
Then the response is 409 SLOT_TAKEN

# AC-002-1
Given a booking is booked
When the employee checks in within 15 minutes
Then the booking is checked-in

# AC-002-2
Given no check in after 15 minutes
When the system job runs
Then the booking is released and the calendar service is updated

# AC-003-1
Given booking records exist today
When the admin opens the daily view
Then rows are grouped by meeting room

```

## Non-functional Requirements
| ID | Stimulus | Source | Environment | Artifact | Response | Measure | Bound CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | With 100 concurrent requests for the same time slot, exactly one booking succeeds. | user | normal load | API-001 | ok | 100 concurrent → 1 success | API-001 | AC-N01-1 |

## Gaps
| # | Question | Affects REQ | Assumption |
|---|---|---|---|
