# Loyalty points redemption — requirements

## Requirements
| ID | Requirement | Type | Source Anchor | AC |
|---|---|---|---|---|
| REQ-001 | A member can redeem a reward when the points account has enough points | functional, domain_rich, integration | PM§3.1 | AC-001-1, AC-001-2 |
| REQ-002 | Points expire after 12 months | functional, data | PM§3.2 | AC-002-1 |
| REQ-003 | A member can view each points transaction | functional | PM§3.3 | AC-003-1 |

## Acceptance Criteria
```gherkin
# AC-001-1
Given the balance covers the reward
When the member redeems it
Then a redemption is created and the reward vendor is called

# AC-001-2
Given the balance is not enough
When the member redeems it
Then the response is 422 INSUFFICIENT_POINTS and nothing is deducted

# AC-002-1
Given points were earned 13 months ago
When the monthly job runs
Then an expiry points transaction is written and the balance drops

# AC-003-1
Given the member has a points transaction
When the member opens the history
Then each points transaction shows date, type and points

```

## Non-functional Requirements
| ID | Stimulus | Source | Environment | Artifact | Response | Measure | Bound CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | The points account balance must never become negative, even with concurrent redemption. | user | normal load | API-001 | ok | balance never negative | API-001 | AC-N01-1 |

## Gaps
| # | Question | Affects REQ | Assumption |
|---|---|---|---|
