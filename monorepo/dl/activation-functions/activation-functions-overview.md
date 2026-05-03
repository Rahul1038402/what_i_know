---
difficulty: easy
last_sent: '2026-05-03T05:01:29.732961+00:00'
review_count: 1
tags:
- activation-functions
- non-linearity
- neural-networks
topic: deep-learning
---

# Activation functions — overview

## Why activation functions exist

Without non-linear activations, **stacking layers collapses into a single linear transformation**:

```
Layer1: y₁ = W₁·x + b₁
Layer2: y₂ = W₂·y₁ + b₂
      = W₂·(W₁·x + b₁) + b₂
      = (W₂W₁)·x + (W₂b₁ + b₂)
      = W'·x + b'    ← still linear!
```

No matter how many layers you stack, you can collapse them to `y = W·x + b`. The whole point of "deep" learning vanishes.

**Non-linearity is what gives neural networks their power** — they let the network learn complex patterns that no linear function could represent.

## The three main types

1. **Sigmoid** — outputs (0, 1), used for binary classification outputs
2. **Tanh** — outputs (-1, 1), zero-centered version of sigmoid
3. **ReLU** — outputs [0, ∞), default for hidden layers

See `sigmoid-tanh-relu.md` for full comparison and properties.

## How to choose

| Use case | Recommended activation |
|----------|------------------------|
| Hidden layers (default) | ReLU |
| Hidden layers (avoiding dying neurons) | Leaky ReLU |
| Binary classification output | Sigmoid |
| Multi-class classification output | Softmax |
| Regression output | None (linear) |
| RNN hidden state | Tanh |

## Modern variants worth knowing

- **Leaky ReLU**: `max(0.01x, x)` — fixes dying ReLU
- **GELU**: Gaussian Error Linear Unit — smoother ReLU, used in transformers (BERT, GPT)
- **Swish / SiLU**: `x · sigmoid(x)` — found by Google's neural architecture search
- **ELU**: Exponential Linear Unit — smooth like tanh, has negative outputs

## The deeper question

Why does non-linearity work so well? Each non-linear activation is essentially a "decision" — turning a smooth weighted sum into something more discrete and meaningful. Stacking these decisions creates hierarchy, which matches how real-world data is structured (pixels → edges → shapes → objects).