---
difficulty: easy
last_sent: '2026-08-18T02:38:20.292076+00:00'
review_count: 4
tags:
- neural-networks
- neuron
- forward-propagation
- basics
topic: deep-learning
---

# Single neuron and forward propagation

![Single neuron architecture](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/neural-networks/images/single-neuron.png)

## Single neuron — the building block

A neuron applies an activation function to a weighted sum of inputs to produce an output.

**Computation:**

```
z = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
a = f(z)
```

Where:
- `xᵢ` — input values
- `wᵢ` — weights (learned parameters)
- `b` — bias (helps the neuron fire even when all inputs are 0)
- `f` — activation function (introduces non-linearity)
- `a` — neuron's output (passed to next layer)

## Why bias matters

Without bias, the decision boundary is forced to pass through the origin. Bias shifts the activation independently of inputs, letting the neuron fire even when all inputs are zero. It's a learnable threshold.

## Forward propagation

The process of moving data through the network from input to output:

```
Input layer → Hidden layer 1 → Hidden layer 2 → ... → Output layer
```

**At each layer:**
1. Compute `z = Wx + b` for every neuron (matrix form: vectorized across the layer)
2. Apply activation function: `a = f(z)`
3. Pass `a` to the next layer as its input

## Vectorized form

For a layer with multiple neurons, the computation becomes a matrix operation:

```
Z = W·X + b
A = f(Z)
```

Where `W` is a weight matrix, `X` is the input vector, `b` is the bias vector. This is what GPUs accelerate — the dot product across thousands of neurons in parallel.

## Why this matters

Forward propagation is just inference — it's how a trained network makes predictions. The cleverness comes during training, where backpropagation tells us how to adjust `W` and `b` to reduce loss.

---