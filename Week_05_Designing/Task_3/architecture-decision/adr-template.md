# ADR-<NNN>: <Use X for Y>

- Status: accepted
- Date: <YYYY-MM-DD>
- Deciders: <user>, with Claude Code

## Context and problem statement

<What the system is, roles, number of stories by area. Stated constraints and whether any story justifies them. Missing numbers and unnamed external parties. One sentence on what the architecture must achieve.>

## Decision drivers

- <All stories covered.>
- <Each stated constraint, and whether it may be challenged.>
- <The integrity property that matters most, e.g. payment correctness.>
- <Team size and operating cost.>
- <Path to change later.>

## Considered options

1. <Option 1>
2. <Option 2, with the user's granularity choice>
3. <Option 3, with the user's scope and broker choice>

| Decision driver | 1. <short> | 2. <short> | 3. <short> |
|---|---|---|---|
| <driver> | <one short phrase> | ... | ... |

## Decision outcome

Chosen option: <option>.

<Why, in a short paragraph. How the challenged constraints are still met.>

```mermaid
flowchart LR
    <clients, components inside the deployable(s), DB, external parties, webhook direction>
```

### Design decisions inside <option>

- <One bullet per decision from the discussion and the ADR rounds, one or two sentences each.>

### Consequences

Good:
- <...>

Bad:
- <...>
- <For each challenged constraint: a reviewer may read it literally.>

### Assumptions

- <Every screen or feature the design needs that no story covers.>

### Not decided here

<Topics never discussed for the chosen option. Each needs its own ADR.>

### When to revisit

- <Concrete trigger>: <which option it points to>.

## Pros and cons of the options

### 1. <Option 1>

- Good: <...>
- Bad: <...>

### 2. <Option 2>

- Good: <...>
- Bad: <include the failure scenarios found in the discussion>

### 3. <Option 3>

- Good: <...>
- Bad: <...>
