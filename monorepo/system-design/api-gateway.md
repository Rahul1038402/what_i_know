---
difficulty: easy
last_sent: '2026-08-30T07:13:03.036691+00:00'
review_count: 4
tags:
- api-gateway
- microservices
- architecture
topic: system-design
---

# API Gateway

An API Gateway is the single entry point for all client requests. Think of it as a smart receptionist that handles everything before requests reach your backend services.

## How it works

1. **Request routing** — Directs requests to the right microservice based on URL path
2. **Authentication & authorization** — Validates tokens and API keys before allowing access
3. **Rate limiting** — Protects services from overload
4. **Response aggregation** — Combines data from multiple services into one response
5. **Protocol translation** — Converts between formats (REST to gRPC, HTTP to WebSocket)

## Why use it

Clients call ONE endpoint instead of managing URLs for 10+ microservices. All security, monitoring, and rate limiting happen in one place — no duplication across services.

## Popular tools

AWS API Gateway, Kong, Nginx, Apigee