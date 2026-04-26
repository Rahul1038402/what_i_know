---
topic: deep-learning
difficulty: easy
tags: [loss-functions, training, optimization]
last_sent: null
review_count: 0
---

# Loss functions — overview

A **loss function** is a mathematical method that tells the difference between a model's predicted output and the actual output. Training a network = minimizing this loss.

## Why we need them

The loss function turns "how wrong is the model?" into a single number that gradient descent can optimize. Without a well-chosen loss, the network has no direction to learn.

The choice of loss function depends on the **task type** — using the wrong loss gives gradients that point the wrong way.

## The five main types

1. **Mean Squared Error (MSE)** — regression tasks
2. **Binary Cross-Entropy** — binary classification, GAN discriminators
3. **Categorical Cross-Entropy** — multi-class classification
4. **VAE Loss (ELBO)** — variational autoencoders
5. **GAN Loss** — generative adversarial networks

See `mse-and-cross-entropy.md` for the three classical ones, `vae-loss.md` for VAE specifics.

## How to choose

| Task | Recommended loss |
|------|------------------|
| Predicting continuous value (price, temperature) | MSE / MAE |
| Yes/no classification (spam, fraud) | Binary Cross-Entropy |
| Multi-class classification (digit recognition) | Categorical Cross-Entropy |
| Image reconstruction | MSE / Binary CE |
| Generative model (VAE) | ELBO |
| Generative model (GAN) | GAN loss (min-max) |

## Properties a loss should have

- **Differentiable** — so we can compute gradients
- **Aligned with task** — minimizing loss should produce the behavior we actually want
- **Numerically stable** — no exploding values or NaN gradients
- **Convex when possible** — guarantees a global minimum (rarely achievable for deep nets, but locally convex losses help)

## Loss vs metric

These are different concepts that beginners often confuse:

- **Loss** — what the network optimizes during training (must be differentiable)
- **Metric** — what humans care about (accuracy, F1, IoU); used for evaluation, not training

Example: For classification you train with **cross-entropy loss** but evaluate with **accuracy**. Accuracy isn't differentiable, so it can't be used for backprop, but it's what stakeholders actually want to see.

## Common pitfall

Choosing a loss that minimizes well but doesn't match the real-world goal. Example: MSE on classification produces gradients that don't push hard enough on confident wrong answers — cross-entropy heavily penalizes confidently wrong predictions, which is what classification actually needs.