---
difficulty: medium
last_sent: '2026-06-22T07:00:06.121691+00:00'
review_count: 1
tags:
- activation-functions
- sigmoid
- tanh
- relu
- vanishing-gradient
topic: deep-learning
---

# Sigmoid, Tanh, and ReLU

![Activation functions comparison](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/activation-functions/images/sigmoid-tanh-relu-curves.png)

## 1. Sigmoid

**Formula:** `σ(x) = 1 / (1 + e⁻ˣ)`

**Derivative:** `σ'(x) = σ(x) · (1 - σ(x))`

| Property | Value |
|----------|-------|
| Output range | (0, 1) |
| Differentiable | Yes |
| Max derivative | 0.25 (at x=0) |
| Zero-centered | No |
| Used for | Binary classification output |

### Vanishing gradient problem

When `\|x\|` is large, `σ'(x) → 0`. Gradients passing through many sigmoid layers get multiplied by ~0 repeatedly and vanish before reaching early layers — early-layer weights barely update, training stalls.

**Why ReLU is preferred for hidden layers** — its derivative is exactly 1 for positive inputs, no shrinkage during backprop.

## 2. Tanh (Hyperbolic Tangent)

**Formula:** `tanh(x) = (eˣ - e⁻ˣ) / (eˣ + e⁻ˣ)`

**Relation to sigmoid:** `tanh(x) = 2σ(2x) - 1`

**Derivative:** `tanh'(x) = 1 - tanh²(x)`

| Property | Value |
|----------|-------|
| Output range | (-1, 1) |
| Zero-centered | **Yes** |
| Max derivative | 1 (at x=0) |
| Used for | RNN hidden states |

### Why zero-centered matters

Sigmoid outputs are always positive, so gradients passed backward are all the same sign — the optimizer can only update weights all-up or all-down at each step, causing **zig-zag updates**.

Tanh produces both positive and negative outputs, so gradients can be positive or negative, allowing more efficient diagonal updates. This is why tanh is preferred over sigmoid for hidden layers when sigmoid-like behavior is needed.

## 3. ReLU (Rectified Linear Unit)

**Formula:** `ReLU(x) = max(0, x)`

**Derivative:** `1 if x > 0, else 0`

| Property | Value |
|----------|-------|
| Output range | [0, ∞) |
| Computationally cheap | **Yes** (just a comparison) |
| Vanishing gradient | **No** for positive inputs |
| Used for | Hidden layers in CNNs, MLPs (default) |

### The Dying ReLU problem

For negative inputs, output is 0 AND gradient is 0. If a neuron's pre-activation is consistently negative, it gets stuck — gradient is 0, so weights never update. The neuron is permanently dead.

**Solution: Leaky ReLU** — `f(x) = max(0.01x, x)`. The small slope (0.01) for negative inputs keeps gradients flowing so the neuron can recover.

## Quick comparison

| | Sigmoid | Tanh | ReLU |
|---|---------|------|------|
| Range | (0, 1) | (-1, 1) | [0, ∞) |
| Zero-centered | ✗ | ✓ | ✗ |
| Vanishing gradient | Severe | Moderate | None (x>0) |
| Compute cost | Expensive (exp) | Expensive (exp) | Cheap (max) |
| Default use | Binary output | RNN hidden | Hidden layers |

## Key gradients to remember

| Function | Gradient at x=0 | Issue |
|----------|-----------------|-------|
| Sigmoid | 0.25 | Vanishes for \|x\| > 4 |
| Tanh | 1.0 | Vanishes for \|x\| > 3 |
| ReLU | 1 (if x>0), 0 (if x<0) | Dying ReLU |

---