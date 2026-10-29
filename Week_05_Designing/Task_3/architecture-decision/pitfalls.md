# Low-level pitfalls to raise in the discussion

Use the ones that fit the domain. Each line is a problem, then the usual fix.

## Payments and webhooks

- Duplicate webhooks: the provider resends. Store the provider's event ID under a unique constraint, so a duplicate becomes a no-op.
- Reply before commit: the handler replies 200, then crashes before committing, so the provider never retries. Commit first, reply 200 last.
- Lost webhook: the order stays pending. A job asks the provider about orders stuck in pending.
- Signature over raw bytes: any proxy or gateway that re-serialises, decompresses or re-encodes the body breaks verification. Verify before parsing, and pass the path through untouched.
- External call inside a DB transaction: holds locks and connections during a slow call, and still isn't atomic. Commit first, call after, and pass the order ID as an idempotency key.
- Cancelling a pending order: the provider may still accept payment. Ask the provider first, expire the session before cancelling, and treat a failed expiry as "maybe paid" (keep the order).
- Late payment on a cancelled order: record it and flag the order for the merchant to refund or reinstate.

## Data and checkout

- Checkout race and double click: lock the cart row, and return the existing pending order if the cart is unchanged.
- Price changes after checkout: copy the name and price into the order items. Never join back to the product.
- Removed products: soft delete, because orders reference them. Checkout rejects removed products.
- Price shown vs. charged: compare the total the customer saw with the checkout total, and ask for confirmation if it changed.
- Abandoned payment: don't clear the cart at checkout. When paid, remove only the ordered items.
- Unstated stock: without stock, overselling is an accepted risk. Reservations need a cleanup job.

## Services

- No cross-service transaction: keep the transactional flow (cart, order, payment) inside one service if the user allows it.
- Synchronous dependency: if the service that owns prices is down, checkout fails. Use timeouts and a clear error. Retries are safe only for reads.
- Snapshots keep history working when another service is down.
- Gateway and webhooks: exempt the webhook path from token checks, and verify the provider's signature in the service.
- Logout with stateless tokens: use short access tokens and revoke the refresh token. Logout and role changes take effect only after the access token expires.
- Contract changes between services: version the APIs or add contract tests.
- Local development needs every service and its DB running.

## Events and CQRS

- Event and state in one transaction: use an outbox table plus a relay. Delivery is at least once.
- Duplicate delivery: each consumer keeps a processed-events table.
- Competing consumers reorder events: put a version on each event and ignore older ones, or use a single active consumer, or route by key.
- Requeued failures also reorder events. Poison messages go to a dead-letter queue someone watches.
- No replay (RabbitMQ): rebuild a read model from the write tables.
- Read your own writes: the merchant or customer doesn't see their own change. Read that screen from the write side.
- A UI that polls a lagging read model needs a time limit. The customer may wait once per event.
- A consumer can see "paid" before "placed": retry, don't drop.
- Two read paths (read model and write side) for the same list, search and sort will drift unless shared.
- Checkout must read prices from the write side, never from a read model.
