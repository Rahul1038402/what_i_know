---
difficulty: medium
last_sent: '2026-05-28T05:51:48.051120+00:00'
review_count: 1
tags:
- pattern
- two-pointers
- linked-list
- cycle-detection
topic: dsa
---

# Slow-fast pointer (Floyd's tortoise and hare)

Two pointers traversing the same structure at **different speeds**. The slow pointer advances 1 step per iteration; the fast pointer advances 2. Used primarily for cycle detection and finding "middle" positions in linked lists. Time **O(n)**, space **O(1)**.

## Core idea

If a sequence has a cycle, the fast pointer will eventually lap the slow pointer and they'll meet inside the cycle. If there's no cycle, the fast pointer reaches the end first.

## Cycle detection (Floyd's algorithm)

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

If a cycle exists, `slow` and `fast` will meet in **at most n steps**, where n is the cycle length.

## Find the cycle's start node

After they meet, reset one pointer to head and advance both at the same speed. They meet again at the cycle's start.

```python
def cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None
    
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    return slow
```

**Why does this work?** Math: if `m` is the distance from head to cycle start, and `k` is the distance from cycle start to meeting point, then the distance from meeting point back to cycle start (going forward through the cycle) equals `m`. So advancing one pointer from head and the other from the meeting point at the same speed makes them meet exactly at the cycle start.

## Find the middle of a linked list

When `fast` reaches the end, `slow` is at the middle. For even length, slow points to the second middle node.

```python
def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

## Other applications

| Problem | How |
|---------|-----|
| Detect cycle in linked list | Floyd's |
| Find cycle start | Two-phase Floyd's |
| Cycle length | After meeting, walk slow until you meet fast again |
| Middle of linked list | Slow=1x, fast=2x, return slow |
| Palindrome linked list | Find middle, reverse second half, compare |
| Happy number (LC 202) | Treat number transformation as a graph; cycle detection |
| Reorder list | Find middle, reverse second half, interleave |

## Common bugs

- Not checking `fast and fast.next` before accessing `fast.next.next` (NPE)
- Stopping condition wrong for even vs odd length
- Forgetting to reset slow to head in cycle-start variant
- Using `==` to compare values instead of node identity for cycle detection

## Why O(1) space matters

The naive cycle-detection solution stores visited nodes in a hash set — O(n) space. Floyd's gets the same answer with two pointers and constant space, which makes it asymptotically optimal and a favorite interview question.