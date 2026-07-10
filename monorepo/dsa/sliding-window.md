---
difficulty: medium
last_sent: '2026-07-10T05:40:45.367505+00:00'
review_count: 4
tags:
- pattern
- two-pointers
- arrays
- strings
topic: dsa
---

# Sliding window

A pattern for problems on **contiguous subarrays or substrings**. Maintain a window between two pointers (`left`, `right`) and slide it through the array, expanding or contracting based on a condition. Reduces O(n²) brute-force solutions to **O(n)**.

## When to reach for it

Look for these signals in the problem:

- "Contiguous subarray/substring of size K"
- "Longest/shortest substring with property X"
- "Subarray sum / count / max / min within constraints"
- "All anagrams" / "permutation in string"

If the brute force is "try all subarrays in O(n²)", sliding window often collapses it to O(n).

## Two flavors

### 1. Fixed-size window

Window size is given. Slide it through the array, maintaining the metric incrementally.

```python
def max_sum_subarray_k(nums, k):
    window_sum = sum(nums[:k])
    best = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]  # add new, remove old
        best = max(best, window_sum)
    return best
```

### 2. Variable-size window

Expand `right` to include new elements. When the window violates the constraint, shrink from `left` until valid again.

```python
def longest_unique_substring(s):
    seen = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1  # shrink past duplicate
        seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

## Mental model

- `right` always moves forward — this is what makes it O(n)
- `left` only catches up when the window becomes invalid
- Each element is visited at most twice (once by `right`, once by `left`)

## Classic problems

| Problem | Type | Trick |
|---------|------|-------|
| Max sum subarray of size K | Fixed | Subtract leaving, add entering |
| Longest substring without repeat | Variable | Map char → last index |
| Min window substring | Variable | Char-count map + match counter |
| Longest substring with K distinct chars | Variable | Shrink when distinct > K |
| Permutation in string | Fixed | Compare frequency maps |
| Smallest subarray with sum ≥ target | Variable | Shrink while sum still ≥ target |
| Fruit into baskets | Variable | Same as K=2 distinct |

## Common bugs

- Forgetting to shrink the window in the variable case (loops as O(n²) silently)
- Off-by-one errors in window-size calculation: `right - left + 1`
- Using the wrong condition for shrinking (`while` vs `if`)
- Updating the answer at the wrong moment (before vs after shrinking)

## Time/space

- Time: **O(n)** — each pointer moves at most n times
- Space: **O(k)** — usually a hash map of window contents