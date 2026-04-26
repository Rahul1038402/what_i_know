---
topic: system-design
difficulty: medium
tags: [message-queue, async, kafka, rabbitmq, decoupling]
last_sent: null
review_count: 0
---

# Message queues

Message Queues enable asynchronous communication between services by temporarily storing messages until they're processed. Think of it as a post office mailbox where senders drop letters without waiting for recipients to read them.

## How it works

1. **Producer** — Service that sends messages to the queue without waiting for processing completion
2. **Queue** — Persistent storage that holds messages in order until consumers are ready
3. **Consumer** — Service that pulls messages and processes them at its own pace
4. **Acknowledgment** — Consumer confirms successful processing. On failure, message returns to queue for retry.

## Patterns

- **Point-to-point**: One message → one consumer (task processing)
- **Pub/Sub**: One message → multiple consumers (event broadcasting)
- **Priority queue**: High-priority messages processed first
- **Dead letter queue**: Failed messages routed to a separate queue for inspection

## Why use it

- **Decoupling** — Producers don't wait for slow consumers, preventing cascading failures
- **Spike absorption** — Buffers requests during peak loads instead of overwhelming downstream
- **Retry logic** — Failed operations automatically retry without custom code
- **Delivery guarantees** — Messages persist even if consumers are temporarily down

## Delivery semantics

- **At-most-once** — Fast, but messages can be lost
- **At-least-once** — Messages may be duplicated; consumers must be idempotent
- **Exactly-once** — Hardest to achieve; usually requires consumer-side dedup

## Real impact

Uber uses queues for ride matching. When you request a ride, the request goes to a queue. Driver matching happens asynchronously without blocking your app. During surge, queues buffer millions of requests instead of dropping them.

## Popular tools

RabbitMQ, Apache Kafka, AWS SQS, Redis Pub/Sub, Google Pub/Sub, NATS, Amazon Kinesis
