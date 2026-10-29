# Task 1: architecture discussion notes (CDC)

Start: 9:31
End: 9:57

Short notes kept by the assistant during the session. Not a transcript. "Me" is the user, "Assistant" is Claude Code.

## Setup

Me: My project is CDC.

## Requirements and candidates

Assistant: CDC is a hardware-store web shop with Customer and Merchant roles and 25 stories: auth 7, catalogue browse/search/sort 8, cart 3, payment 1, package tracking 1, product management 2, About Us and contact 3. Gaps: no traffic or size numbers; payment provider, carrier and contact channel unnamed; no story says who creates a shipment or sets package status; no stock, order history, refunds or merchant order view. "CDC shop is a distributed system" is a constraint no story justifies. Candidates: 1. modular monolith, 2. a few services behind a gateway, 3. event-driven with CQRS on the catalogue. How do we treat "distributed system"? Options: challenge it but don't dismiss it (recommended), take it literally, ignore it.

Me: Challenge it, don't dismiss it.

Assistant: Option 1 stays as the baseline. The ADR will list what is already distributed (browser to backend, payment provider and webhooks, carrier, email, DB host) and carry a "Bad" consequence that a reviewer may read the constraint literally.

## Architecture 1: modular monolith

Assistant: One backend and one PostgreSQL DB, with modules Accounts (1, 2, 3, 8, 13, 14, 19; Merchant is a role), Catalogue (5, 6, 11, 12, 15-18, 21, 22; soft delete for 16), Cart & Orders (4, 24, 25; checkout copies name and price into order items), Payment (7; hosted checkout plus webhook), Shipping (9) and static pages with a contact form (10, 20, 23). Gains: cart, order and payment share one transaction; one thing to deploy. Costs: scales and fails as one unit. Painful parts: duplicate webhooks (unique event ID), commit before replying 200, signature over raw bytes, no provider call inside a DB transaction, double-click checkout (lock the cart row), don't clear the cart at checkout.

Assistant: How does an order become paid? Options: webhook plus reconcile job (recommended), webhook only, return page only.

Me: Webhook plus reconcile job.

Assistant: `payment_events` with a unique provider event ID; the webhook verifies the raw body, sets the order paid and commits before replying 200. A job asks the provider about orders pending over ~15 min and uses the same pending-to-paid transition, so a payment can't apply twice.

Assistant: Where does package info (story 9) come from? Options: carrier API (recommended), merchant sets it manually, tracking link only.

Me: Carrier API.

Assistant: The webhook writes a `shipments` row (`to_create`) in its transaction; a job creates the shipment at the carrier with the order ID as reference, and another polls status. Assumptions: a shipping address in the profile and a merchant packing view, neither in the stories.

Assistant: Stock isn't in any story. Add it? Options: count decremented when paid (recommended), no stock, reserve at checkout.

Me: Count, decrement when paid.

Assistant: `products.stock`, checked at checkout and decremented in the webhook. No `CHECK (stock >= 0)`, because a paid webhook must not fail; negative stock flags the order for the merchant. Assumption: a merchant screen to set stock.

Assistant: How do login and logout work? Options: server-side sessions (recommended), stateless JWT.

Me: Server-side sessions.

Assistant: A `sessions` table and an HttpOnly cookie with CSRF protection. Logout (8, 13) deletes the row and works at once; merchant pages check the role.

Assistant: Quiz: the monolith is down for an hour and a customer pays during it. What happens? Options: order stays pending forever, becomes paid later, customer charged twice.

Me: Becomes paid later.

Assistant: Correct. The provider retries the webhook, and the reconcile job catches it if retries run out; the event ID makes it apply once. "Pending forever" happens with webhook only, or if the handler replies 200 before commit. The customer's return page fails during the outage even though they paid.

Assistant: Arch 1 for CDC is one deployable where cart, order, payment and stock share one transaction; only the provider, carrier and email are distributed.

## Architecture 2: a few services behind a gateway

Assistant: A gateway (routing, session check, webhook path passed through untouched) in front of Identity (1, 2, 3, 8, 13, 14, 19), Catalogue (5, 6, 11, 12, 15-18, 21, 22) and Ordering (4, 7, 24, 25, maybe 9); static pages and contact stay with the frontend. New: checkout needs prices from Catalogue, and anything outside Ordering splits the webhook transaction. Gains: browsing survives an Ordering outage, Catalogue scales alone, "distributed" met literally. Costs: no cross-service transaction, contract versioning, every service needed for local dev. Carried forward: webhook plus reconcile stays simple only with payment and order together; the shipments row needs an outbox if Shipping leaves Ordering; sessions now need a lookup from the gateway.

Assistant: How fine is the split? Options: 3 services, Identity, Catalogue, Ordering (recommended); 4 with a separate Shipping; one service per module.

Me: 3 services.

Assistant: Ordering holds cart, order, payment, shipping and stock in its own DB, so the webhook transaction is unchanged from Arch 1. `order_items.product_id` has no cross-DB foreign key; snapshots keep order history readable when Catalogue is down.

Assistant: Where does stock live? Options: in Ordering (recommended), in Catalogue decremented by event, in Catalogue by sync call.

Me: In Ordering.

Assistant: A `stock(product_id, qty)` table in Ordering; a missing row means 0, so a new product (16) can't be bought until the merchant sets stock through Ordering. ADR assumption.

Assistant: How does checkout get prices? Options: sync call at checkout (recommended), local replica via events, price stored when added to cart.

