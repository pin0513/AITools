---
name: Structured Interview
description: Provide in-depth interview methodology for extracting clear actionable requirements from vague descriptions
---

# Structured Interview

## Description

Provide in-depth interview methodology for extracting clear, actionable requirements from vague user descriptions.

## Users

- `requirements-analyst`: For user interviews during the requirements exploration phase
- `team-architect`: For initial requirements assessment and direction confirmation

## Core Methods

### Funnel Questioning Method

From broad to narrow, progressively converge:

1. **Open exploration**: "What goal do you want to achieve?" — Let users describe freely
2. **Boundary confirmation**: "What does this team NOT need to handle?" — Define scope by exclusion
3. **Concretization follow-up**: "What specifically do you mean by X? Can you give an example?" — Eliminate ambiguity
4. **Verification playback**: "My understanding is Y, is that correct?" — Confirm consensus

### Follow-up Triggers

Must follow up when encountering these signals:
- User uses vague words: "roughly", "probably", "things like that", "etc."
- User skips process details: States results directly without explaining process
- User's description has logical gaps: Missing B between A and C
- User's requirements have implicit conflicts: Demanding both "fast" and "high quality"

### Reverse Validation Method

After user provides requirements, validate with opposite questions:
- "If role X didn't exist, which work would have no one doing it?"
- "If Y and Z were merged into one role, what problems would arise?"
- "What's the most likely reason this team would fail?"

## Interview Rhythm Control

- Focus each response on one direction only, don't ask multiple unrelated questions simultaneously
- Provide an interim summary every 3-4 rounds to confirm direction is correct
- Control total interview rounds to 8-15, adjusted by complexity
- When user starts repeating previously stated content, that dimension is fully explored — move to next dimension
