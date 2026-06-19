---
difficulty: medium
last_sent: '2026-06-19T06:42:23.505017+00:00'
review_count: 2
tags:
- graph
- shortest-path
- greedy
- priority-queue
topic: dsa
---

# Dijkstra's algorithm

Dijkstra finds the shortest path from a source node to all other nodes in a weighted graph with **non-negative edge weights**. It's a greedy algorithm — at each step, pick the closest unvisited node and relax its neighbors.

## The intuition

Imagine ripples spreading from the source. The ripple reaches each node by the shortest possible path. Once a node is "settled" (the ripple has reached it), its shortest distance is final.

## Algorithm

1. Set distance to source = 0, all others = infinity
2. Push source into a min-heap keyed by distance
3. Pop the node with smallest distance. If already settled, skip.
4. Mark it settled. For each neighbor, check if `dist[current] + weight(current, neighbor) < dist[neighbor]`. If yes, update and push into heap.
5. Repeat until heap is empty

## Pseudocode

```python
import heapq

def dijkstra(graph, source):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    heap = [(0, source)]
    
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # stale entry
        for v, weight in graph[u]:
            new_dist = d + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
    return dist
```

## Complexity

- With binary min-heap: **O((V + E) log V)**
- With Fibonacci heap: O(E + V log V) — theoretically faster, rarely used in practice
- Space: O(V)

## Critical limitation

**Does NOT work with negative edge weights.** Once a node is settled, Dijkstra assumes its distance is final — but a negative edge could create a shorter path later. Use **Bellman-Ford** for graphs with negative weights.

## Use cases

- GPS navigation (Google Maps, route planning)
- Network routing protocols (OSPF, IS-IS)
- Social network "degrees of separation"
- Game pathfinding (when no heuristic is available)

## Common interview variations

- Shortest path with at most K stops
- Network delay time (LeetCode 743)
- Cheapest flights within K stops
- Path with maximum probability