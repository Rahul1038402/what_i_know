---
difficulty: medium
last_sent: '2026-07-21T04:49:01.201642+00:00'
review_count: 3
tags:
- replication
- database
- high-availability
- master-slave
topic: system-design
---

# Database replication

Database replication creates copies of your database across multiple servers to improve read performance and availability. Think of it as photocopying important documents and storing them in different locations for faster access and backup.

## How it works

1. **Master (primary)** — Handles all write operations. Single source of truth for data changes.
2. **Slaves (replicas)** — Read-only replicas that sync data from master. Handle read queries to distribute load.
3. **Replication process** — Master logs changes (binlog/WAL); slaves continuously pull and apply these changes.
4. **Failover** — If master fails, a slave is promoted to master. Ensures system stays operational during outages.

## Replication types

- **Synchronous** — Slave confirms write before master responds. Strong consistency but slow.
- **Asynchronous** — Master responds immediately; slaves sync later. Fast but replication lag means slaves can serve stale reads.
- **Semi-synchronous** — At least one slave confirms. Balanced approach used by MySQL.

## Why use it

- **Read scaling** — 10x+ read throughput as multiple slaves handle queries
- **High availability** — Automatic failover if master crashes
- **Geographic latency** — Serve reads from slaves closer to users
- **Zero-downtime maintenance** — Switch traffic to replicas during master upgrades

## Common pitfalls

- **Replication lag** — Read-after-write inconsistency (write to master, immediately read from slave shows stale data). Solution: route critical reads to master.
- **Split brain** — Two nodes both think they're master after a network partition
- **Slave drift** — Slaves slowly fall behind under heavy write load

## Real impact

Facebook uses master-slave replication with hundreds of read replicas per master. With billions of users reading posts constantly, a single database would bottleneck within seconds.

## Popular tools

MySQL Replication, PostgreSQL Streaming, MongoDB Replica Sets, AWS RDS Multi-AZ, Patroni