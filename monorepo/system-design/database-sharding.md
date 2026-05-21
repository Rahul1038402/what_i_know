---
difficulty: hard
last_sent: '2026-05-21T05:48:53.308324+00:00'
review_count: 1
tags:
- sharding
- database
- scalability
- partitioning
topic: system-design
---

# Database sharding

Sharding is a horizontal partitioning technique that splits large datasets across multiple independent database servers. Think of it as splitting a massive library into multiple buildings, each holding different sections based on specific rules.

## How it works

1. **Shard key** — The field used to determine data placement (e.g. `user_id`, `region`). Choosing the right key is the most critical decision.
2. **Partitioning logic** — Algorithm that routes queries to correct shards. Hash-based, range-based, or geographic.
3. **Routing layer** — Middleware that tracks shard locations and directs queries to appropriate databases.
4. **Rebalancing** — Redistributes data when adding shards or fixing hotspots. Complex and requires careful migration.

## Strategies

- **Hash-based**: `hash(key) % num_shards` — even distribution, but adding shards reshuffles data
- **Range-based**: A-M on shard1, N-Z on shard2 — easy range queries, but risk of hotspots
- **Geographic**: EU users → EU shard for compliance and latency
- **Directory-based**: Lookup table maps keys to shards — flexible, but the lookup table becomes a bottleneck

## Why use it

- **Storage scaling** — Move beyond single-server limits (2TB → 100TB+)
- **Query speed** — Smaller dataset per server means faster queries
- **Write throughput** — Distribute writes across machines instead of one master
- **Data sovereignty** — Store user data in specific regions for legal compliance

## Trade-offs

- Cross-shard queries become expensive (require scatter-gather)
- Joins across shards are painful
- Transactions across shards need distributed consensus
- Resharding when load grows is operationally hard

## Real impact

Instagram shards by `user_id` across thousands of databases. With 2B+ users, a single database would collapse under storage and write load.

## Popular tools

Vitess, Citus (Postgres), MongoDB (built-in), Apache ShardingSphere, Cassandra, CockroachDB