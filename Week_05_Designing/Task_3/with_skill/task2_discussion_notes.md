# Task 2: ADR discussion notes (CDC)

Start: 9:58
End: 10:22

Short notes kept by the assistant during the session. Not a transcript. "Me" is the user, "Assistant" is Claude Code.

## Setup

Me: Start Phase 2, the ADR for CDC.

## Choice and template

Assistant: Which option does the ADR choose? Options: 1. modular monolith (recommended), 2. three services plus gateway, 3. event-driven with CQRS catalogue.

Me: 1. Modular monolith.

Assistant: The ADR chooses option 1 and keeps 2 and 3 as considered options, with the user's Phase 1 choices.

Assistant: Which template? Options: MADR (recommended), Nygard.

Me: MADR.

Assistant: MADR, so the ADR has drivers, a comparison table, the outcome, consequences, and pros and cons per option.

## Draft 1

Assistant: Wrote `ADR-001-cdc-architecture.md`: context with gaps, drivers, three options with a comparison table, a Mermaid diagram of the monolith, the eight Phase 1 decisions, consequences (including that a reviewer may read "distributed" literally), assumptions, not decided here, and revisit triggers. Open point raised and left out: nothing cancels an abandoned pending order.

## Draft 2

Assistant: Open point: nothing cancels an abandoned pending order. Options: expire after 24 h and ask the provider first (recommended), never cancel, leave it in "Not decided here".

Me: Expire after 24 h, ask provider first.

Assistant: Added a 24 h expiry job and a rule for late payments on cancelled orders. Adjusted: the webhook now records a payment on a cancelled order and flags it for the merchant, instead of the pending-to-paid guard dropping it; the cancel is a conditional update after the provider call, with no lock held, so a webhook in between wins.

## Draft 3 (final)

Me: Two additions. If the cart changed since the pending order was created, checkout expires that order's provider session and cancels it with the 24 h job's rules; if the expiry fails because it was paid, show that order instead. Checkout asks the customer to confirm if the total changed since they last saw the cart. Then it's done.

Assistant: Added both. Adjusted: the provider call runs outside the cart lock, and checkout re-locks and checks again for a pending order, which keeps the double-click guard; "cart unchanged" now also compares prices with the order's snapshot, so a confirmed new total doesn't lead back to the old order at the old price.

Assistant: Open point: what does checkout do if the old session's expiry fails for another reason (provider unreachable)? Options: show an error and ask to retry (recommended), create the new order anyway, leave it in "Not decided here".

Me: Show an error, ask to retry.

Assistant: Added to the same decision: no new order while the old one might still be paid, so the customer can't pay twice.
