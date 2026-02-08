---
name: Team Topology Analysis
description: Provide framework for analyzing team structure rationality and evaluating collaboration topology efficiency between agents
---

# Team Topology Analysis

## Description

Provide framework for analyzing team structure rationality, used to evaluate whether collaboration topology between agents is efficient and whether bottlenecks or redundancies exist.

## Belongs To

This skill belongs exclusively to `agents/discovery/role-designer.md`

## Core Knowledge

### Topology Patterns

#### 1. Pipeline Topology
```
A → B → C → D
```
- Applicable scenario: Work has strict sequential order
- Advantages: Clear responsibilities, predictable process
- Risk: Any blocked node causes entire chain to stall

#### 2. Hub & Spoke Topology
```
    B
    ↑
A ← Coordinator → C
    ↓
    D
```
- Applicable scenario: Multiple parallel work streams coordinated by one coordinator
- Advantages: Flexible assignment, easy to add/remove nodes
- Risk: Coordinator becomes single point of bottleneck

#### 3. Hybrid Topology
```
Coordinator → [GroupA: A1 → A2] → Review → [GroupB: B1, B2] → Final
```
- Applicable scenario: Complex teams with some sequential work, some parallel
- Usually the recommended final pattern

### Topology Health Check

1. **Bottleneck detection**: Is any agent the upstream of 3+ other agents simultaneously?
2. **Island detection**: Is any agent without any interaction with other team members?
3. **Cycle detection**: Does A→B→C→A circular dependency exist? (review cycles excluded)
4. **Coordinator load**: Does coordinator directly manage more than 7 agents? If so, recommend splitting into separate teams.

## Quality Checkpoints

- [ ] Every agent has at least one upstream or downstream connection
- [ ] Coordinator is at the logical center of topology
- [ ] No meaningless circular dependencies
- [ ] Parallel work agents are correctly grouped
