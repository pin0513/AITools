---
name: Role Decomposition
description: Provide methodology and decision framework for decomposing team responsibilities into agent roles with appropriate granularity
---

# Role Decomposition

## Description

Provide methodology and decision framework for decomposing team responsibilities into agent roles with appropriate granularity.

## Users

- `role-designer`: For responsibility decomposition during role design phase
- `team-architect`: For structural rationality assessment during review phase

## Core Framework: MECE Responsibility Decomposition

Each agent's responsibilities must follow the MECE principle:
- **Mutually Exclusive**: Any specific work should belong to only one agent
- **Collectively Exhaustive**: All work combined should have no omissions

## Granularity Calibration Method

### Signals of Too Coarse (Need to Split)
- Agent's responsibility description exceeds 5 core work items
- Agent needs to switch between 2+ different professional domains
- Agent's output types exceed 3 kinds
- Cannot summarize what this agent does in one sentence

### Signals of Too Fine (Need to Merge)
- Two agents have identical input sources
- One agent's output has only one downstream consumer, and both are in the same professional domain
- One agent's workload is insufficient to exist independently (only 1-2 simple tasks)
- After splitting, two agents need to communicate on every single task

### Signs of Appropriate Granularity
- Each agent can be clearly described with one sentence about their core responsibility
- Each agent has 3-5 core work items
- Agent interactions are primarily "deliverable handoffs" rather than "ongoing discussions"
- Removing any agent would leave certain work with no one responsible

## Grouping Strategy

Choose grouping criteria by priority:

1. **Workflow stages** (Most recommended)
   - Applicable scenario: Team work has clear sequential order
   - Example: discovery → planning → execution → review

2. **Professional domains**
   - Applicable scenario: Team spans multiple specialties, but processes within each are similar
   - Example: content → technical → quality

3. **Deliverable-oriented**
   - Applicable scenario: Team's deliverable types are significantly different
   - Example: code → documentation → visual-assets
