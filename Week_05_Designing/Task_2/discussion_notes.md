# Task 2: ADR discussion notes (CDC shop)

Short notes kept by the assistant during the session. Not a transcript. "Me" is the student, "Assistant" is Claude Code.

## Setup

Me: Let's head into Task 2, an ADR based on the Task 1 discussion. Keep notes like in Task 1.

Assistant: Which architecture should the ADR choose? Options: modular monolith, 3 services, event-driven + CQRS.

Me: Modular monolith.

Assistant: Which ADR template? Options: MADR (context, drivers, options with pros and cons, outcome, consequences), Nygard (short: context, decision, consequences).

Me: MADR.

## Draft 1

Assistant: Wrote `ADR-001-cdc-architecture.md`. Sections: context, decision drivers, three considered options, decision outcome with the design decisions from Task 1 (webhook only, provider call after commit, cart lock, price snapshot, no stock, manual shipment status), consequences, assumptions, what is not decided (auth, search, deployment), when to revisit, pros and cons per option. No overview table or diagram yet.

## Draft 2

Me: Good draft. Add design decisions: verify the webhook signature on the raw body, clear the cart only when the order is paid, checkout rejects soft-deleted products, cart shows current prices and checkout warns if the total changed, the job cancels pending orders after about 24 h. Add a "Bad" consequence that the decision depends on reading "distributed" as including external parts. Add a comparison table (drivers × options) and a diagram of the chosen architecture. Keep it concise.

Assistant: Added all of it. Table sits after "Considered options", diagram after the decision paragraph. One addition to the timeout: the job cancels only after the provider confirms the session wasn't paid, and expires the session, because providers retry webhooks for days and a late payment could hit a cancelled order. Open point: since the cart stays intact while an order is pending, the customer can edit it and check out again, which leaves two pending orders. Not decided in the ADR.

## Draft 3

Me: Keep the 24-hour change. For the open point, cancel the earlier pending order at checkout, but ask the provider first: unpaid means cancel it and expire the session, paid means show that order, still processing means refuse the new checkout and tell the customer to finish or wait. And when an order is paid, remove only its items from the cart, not the whole cart.

Assistant: Added both. Two adjustments: a double click would otherwise cancel the order the first click just created, so checkout returns the pending order when the cart is unchanged and only runs the provider check when it changed. And the provider is asked before the cart lock is taken (no slow external call while holding the lock, as in Task 1), with the order status re-read inside the transaction in case the webhook landed in between.

## Draft 4

Me: One last change. In both checkout and the 24-hour job, expire the payment session before cancelling the order, and treat a failed expiry as "paid". If a paid webhook arrives for a cancelled order, record the payment and flag the order for the merchant to refund or reinstate.

Assistant: Done, one or two sentences each. "Treated as paid" means the order is kept, not marked paid in the database: checkout shows it instead of creating a new one, and the job retries on its next run. The refund-or-reinstate flag needs a merchant screen that no story covers, same as the shipment status screen.
