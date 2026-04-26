---
topic: deep-learning
difficulty: medium
tags: [optimization, sgd, batch-gradient-descent, mini-batch]
last_sent: null
review_count: 0
---

# Batch GD vs Stochastic GD

The two extremes of how to compute the gradient. Modern training uses **mini-batch GD** as a middle ground.

## Batch Gradient Descent (BGD)

**Formula:**

```
∇L = (1/N) · Σᵢ ∇Lᵢ(w)
```

- Uses the **entire dataset** to compute one gradient
- `∇L` is averaged over all N samples
- One weight update per pass through the dataset (one epoch = one update)

**Properties:**
- ✅ Stable, smooth convergence — gradient direction is the true average
- ✅ Deterministic — same result every run
- ❌ Extremely slow — wait for all N samples before any update
- ❌ Memory-heavy — must hold entire dataset in memory
- ❌ Bad for huge datasets (impossible for ImageNet, etc.)

## Stochastic Gradient Descent (SGD)

**Formula:**

```
∇L = ∇Lᵢ(w)
```

- Uses **one sample at a time** (or a small mini-batch)
- `∇L` computed over a single selected sample
- N weight updates per epoch (one update per sample)

**Properties:**
- ✅ Fast — updates after every sample
- ✅ Scales well to huge datasets
- ✅ Noise can help escape local minima (paradoxically useful)
- ❌ Noisy gradients — trajectory oscillates
- ❌ Doesn't converge to exact minimum, oscillates around it

## Side-by-side

| | BGD | SGD |
|---|-----|-----|
| Samples per update | All N | 1 |
| Updates per epoch | 1 | N |
| Convergence | Smooth | Noisy, oscillates |
| Speed | Slow | Fast |
| Memory | High (whole dataset) | Low (one sample) |
| Final position | Exact minimum | Near minimum |
| Escapes local minima | Poorly | Well |

## Mini-batch GD — the practical compromise

In practice, neither extreme is used. **Mini-batch SGD** is what every modern framework defaults to:

```
∇L = (1/B) · Σᵢ₌₁ᴮ ∇Lᵢ(w)    where B is the batch size (e.g., 32, 64, 128)
```

- Uses a small batch of B samples (usually 32-256)
- Less noise than pure SGD
- Faster than BGD
- Vectorizes well on GPU (each batch is one matrix multiply)

When people say "SGD" today, they almost always mean mini-batch SGD.

## The problem with vanilla SGD

Even with mini-batches, SGD has a fundamental issue:

> **It treats every direction equally and uses the same learning rate η for all parameters.**

In practice, different parameters need different effective learning rates:
- A parameter near a sharp minimum needs small steps
- A parameter on a flat plateau needs large steps
- A frequently-updated parameter (common feature) needs small steps
- A rarely-updated parameter (rare feature) needs large steps

SGD can't do any of this. **This is why Momentum, Adagrad, RMSProp, and Adam exist** — each one adds adaptive behavior on top of vanilla SGD.

See `momentum-adagrad-rmsprop-adam.md` for the fixes.

## Choosing batch size

| Batch size | Trade-off |
|------------|-----------|
| Very small (1-8) | Noisy, slow per-epoch but maybe better generalization |
| Medium (32-128) | Sweet spot — most papers use this range |
| Large (512+) | Smooth, fast per-step, but may generalize worse and need LR scaling |

The "linear scaling rule" — when you increase batch size by k, scale the learning rate by k too. Helps with very large batches.
