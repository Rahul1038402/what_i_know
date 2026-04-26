---
topic: system-design
difficulty: easy
tags: [load-balancing, scalability, high-availability]
last_sent: null
review_count: 0
---

# Load Balancer

A Load Balancer distributes incoming traffic across multiple servers to prevent any single server from being overwhelmed. Think of it as a traffic cop directing cars to different lanes to keep traffic flowing smoothly.

## How it works

1. **Health checks** — Continuously monitors servers and stops routing to failed ones
2. **Distribution algorithms**:
   - Round Robin — equal turns
   - Least Connections — pick the least busy server
   - IP Hash — same client always hits the same server
3. **SSL termination** — Handles encryption/decryption, reducing backend workload
4. **Session persistence** — Keeps users connected to the same server when needed

## Types

- **Layer 4 (Transport)** — Routes by IP/port. Faster but basic.
- **Layer 7 (Application)** — Routes by URL/headers. Smarter and more flexible.

## Why use it

Provides high availability (automatic failover), better performance (distributed workload), and easy horizontal scaling — add servers without downtime. If one server crashes, traffic automatically routes to healthy servers.

## Popular tools

AWS ELB/ALB, Nginx, HAProxy, Cloudflare Load Balancing
