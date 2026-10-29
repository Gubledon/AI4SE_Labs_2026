# Task 1: architecture discussion notes (CDC shop)

Short notes kept by the assistant during the session. Not a transcript. "Me" is the student, "Assistant" is Claude Code.

## Setup

Me: My assigned project is CDC. Read the task and the requirements, propose next steps and keep notes.

Assistant: CDC is a two-role hardware store e-shop (customer, merchant) with 25 user stories: accounts, catalogue, search, sort by price, cart, payment, order status, product management. Gaps: no scale numbers, no payment provider or carrier named, no stock story. "Distributed system" is stated, but no story justifies it. I propose three candidates: modular monolith, microservices with a gateway, event-driven with CQRS. Is "distributed" a hard requirement or a label we can challenge?

Me: Keep the notes short and mark who said what.

## Architecture 1: modular monolith

Me: Challenge "distributed" but don't dismiss it. Present the monolith as the baseline that meets all stories and say which parts are already distributed.

Assistant: Modules Accounts, Catalogue, Cart, Orders+Payments, Content. One Postgres DB, each module owns its tables, separate frontend. Already distributed even here: browser to backend, external payment provider (async webhooks), carrier or merchant for shipment status, email service, DB host. So "distributed" is met by external parties, not by splitting our own code. Cheapest to build, one transaction for checkout, easy debugging. Risks: boundary erosion into a tangled monolith, all-or-nothing deploys. Painful parts: webhook idempotency, checkout race, price snapshot in order items, enforcing module boundaries, LIKE search not indexable.

Assistant: How should the order's paid status be set? Options: webhook only, redirect + webhook, synchronous charge.

Me: Webhook only.

Assistant: Order starts as `pending_payment`, the return page polls, a unique event ID makes duplicate webhooks a no-op, and a job checks orders stuck in pending with the provider.

Assistant: Where does the package status for story 9 come from? Options: merchant updates it, carrier API polling, carrier webhooks.

Me: Merchant updates it.

Assistant: The merchant needs a small screen (packed, shipped, tracking number) that no story covers, so it goes into the ADR as an assumption.

Assistant: Should we track stock, even though no story mentions it? Options: simple stock count, no stock, reservation at cart time.

Me: No stock.

Assistant: Overselling is an accepted risk, and product removal must be a soft delete, because orders reference products.

Assistant: How should module boundaries be enforced? Options: separate packages, lint rule on imports, convention only.

Me: Separate packages.

Assistant: Each package exports one facade and keeps repositories internal, which also makes a later split into services cheaper.

Me: Let's discuss it more thoroughly, do I actually understand the architectures, trade-offs and painful parts?

Assistant: Scenario: the customer pays, the provider charges the card, but our server is down when the webhook arrives. What happens to the order? Options: stays pending forever, paid once server is back, customer charged twice.

Me: Stays pending forever.

Assistant: Usually not. Providers retry webhooks for up to a few days, so the order becomes paid when the server is back, and the stuck-order job is a second safety net. My answer does happen with one common bug: the handler replies 200 before its transaction commits and then crashes, so the provider never retries. Rule: commit first, reply 200 last.

## Architecture 2: microservices with API gateway

Assistant: Gateway (routing, token validation) plus Identity, Catalogue, Cart, Order and Payment services, each with its own DB. New compared to Arch 1: our own logic crosses processes and data ownership is split. Webhook only now needs an outbox in Payment and idempotency in Order. No stock removes the need for a compensating saga. Gains: independent deploys, fault isolation. Costs: no cross-service transactions, network failures, heavy local dev, tracing needed. Painful parts: checkout across three services, price snapshots, removed products left in carts, product names in order history, logout with JWTs, contract changes.

Assistant: How finely should we split services? Options: 3 services (Identity, Catalogue, Ordering = cart + order + payment), 5 services, 2 services.

Me: 3 services.

Assistant: Checkout is one transaction again and the webhook lands where the order lives, so the outbox and two-hop idempotency go away.

Assistant: How should services talk to each other? Options: sync HTTP only, HTTP + message broker, events only.

Me: Sync HTTP only.

Assistant: Ordering fetches prices and names from Catalogue at checkout and snapshots them. A batch call when viewing a cart also handles removed products. These calls are reads, so retries are safe, but if Catalogue is down there's no checkout, so we need timeouts and a clear error.

Assistant: How should logout (stories 8, 13) work when the gateway validates tokens? Options: short JWT + refresh token, gateway sessions, revocation list.

Me: Short JWT + refresh token.

Assistant: The gateway verifies tokens with Identity's public key. Logout revokes the refresh token and the session ends within about 5 minutes. Role changes also take up to 5 minutes.

Assistant: After these choices, Arch 2 is "the monolith with Catalogue and Identity pulled out": real but small distribution (timeouts, retries, token validation, three deploys instead of one).

Assistant: Scenario: the Catalogue service is down. Which stories still work? Options: nothing works, login + profile + order status, all except browsing.

