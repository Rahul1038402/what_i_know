---
difficulty: hard
last_sent: '2026-08-27T11:54:13.518900+00:00'
review_count: 5
tags:
- graph
- shortest-path
- heuristic
- pathfinding
topic: dsa
---

# A* (A-star) search

A* finds the shortest path between a **specific** source and destination, using a heuristic to guide the search. It's like Dijkstra with a sense of direction — instead of expanding equally in all directions, A* prioritizes nodes that look promising.

## Core formula

For each node `n`:

```
f(n) = g(n) + h(n)
```

- `g(n)` = actual cost from source to `n` (known)
- `h(n)` = heuristic estimate of cost from `n` to goal (guess)
- `f(n)` = total estimated cost of path through `n`

A* always expands the node with smallest `f(n)` next.

## The heuristic is everything

For A* to be **optimal** (find the true shortest path), the heuristic must be **admissible** — it never overestimates the actual remaining cost.

For A* to be **efficient**, the heuristic should be as close to the true cost as possible without going over.

| Heuristic | Used for | Admissible when |
|-----------|----------|-----------------|
| Manhattan distance | Grid with 4-directional movement | Movement is restricted to up/down/left/right |
| Euclidean distance | Grid with any-angle movement | Straight-line movement is allowed |
| Diagonal distance | Grid with 8-directional movement | Diagonals cost the same or more than orthogonal |
| Zero (`h(n) = 0`) | Always | Reduces A* to Dijkstra |

## Algorithm

1. Set `g(source) = 0`, push source into open set with `f = h(source)`
2. Pop node with smallest `f`. If it's the goal, reconstruct path.
3. For each neighbor:
   - Compute tentative `g = g(current) + edge_cost`
   - If this is better than known `g(neighbor)`, update and recompute `f`
   - Push (or update) neighbor in open set
4. Repeat until goal is reached or open set is empty

## Pseudocode

```python
import heapq

def a_star(start, goal, neighbors, h, edge_cost):
    g = {start: 0}
    open_set = [(h(start), start)]
    came_from = {}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct(came_from, current)
        for nxt in neighbors(current):
            tentative = g[current] + edge_cost(current, nxt)
            if tentative < g.get(nxt, float('inf')):
                came_from[nxt] = current
                g[nxt] = tentative
                f = tentative + h(nxt)
                heapq.heappush(open_set, (f, nxt))
    return None
```

## A* vs Dijkstra

| | Dijkstra | A* |
|---|---|---|
| Knows goal? | No | Yes |
| Heuristic? | None | Required |
| Search shape | Expands in all directions | Biased toward goal |
| Use when | Finding distances to ALL nodes | Finding path to ONE specific node |

## Use cases

- Game AI pathfinding (NPCs navigating maps)
- Robot navigation (ROS uses A* variants)
- GPS routing (with road-network heuristics)
- Puzzle solving (15-puzzle, Rubik's cube)
- Production planning, automated theorem proving

## Pitfalls

- Bad heuristic = worse than Dijkstra (more nodes expanded)
- Inadmissible heuristic = wrong answer (path is suboptimal)
- Memory: open and closed sets can grow large in big graphs