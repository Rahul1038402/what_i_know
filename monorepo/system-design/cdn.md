---
difficulty: easy
last_sent: '2026-07-17T04:43:42.599740+00:00'
review_count: 2
tags:
- cdn
- performance
- edge-computing
topic: system-design
---

# Content Delivery Network (CDN)

A CDN is a geographically distributed network of servers that caches content close to users. Think of it as having multiple warehouse branches worldwide instead of one central warehouse.

## How it works

1. **Edge servers** — CDN servers located globally that cache your content near users
2. **Origin server** — Your main server with original content. CDN fetches from here on cache miss.
3. **DNS routing** — Directs users to the nearest edge server based on their location
4. **Cache invalidation** — Updates cached content using TTL expiration, versioning (e.g. `app.v2.js`), or manual purge

## Request path

```
User (closest)
  → Edge server
    → Regional server
      → Origin server (furthest, last resort)
```

## Why use it

- **Lower latency** — 500ms drops to 50ms by serving content locally
- **Traffic absorption** — Handles spikes without overwhelming origin servers
- **Bandwidth savings** — 60-80% cost reduction since most requests never reach origin
- **DDoS protection** — CDN absorbs attack traffic across its global capacity

## What to cache

- Static assets (JS, CSS, images, fonts)
- Video segments (HLS .ts files)
- API responses with cacheable headers
- Fully-rendered HTML pages with short TTLs

## Real impact

Netflix streams globally using CDN. Without it, every user hitting US origin servers would cause massive delays and the service wouldn't be viable internationally.

## Popular tools

Cloudflare, AWS CloudFront, Akamai, Fastly, Bunny CDN