---
difficulty: hard
last_sent: '2026-05-27T05:55:28.932411+00:00'
review_count: 1
tags:
- consistent-hashing
- distributed-systems
- scalability
- hashing
topic: system-design
---

# Consistent hashing

Consistent Hashing is a distributed hashing technique that minimizes data redistribution when nodes are added or removed. Think of it as a circular seating arrangement where adding a new chair only affects neighbors, not the entire room.

## The problem it solves

Traditional hashing uses `hash(key) % num_servers`. Adding or removing one server reshuffles ALL data — 80-90% of keys move. Cache hit rate plummets, databases get hammered with re-fetches.

Consistent hashing: only ~1/N keys move when changing N servers. Massive operational improvement.

## How it works

1. **Hash ring** — Virtual circle (0 to 2^32-1) where both servers and keys are hashed onto positions on the ring
2. **Key placement** — Each key is assigned to the first server found when moving clockwise from the key's position
3. **Adding nodes** — Only keys between the new node and its predecessor need to move. Everything else stays put.
4. **Virtual nodes** — Each physical server gets multiple positions on the ring (e.g. 100 virtual nodes per server) for better load distribution and smoother rebalancing on failure

## Why virtual nodes matter

Without them, the ring distribution is uneven — some servers get huge arcs, others get tiny ones. With 100+ virtual nodes per physical server, the law of large numbers smooths it out.

## Why use it

- **Cache stability** — Adding a cache node only invalidates ~1/N keys instead of all keys
- **Seamless scaling** — Horizontal scaling without massive data movement
- **Predictable distribution** — Works the same regardless of cluster size
- **Graceful failures** — When a node dies, only its keys redistribute to neighbors

## Real impact

Amazon DynamoDB uses consistent hashing to partition data across thousands of nodes. When adding capacity, only a small fraction of data moves, keeping the system available during scaling operations.

## Popular tools / use cases

Memcached (client-side consistent hashing), Redis Cluster, Cassandra, DynamoDB, Riak, Chord DHT, Akamai's content routing