Me: Login, profile, order status.

Assistant: Correct. Cart view and checkout need prices from Catalogue, so they fail. Order status only works because names and prices are snapshotted into the order at checkout. Without the snapshot, order history would break too.

## Architecture 3: event-driven with CQRS

Assistant: Commands (change price, add product, place order) go to a write side that stores state and publishes events (`ProductPriceChanged`, `OrderPlaced`, `PaymentConfirmed`, `OrderShipped`). Consumers on a broker update read models shaped per screen. Fits the read-heavy catalogue and the order lifecycle; accounts, cart and content gain nothing. Newly distributed: a broker, async consumers, eventual consistency between write and read side. Gains: fast read models, audit trail, new reactions plug in easily. Costs: visible lag in the UI, broker to run, harder debugging, event versioning.

Assistant: How much of the system should be event-driven? Options: catalogue + orders, order lifecycle only, whole system.

Me: Catalogue + orders.

Assistant: Two read models: product list (name search, price sort) and "my orders" with status. Webhook becomes `PaymentConfirmed`, merchant actions become `OrderPacked` and `OrderShipped`. Checkout must read prices from the write side, never from the read model.

Assistant: How should the write side store its state? Options: state + outbox, event sourcing.

Me: State + outbox.

Assistant: A relay polls the outbox and publishes. Delivery is at least once, so each consumer keeps a processed-events table. The outbox needs a cleanup job.

Assistant: Which message broker? Options: RabbitMQ, Kafka, Postgres as queue.

Me: RabbitMQ.

Assistant: No replay, so a broken read model is rebuilt from the write tables. Events can arrive out of order, so each carries a version and consumers ignore older ones. Failing messages go to a dead-letter queue that someone has to watch.

Assistant: A merchant changes a price and the list still shows the old one. How do we handle that lag? Options: merchant reads write side, wait for projection, accept the lag.

Me: Merchant reads write side.

Assistant: Merchants always see their change at once, but list, search and sort now have two code paths (customer vs. merchant) that will drift unless shared.

Assistant: For these 25 stories, Arch 3 is the most machinery (broker, relay, consumers, versions, dead-letter queue). It pays off only if more event reactions are coming (emails, analytics, warehouse).

Assistant: Scenario: the merchant changes a price 100 to 80, then 80 to 90 a second later. Two consumers, no version check. What can customers end up seeing? Options: 90 always, 80 until next change, 100.

Me: 90, always.

Assistant: That's the trap. RabbitMQ keeps order within a queue, but two competing consumers can finish in the wrong order: 90 is written first, then 80 overwrites it. Requeued failed messages also break ordering. Fixes: version number on each event (ignore older), a single active consumer, or routing all events of one product to the same consumer.

## Checkout walkthrough (all three)

Me: Walk one checkout step by step through all three architectures and include me in it.

Assistant: Same scenario everywhere: a logged-in customer with two items clicks Pay. Arch 1: lock cart, snapshot prices, create pending order, commit, create payment session, redirect, poll, webhook marks paid. Arch 2: gateway checks JWT, Ordering fetches prices from Catalogue (2 s timeout), locks cart, creates order, creates payment session, webhook arrives at the gateway. Arch 3: write side locks cart, reads prices from write tables, inserts order + `OrderPlaced` into the outbox in one transaction, creates payment session, relay and consumer update the "my orders" read model, webhook adds `PaymentConfirmed`.

Assistant: Arch 1, step 3: should the provider call happen inside the DB transaction or after it commits?

Me: Inside the transaction.

Assistant: Looks atomic, but isn't. It holds the cart lock and a DB connection during a slow external call, so under load the pool runs dry and the whole shop stalls. And if the provider times out on our side but succeeded on theirs (or our commit fails after it), we roll back while the provider holds a live session. Usual answer: call after commit, accept orphan pending orders (stuck-order job cleans them), pass the order ID as an idempotency key to the provider.

Assistant: Arch 2, step 5: the gateway rejects requests without a JWT, the provider has none. How does the webhook reach Ordering? Options: exempt the path, give the provider a token, bypass the gateway.

Me: Exempt the path.

Assistant: Correct. Painful detail: the signature is over the raw body bytes, so if the gateway re-serialises JSON, decompresses or re-encodes, every webhook fails verification. Pass the path through untouched, add rate and body-size limits.

Assistant: Arch 3, step 4: the customer is back on the order page, but the read model hasn't processed `OrderPlaced` yet. What should the page do? Options: read the write side, show "processing" and poll, show "not found".

Me: Show "processing".

Assistant: Works, but the spinner needs a time limit (if the event is stuck in the dead-letter queue it spins forever). The customer also waits twice: once for `OrderPlaced`, again for `PaymentConfirmed`. The consumer can see `PaymentConfirmed` before `OrderPlaced` and must retry, not drop it. Reading order detail from the write side avoids all this, which is why many CQRS systems do it.
