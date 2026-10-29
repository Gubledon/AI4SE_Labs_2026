---
name: architecture-decision
description: Lead a design discussion from a requirements document. Propose three different architectures, discuss each with the user (their decisions, trade-offs, painful low-level parts, failure scenarios), walk the core flow through all of them, then help the user choose one and write and iterate an Architecture Decision Record (ADR). Keeps short conversation notes the whole time. Use when asked to propose or compare architectures for a system, or to write an ADR from such a discussion.
---

# Architecture decision: from requirements to ADR

Two phases. Phase 1 is the architecture discussion. Phase 2 is the ADR. The user leads: they make the design decisions, you prepare the options and explain the consequences.

## Rules that apply the whole time

**Notes start before anything else.** Create a notes file in the task folder before the first proposal, without being asked. If a notes file from an earlier run already exists there, ask for a new file name. Never overwrite an earlier record. Update the notes after every exchange, not at the end.

**Notes format:**

```markdown
# <Task>: <topic> notes (<project>)

Short notes kept by the assistant during the session. Not a transcript. "Me" is the user, "Assistant" is Claude Code.

## <Topic section, e.g. Architecture 1: modular monolith>

Assistant: <question>? Options: <a>, <b>, <c>.

Me: <their pick, in their words if they gave any>.

Assistant: <consequence in one to three sentences>.
```

- Alternate "Me:" and "Assistant:" turns, condensed, not verbatim.
- One exchange per question: the question with its options, the user's pick, then your consequence. Never pack several questions into one turn.
- Put each turn under the section it belongs to. An instruction that framed Architecture 1 goes under Architecture 1, not under Setup.
- Leave out messages the user marks as not for the notes, and messages that only adjust the notes themselves.
- Never write reasoning into a "Me:" turn that the user didn't give. If they want their reasons recorded, ask them for the reasons.
- Keep it short. A turn is one short paragraph at most.

**Questions go through AskUserQuestion.** Two to four options each, with a one-line concrete consequence per option. For design decisions, put your recommendation first and mark it "(Recommended)". For understanding checks (quizzes), never mark an answer.

**One question round per step.** Up to four questions per architecture, one walkthrough round, one round per ADR draft if needed. Don't add extra deep-dive rounds unless the user asks. Stay close to what the assignment asks.

**Never decide alone what the user should decide.** Present an outline, then ask. Don't lay out a full architecture with every choice already made.

**Prose follows the repo's writing rules** (see the project CLAUDE.md, if there is one): plain verbs, no stock AI words, no em dashes, no bold lead-ins in the notes or the ADR.

## Phase 1: architecture discussion

### Step 1. Read and summarise

Read the task file and the assigned requirements file in full. Then give the user a summary of six lines or fewer:

- What the system is, its roles, and the number of user stories, grouped by area.
- Gaps: missing numbers (users, traffic, data size), unnamed external parties (payment provider, carrier, email), missing stories the domain usually needs (stock, refunds, admin screens).
- Stated constraints that no story justifies, for example "distributed system" or "must scale". Quote them.

Propose three candidate architectures that span a real range, usually:
1. The simplest design that covers every story (often a modular monolith).
2. The literal reading of the stated constraints (often a few services behind a gateway).
3. The most decoupled option that fits the domain (often event-driven, with CQRS where reads dominate).

Then ask exactly one question: how to treat the unjustified constraints. The default is "challenge it, but don't dismiss it". Present option 1 as the baseline that meets all stories, and say which parts of it already satisfy the constraint (for "distributed": browser to backend, external payment provider and webhooks, email service, DB host).

### Step 2. One architecture at a time

For each architecture:

1. **Outline**, short: the components and which story numbers each covers, what is new or newly distributed compared with the previous option, gains, costs, and the painful low-level parts. Use `pitfalls.md` for the low-level parts that fit this domain.
2. **Decisions**: one AskUserQuestion round with the three or four open choices that change the design most. Typical ones are how payment status is set, where status data comes from, whether to add an unstated but expected feature (stock), service granularity, communication style, token and logout handling, event scope, storage (state + outbox or event sourcing), broker, and read lag handling.
3. **Consequences**: for each answer, explain concretely what it means in code and data (tables, constraints, jobs, failure modes). Record anything the stories don't cover as an ADR assumption.
4. **Carry decisions forward**: from the second architecture on, say how the user's earlier choices change here (for example, "webhook only" needs an outbox once payment and order live in different services).
5. **Understanding check**: one failure scenario as a quiz with three plausible outcomes and no marked answer. Examples: the webhook arrives while the server is down; one service is down, so which stories still work; two quick updates are handled by competing consumers. Explain the real behaviour, and say when the user's answer would be true (usually a specific bug).

Close each architecture with one sentence on what it amounts to for these requirements, for example "Arch 2 is the monolith with Catalogue pulled out".

### Step 3. Core flow walkthrough

Pick the flow where money or data integrity is at stake (usually checkout and payment). Walk it step by step through all three architectures in one message, as numbered steps, and mark one decision point per architecture where it can break. Then ask one AskUserQuestion round, one question per architecture. Good decision points:

- Is the external call inside or outside the DB transaction?
- How does an unauthenticated webhook pass an authenticating gateway?
- What does the UI show while a read model lags?

Explain each answer the same way as in Step 2.

## Phase 2: ADR

### Step 4. Choose and draft

Ask two questions in one round: which option the ADR chooses (recommend the one that meets all stories at the lowest cost, unless the discussion showed otherwise), and which template (MADR recommended, Nygard as the short alternative). Start a new notes file for this phase.

Write draft 1 from `adr-template.md`. Include from the start:

- Decision drivers taken from the stories and the stated constraints.
- A comparison table: decision drivers × options.
- A Mermaid diagram of the chosen architecture (components, DB, external parties, webhook direction).
- Every design decision the user made in Phase 1 for the chosen option.
- A "Bad" consequence for every challenged constraint (a reviewer may read it literally).
- Assumptions: every screen or feature the design needs that no story covers.
- Not decided here: topics that were never discussed for the chosen option.
- When to revisit: concrete triggers that point to the other options.

Tell the user what to inspect: is it informative enough, is anything missing or extra, is the structure right, do they want more tables or diagrams.

### Step 5. Iterate

Apply each change the user asks for, briefly. Before saving, check every new rule against the existing decisions and fix conflicts. The usual conflicts are these:

- A new rule breaks the double-click guard.
- A new rule puts a slow external call inside a held lock.
- A new rule cancels something a late webhook can still pay.

Name each adjustment you made and why in one sentence, so the user can reject it. If you find an open point, raise it and leave it out of the ADR until the user decides. Log every round as "## Draft N" in the notes.

When the user says it's done, check the outputs the assignment asks for and say which files hold them.
