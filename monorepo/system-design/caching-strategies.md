---
difficulty: medium
last_sent: '2026-08-10T03:28:06.324678+00:00'
review_count: 4
tags:
- caching
- performance
- redis
- memcached
topic: system-design
---

# Caching strategies

Caching stores frequently accessed data in fast storage to reduce latency and database load. Think of it as keeping your most-used items on your desk instead of walking to the storage room every time.

## Patterns

1. **Cache-Aside (Lazy Loading)** — Application checks cache first. On miss, fetch from DB, then store in cache. Most common pattern.
2. **Write-Through** — Data written to cache AND database simultaneously. Ensures consistency but slower writes.
3. **Write-Back (Write-Behind)** — Data written to cache first, then asynchronously to database. Fast writes but risk of data loss on cache failure.
4. **Read-Through** — Cache automatically loads data from database on miss. Application only talks to cache.
5. **Write-Around** — Data written directly to database, bypassing cache. Cache only fills on reads. Good for write-heavy workloads with infrequent reads.

## Cache layers

```
Browser cache (static assets)
  → CDN (global content delivery)
    → Application cache (Redis / Memcached)
      → Database cache (query results, buffer pool)
```

## Why use it

- Reduces database load by 80-90%
- Improves response time from seconds to milliseconds
- Handles traffic spikes without scaling databases
- Lowers infrastructure cost by deferring DB scaling

## Trade-offs to remember

- Cache invalidation is one of the hardest problems in CS
- Stale data risk with async patterns
- Memory cost — caches are RAM, RAM is expensive
- Cache stampede when many requests miss simultaneously

## Popular tools

Redis, Memcached, Varnish, Hazelcast