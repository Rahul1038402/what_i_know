---
topic: deep-learning
difficulty: hard
tags: [optimization, momentum, adagrad, rmsprop, adam, optimizers]
last_sent: null
review_count: 0
---

# Momentum, Adagrad, RMSProp, Adam

![Optimizer trajectories](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/optimizers/images/optimizer-trajectories.png)

Each optimizer fixes a problem with the previous one. Read in order — the math compounds.

## 1. SGD + Momentum

**Idea:** Add a velocity term that accumulates past gradients to smooth updates.

**Update equations:**

```
vᵢ = γ · vᵢ₋₁ + η · ∇L(wᵢ)         ← velocity term
W_{i+1} = Wᵢ - vᵢ
```

Where:
- `γ` — momentum coefficient (typically 0.9)
- `η` — learning rate
- `v₀ = 0` (start with no velocity)

**Properties:**
- ✅ Faster convergence (builds speed in consistent directions)
- ✅ Damps oscillations (cancels out conflicting gradients)
- ❌ γ is one extra hyperparameter to tune

**Exponential decay intuition:** At γ=0.9, if the current gradient has weight 1:
- 1 step back → weight 0.9
- 2 steps back → weight 0.81
- 3 steps back → weight 0.729
- ...

This is **exponentially decaying memory** of past gradients — recent ones dominate, distant ones fade.

## 2. Adagrad

**Idea:** Adaptive learning rate. η varies for each parameter based on its past gradient magnitudes.

**Update equations:**

```
G_t = Σᵢ₌₁ᵗ (∇L(w_τ))²              ← sum of past squared gradients
W_{i+1} = Wᵢ - (η / √(G_t + ε)) · ∇L(Wₜ)
```

Where:
- `η` — global learning rate
- `ε` ≈ 1e-8 (avoids division by 0)
- `G_t` — accumulated squared gradients (per parameter)

**Behavior:**
- Parameter updated **frequently** → large G_t → **small effective learning rate**
- Parameter updated **rarely** → small G_t → **large effective learning rate**

This solves the "same η for all parameters" problem of SGD. Sparse features (rarely updated) get larger steps; common features get smaller steps.

**Problem with Adagrad:** It accumulates squared gradients **forever**. After many steps, G_t grows huge, and effective learning rate `η / √G_t` shrinks toward zero. Training stalls. This is why **RMSProp fixes this**.

## 3. RMSProp

**Idea:** Use an exponentially decaying average of squared gradients instead of summing forever.

**Update equations:**

```
E[g²]_t = β · E[g²]_{t-1} + (1-β) · (∇L)²
W_{i+1} = Wᵢ - (η / √(E[g²]_t + ε)) · ∇L(Wₜ)
```

Where `β` is typically 0.9 (so ~10 most recent gradients matter).

**Key change from Adagrad:** Old gradients are forgotten gradually. The denominator stays bounded, so the effective learning rate doesn't vanish.

**Properties:**
- ✅ Adaptive per-parameter (like Adagrad)
- ✅ Doesn't suffer from vanishing learning rate
- ❌ No momentum — still oscillates

## 4. Adam (Adaptive Moment Estimation)

**Idea:** Combine Momentum (1st moment of gradients) with RMSProp (2nd moment of gradients).

**Update equations:**

```
mₜ = β₁ · mₜ₋₁ + (1-β₁) · ∇L           ← 1st moment (momentum)
vₜ = β₂ · vₜ₋₁ + (1-β₂) · (∇L)²        ← 2nd moment (RMSProp)

m̂ₜ = mₜ / (1 - β₁ᵗ)                    ← bias correction
v̂ₜ = vₜ / (1 - β₂ᵗ)                    ← bias correction

W_{i+1} = Wᵢ - η · m̂ₜ / (√v̂ₜ + ε)
```

Default values: `β₁ = 0.9, β₂ = 0.999, η = 0.001, ε = 1e-8`

**Why bias correction:** Both `m` and `v` start at 0, so they're biased toward zero in early iterations. The `(1 - βᵗ)` correction compensates for this — important during the first few hundred steps.

## Comparison

| Optimizer | Adapts LR | Momentum | Vanishing LR | Default in modern code |
|-----------|-----------|----------|--------------|------------------------|
| SGD + Momentum | No | Yes | No | Image classification (ResNet etc.) |
| Adagrad | Yes | No | **Yes** ❌ | Sparse features (NLP, recsys) |
| RMSProp | Yes | No | No | RNNs |
| Adam | Yes | Yes | No | **Almost everything else** |

## When to use what

- **Adam** — default for transformers, most modern work. Just works.
- **SGD + Momentum** with learning rate schedule — image classification, often beats Adam on final accuracy.
- **AdamW** — Adam with decoupled weight decay, standard for training transformers (GPT, BERT etc.).

## Why Adam isn't always best

Adam's adaptive learning rates can converge to sharper minima that don't generalize as well. SGD finds flatter minima (rolls there slowly), which often generalize better. This is why CV practitioners often prefer SGD + Momentum despite Adam's faster convergence.

---
