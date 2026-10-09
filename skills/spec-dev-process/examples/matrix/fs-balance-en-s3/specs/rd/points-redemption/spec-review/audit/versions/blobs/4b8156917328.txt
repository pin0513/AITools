# Loyalty points redemption (PM spec)

## 1 Background and Goals
A member collects points but cannot redeem them online. Goal: online redeem of a reward with a reliable ledger.

## 2 Users
member: wants to redeem a reward. system: will expire old points.

## 3 Functional Requirements
### 3.1 A member can redeem a reward when the points account has enough points
A member can redeem a reward when the points account balance covers the cost. The redemption starts pending, the points are deducted as a points transaction, and the reward vendor fulfills it.

### 3.2 Points expire after 12 months
Points that are not used for 12 months expire. A monthly system job writes an expiry points transaction and reduces the points account balance.

### 3.3 A member can view each points transaction
A member can view every points transaction with date, type and points.

## 4 Non-functional Requirements
The points account balance must never become negative, even with concurrent redemption.

## 5 Acceptance
- the balance covers the reward → the member redeems it → a redemption is created and the reward vendor is called
- the balance is not enough → the member redeems it → the response is 422 INSUFFICIENT_POINTS and nothing is deducted
- points were earned 13 months ago → the monthly job runs → an expiry points transaction is written and the balance drops
- the member has a points transaction → the member opens the history → each points transaction shows date, type and points
