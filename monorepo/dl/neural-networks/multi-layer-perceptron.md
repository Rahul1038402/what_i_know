---
difficulty: easy
last_sent: '2026-07-30T04:36:59.664999+00:00'
review_count: 4
tags:
- neural-networks
- mlp
- architecture
- basics
topic: deep-learning
---

# Multi-Layer Perceptron (MLP)

![MLP architecture](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/neural-networks/images/mlp-architecture.png)

## What is an MLP

A feedforward neural network with at least one hidden layer between input and output. Every neuron in one layer is connected to every neuron in the next (**fully connected**).

```
Input layer → Hidden layer 1 → Hidden layer 2 → Output layer
   x₁ ─┐         p₁ ─┐               q₁ ─┐
   x₂ ─┤         p₂ ─┤               q₂ ─┤───→ ŷ
                p₃ ─┘               q₃ ─┘
```

## Why hidden layers matter

A single-layer network (no hidden layer) can only learn linearly separable patterns — like logistic regression. Each hidden layer composed with non-linear activations lets the network learn more abstract features:

- Layer 1: edges, simple shapes
- Layer 2: combinations of edges (curves, corners)
- Layer 3+: object parts, then whole objects

This compositional structure is why deep networks generalize well.

## The universality theorem

A single hidden layer with enough neurons can approximate any continuous function (Cybenko, 1989). But "enough" can mean exponentially many neurons. **Depth is exponentially more efficient than width** for most real-world functions — which is why "deep" learning beats "wide" learning.

## Forward pass through an MLP

For each layer ℓ:

```
z⁽ℓ⁾ = W⁽ℓ⁾ · a⁽ℓ⁻¹⁾ + b⁽ℓ⁾
a⁽ℓ⁾ = f(z⁽ℓ⁾)
```

The output `a⁽ℓ⁾` becomes the input to layer ℓ+1.

## Activation choice per layer

- **Hidden layers**: ReLU (default) — fast, no vanishing gradient
- **Output layer (regression)**: Linear (no activation)
- **Output layer (binary classification)**: Sigmoid → outputs in (0, 1)
- **Output layer (multi-class)**: Softmax → outputs sum to 1

## Limitations

MLPs work well for tabular data but struggle with:
- **Images** — too many parameters (each pixel is its own input), no spatial awareness → **CNNs solve this**
- **Sequences** — no sense of order or memory → **RNNs/Transformers solve this**

This is the "no free lunch" of architectures. The right structure embeds the right inductive bias for the data type.

---