Me: Sync call at checkout.

Assistant: Ordering calls Catalogue with a ~2 s timeout, rejects removed products, copies name and price, and asks the customer to confirm if the total changed. The cart view (4) also depends on Catalogue for names and prices.

Assistant: How does the gateway check who is logged in? Options: gateway asks Identity (recommended), short JWT plus refresh token.

Me: Gateway asks Identity.

Assistant: The gateway validates the session with Identity and caches it ~5 s, so logout works within 5 s. It passes user ID and role as headers, which services must accept only from the gateway. The webhook path is exempt.

Assistant: Quiz: Identity is down for 10 minutes. What still works? Options: only browsing and About Us; everything but login, register and logout; browsing plus webhooks paying orders.

Me: Browsing, plus webhooks pay orders.

Assistant: Correct. The webhook skips the session check and goes straight to Ordering; logged-in calls fail once the ~5 s cache expires. "Only browsing" would be true if the webhook went through the session check by mistake; "all but login" would be true with JWTs or a long cache.

Assistant: Arch 2 for CDC is the monolith with Identity and Catalogue pulled out; Ordering is still the Arch 1 core with one transaction.

## Architecture 3: event-driven with CQRS on the catalogue

Assistant: The Arch 2 services publish events through an outbox and a broker. A search-oriented Catalogue read model, built from `ProductCreated`, `PriceChanged` and `ProductRemoved`, serves the browse stories; the write side keeps 15 and 16. Ordering publishes `OrderPaid` for shipping, email and the tracking view. Gains: catalogue reads scale and search better, new consumers don't touch Ordering, outages become queues. Costs: lag, a broker to run, outbox relay, idempotent consumers, a watched dead-letter queue. Painful parts: merchant doesn't see their own price change, reordered events need versions, two read paths drift. Carried forward: checkout still reads prices from the write side; the shipments row becomes the `OrderPaid` outbox row.

Assistant: Which flows become events? Options: catalogue changes plus `OrderPaid` (recommended), everything with checkout as a saga, catalogue only.

Me: Catalogue changes plus `OrderPaid`.

Assistant: Catalogue publishes product events with a per-product version; Ordering publishes `OrderPaid`. Shipping becomes a small consumer service with its own `shipments` table and serves story 9; an email consumer sends confirmations. Checkout stays synchronous.

Assistant: How do the write sides store state? Options: state tables plus outbox (recommended), event sourcing.

Me: State tables plus outbox.

Assistant: An `outbox` table in Catalogue and Ordering, written in the same transaction; a relay publishes and marks rows. Delivery is at least once, so each consumer keeps `processed_events`.

Assistant: Which broker? Options: RabbitMQ (recommended), Kafka, no broker with Postgres outbox polling.

Me: RabbitMQ.

Assistant: One queue per consumer plus a dead-letter queue. The projector applies an event only if its version is newer. No replay, so a rebuild re-projects from the Catalogue write tables.

Assistant: How do screens handle read-model lag? Options: merchant reads write side (recommended), everyone reads the read model, poll until the version matches.

Me: Merchant reads write side.

Assistant: Merchant stories 17, 18, 21, 22 query the write DB, customer stories 5, 6, 11, 12 the read model; search and sort rules must be shared. Checkout's confirm step catches a price that changed during the lag.

Assistant: Quiz: price goes 10 to 12 to 11 within a second, two projector instances, the 11 event finishes first. What do customers see? Options: 11, 12, 10.

Me: 11.

Assistant: Correct. The projector skips the version 2 event because version 3 is already stored. Without the version check it would show 12; a projector that demands exactly `stored + 1` would drop version 3 and also end at 12.

Assistant: Arch 3 for CDC is Arch 2 with an event-fed catalogue read model and `OrderPaid` driving shipping and email; checkout stays synchronous.

## Core flow: checkout and payment

Assistant: Walked checkout through all three. Arch 1: lock cart, check stock, create pending order with snapshots (or return the existing one), commit; create the provider session with the order ID as idempotency key; webhook sets paid, decrements stock, removes ordered items from the cart, writes the shipments row. Arch 2: the same, plus the gateway session check and a sync price call to Catalogue before the order is created. Arch 3: the same, plus the `OrderPaid` outbox row feeding Shipping and Email. Decision points: Arch 1, where the provider call sits relative to the transaction; Arch 2, how the webhook passes the gateway; Arch 3, what the order page shows while status lags.

Assistant: Arch 1: where does the provider session call go? Options: after commit with an idempotency key (recommended), inside the transaction, before creating the order.

Me: After commit, idempotency key.

Assistant: `orders.provider_session_id` is nullable. If the call fails, the order stays pending; paying again returns the same order and retries with the same key, so the provider returns the same session.

Assistant: Arch 2: how does the webhook get through the gateway? Options: exempt path verified in Ordering (recommended), gateway verifies the signature, separate public endpoint.

Me: Exempt path, verify in Ordering.

Assistant: The gateway route has auth off and passes the raw body unchanged; Ordering checks the HMAC before parsing. A test with a signed payload through the real gateway config catches drift.

Assistant: Arch 3: what does the order page show before the webhook arrives? Options: poll Ordering with a time limit (recommended), trust the return URL, read the Shipping view.

Me: Poll Ordering, time limit.

Assistant: The page polls Ordering every 2 s for up to 30 s, then says payment is being confirmed and the email follows. Status always comes from the write side. Open point for the ADR: nothing cancels an abandoned pending order.
