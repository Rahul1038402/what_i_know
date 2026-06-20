---
difficulty: medium
last_sent: '2026-06-20T05:56:26.525004+00:00'
review_count: 3
tags:
- neural-networks
- backpropagation
- gradient
- chain-rule
- training
topic: deep-learning
---

# Backpropagation

![Backpropagation flow](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/neural-networks/images/backprop-flow.png)

## The core idea

Compute `∂L/∂W` for every weight by applying the **chain rule** backward through the network. This tells us how much each weight contributed to the loss, so we can adjust each one in the right direction.

## The chain rule decomposition

For a single weight in a layer:

```
∂L/∂W = ∂L/∂a · ∂a/∂z · ∂z/∂W
       = ∂L/∂a · f'(z) · x
```

Where:
- `z = Wx + b` (pre-activation)
- `a = f(z)` (post-activation)
- `L = loss(a)` (final loss)

Each term has meaning:
- `∂L/∂a` — how much the loss changes with this neuron's output
- `f'(z)` — slope of the activation function at this point
- `x` — the input that was multiplied by this weight

## The 5-step training loop

1. **Compute output error** — How wrong was the prediction?
2. **Gradient of output weights** — `∂L/∂W` for the final layer
3. **Propagate errors back** — Use chain rule to push gradients backward
4. **Gradient of hidden weights** — Compute `∂L/∂W` for every internal weight
5. **Update all weights** — Apply the gradient: `W_new ← W_old - η · ∂L/∂W`

Where `η` is the learning rate.

## Why this works

The chain rule is the only way to assign blame to deep weights. A weight in layer 1 affects the loss through every layer above it — backprop systematically computes that compounded effect.

The "vanishing gradient problem" is a direct consequence: when each `f'(z)` is small (like sigmoid's max derivative of 0.25), multiplying many of them together makes the gradient near-zero by the time it reaches early layers. This is why ReLU is preferred — its derivative is exactly 1 for positive inputs.

## Computational graphs

Modern frameworks (PyTorch, TensorFlow) build a **computational graph** during forward pass — a DAG of every operation. Backprop walks this graph in reverse, applying the chain rule automatically. You write the forward pass; the framework handles backprop.

## What gets stored

To compute gradients during backprop, each layer caches its inputs and intermediate values from the forward pass. This is why training a model uses much more memory than inference — every activation is held in memory until the backward pass is done.

---