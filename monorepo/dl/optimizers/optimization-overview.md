---
difficulty: easy
last_sent: '2026-07-19T04:50:58.350369+00:00'
review_count: 3
tags:
- optimization
- gradient-descent
- training
- optimizers
topic: deep-learning
---

# Optimization & Optimizers — overview

## The problem

After the forward pass computes a loss, we need to update the weights to reduce it. This is what an optimizer does.

## The universal update rule

```
W ← W_old - η · ∇L
```

Where:
- `W` — the weight being updated
- `η` — learning rate (step size)
- `∇L` — gradient of the loss with respect to W

**This rule never changes.** All optimizers follow it. They differ only in **how they compute the effective gradient and step size**.

## The five main optimizers

1. **Batch Gradient Descent (BGD)** & **Stochastic Gradient Descent (SGD)** — vanilla approaches
2. **SGD + Momentum** — adds velocity to smooth updates
3. **Adagrad** — per-parameter adaptive learning rates
4. **RMSProp** — fixes Adagrad's vanishing learning rate
5. **Adam** — combines Momentum + RMSProp

This is a chain of fixes. Each optimizer was invented to solve the previous one's problem.

## The lineage

```
SGD              "noisy, oscillates, treats every direction equally"
  ↓ (add velocity)
SGD + Momentum   "smooth but still uses one global learning rate"
  ↓ (per-parameter rates)
Adagrad          "adaptive, but learning rate keeps shrinking forever"
  ↓ (decay old gradients)
RMSProp          "fixed the vanishing rate, but no momentum"
  ↓ (combine both)
Adam             "Momentum + RMSProp = the modern default"
```

## Quick comparison

| Optimizer | Adapts learning rate | Uses momentum | Best for |
|-----------|---------------------|---------------|----------|
| SGD | No | No | Simple problems, well-tuned LR |
| SGD + Momentum | No | Yes | CNNs, image classification |
| Adagrad | Yes | No | Sparse data (NLP, recsys) |
| RMSProp | Yes | No | RNNs |
| Adam | Yes | Yes | Default for almost everything |

## Why the learning rate matters

Too high → loss explodes, training diverges.
Too low → training crawls, gets stuck in local minima.
Just right → smooth convergence to a good minimum.

This is why **learning rate scheduling** matters — start with a higher rate to escape bad regions, then anneal it down for fine-tuning. Common schedules: step decay, cosine annealing, warmup.

## Beyond the basics

- **Adam** is the default for most modern work. Use it when in doubt.
- **SGD + Momentum** with learning rate scheduling often beats Adam on image classification (better final accuracy, slower convergence).
- **AdamW** — Adam with decoupled weight decay. Standard for training transformers.
- **Lion**, **Sophia** — newer optimizers from 2023+. Sometimes better, often within noise.

## Mental model

Optimization is rolling a ball down a loss landscape. SGD is the ball. Momentum lets it accumulate speed and roll past small bumps. Adagrad/RMSProp adjust how big a step the ball takes based on the steepness of each direction. Adam combines both.