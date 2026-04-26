# what_i_know — knowledge base

Personal notes organized by topic, designed to be sent as a daily email by the cron job.

## Structure

- `system-design/` — architecture, distributed systems, large-scale patterns
- `dsa/` — data structures and algorithms
- `patterns/` — design patterns
- `ml/` — AI / ML / DL concepts

## Note format

Each `.md` file uses YAML frontmatter:

```yaml
---
topic: system-design
difficulty: medium      # easy | medium | hard
tags: [tag1, tag2]
last_sent: null         # auto-updated by cron
review_count: 0         # auto-updated by cron
---
```

The `last_sent` and `review_count` fields are written back by the daily email workflow — don't edit them manually.
