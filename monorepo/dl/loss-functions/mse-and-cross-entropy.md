---
difficulty: medium
last_sent: '2026-07-15T04:29:30.109252+00:00'
review_count: 5
tags:
- loss-functions
- mse
- cross-entropy
- regression
- classification
topic: deep-learning
---

# MSE and Cross-Entropy

The three classical losses that cover most supervised learning tasks.

## 1. Mean Squared Error (MSE)

**Used for:** Regression, autoencoders, reconstruction loss.

**Formula:**

```
MSE = (1/N) · Σᵢ (yᵢ - ŷᵢ)²
```

Where:
- `y` — true value
- `ŷ` — predicted value
- `N` — number of samples

**Properties:**
- Penalizes large errors heavily (squared term)
- Sensitive to outliers — one way-off data point dominates the loss
- Smooth, differentiable everywhere
- Output is in squared units — interpretable as variance

**When NOT to use:** When outliers are present and you don't want them to dominate. Use MAE (Mean Absolute Error) instead — it's more robust.

## 2. Binary Cross-Entropy (BCE)

**Used for:** Binary classification, GAN discriminator, multi-label classification.

**Formula:**

```
L = -[y · log(p) + (1-y) · log(1-p)]
```

Where:
- `y` — true probability (0 or 1)
- `p` — predicted probability (output of sigmoid)

**Output activation:** Sigmoid (forces output to (0,1) so log doesn't blow up)

**How it works:**
- If true label is 1: loss = `-log(p)` → 0 when p=1, ∞ when p=0
- If true label is 0: loss = `-log(1-p)` → 0 when p=0, ∞ when p=1

The log creates a strong penalty for confidently wrong answers — predicting 0.99 when the truth is 0 is much worse than predicting 0.6.

## 3. Categorical Cross-Entropy (CCE)

**Used for:** Multi-class classification (one true class out of K).

**Formula:**

```
L = -Σₖ yₖ · log(pₖ)
```

Simplified for one-hot true labels (only one class is 1, rest are 0):

```
L = -log(p_correct_class)
```

Where:
- `yₖ` — true probability for class k (one-hot encoded)
- `pₖ` — predicted probability for class k

**Output activation:** Softmax (forces outputs to sum to 1 across all classes)

**Intuition:** The loss is just the negative log of the probability assigned to the correct class. Predict 0.9 for the right class → low loss. Predict 0.1 for the right class → high loss.

## MSE vs Cross-Entropy for classification

Why not just use MSE for classification?

| | MSE | Cross-Entropy |
|---|-----|---------------|
| Gradient when wrong but confident | Small (saturated sigmoid) | Large |
| Convex w/ logistic regression | No | Yes |
| Punishes confident wrong predictions | Mildly | Heavily |

The math: for sigmoid + MSE, the gradient contains a `σ'(z)` term that shrinks to zero when the network is confidently wrong (sigmoid is flat at extremes). This means **wrong, confident predictions don't get strong correction signals**. Cross-entropy's gradient cancels out this term, giving cleaner learning signals.

**Bottom line:** Always use cross-entropy for classification, MSE for regression.

## Numerical stability

In practice, frameworks combine softmax + cross-entropy into a single op (`F.cross_entropy` in PyTorch, `tf.nn.sparse_softmax_cross_entropy_with_logits` in TF). This avoids computing log(softmax) directly, which can produce NaN for very small probabilities.