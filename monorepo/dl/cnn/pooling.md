---
difficulty: easy
last_sent: '2026-07-03T05:30:21.408848+00:00'
review_count: 2
tags:
- cnn
- pooling
- max-pooling
- downsampling
topic: deep-learning
---

# Pooling

![Max vs Average Pooling](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/cnn/images/max-vs-avg-pooling.png)

A downsampling operation that reduces spatial dimensions of feature maps. Reduces computation, adds translational invariance, and extracts dominant features.

## Max-Pooling [with window K×K]

Slides a K×K window across the input, picks the **maximum value** in each window.

**Properties:**
- Selects the strongest activation in each window
- Helps reduce spatial dimension → less computation in later layers
- Provides a degree of **translational invariance** — small shifts in input don't change the output much
- Retains the strongest feature responses

**Example with 2×2 window, stride 2:**

```
Input (4×4):           Output (2×2):
[1  3  2  4]
[5  6  7  8]    →      [6  8]
[3  2  1  0]           [4  3]
[1  4  3  2]
```

## Average-Pooling

A downsampling operation that calculates the **mean value** of all pixels within a K×K window.

**Properties:**
- Smooths out the image by considering all values in the neighborhood
- Less aggressive than max-pooling — preserves more information
- Used in older architectures and at the very end of some networks (Global Average Pooling)

**Same example as above:**

```
Input (4×4):           Output (2×2):
[1  3  2  4]
[5  6  7  8]    →      [3.75  5.25]
[3  2  1  0]           [2.50  1.50]
[1  4  3  2]
```

## Why Max-Pooling over Average-Pooling?

**Max-Pooling retains the strongest feature responses.** When a filter detects an "edge" in a region, what matters is the strongest activation in that region — not the average.

Averaging can dilute strong signals. If one pixel screams "edge here!" and three others say nothing, max-pooling keeps the signal; average pooling halves it.

## Global Average Pooling (GAP)

A special case used at the **end** of modern CNNs:

- Pool over the **entire spatial dimension** of each feature map
- Each feature map collapses to a single number
- 7×7×512 feature map → 1×1×512 vector

**Why this matters:**
- Replaces fully-connected layers in classifier head
- Drastically fewer parameters → less overfitting
- Used in ResNet, GoogLeNet, MobileNet

## Modern view: do we still need pooling?

A growing trend (since ResNet) replaces max-pooling with **strided convolutions** (stride 2). The conv layer itself does the downsampling AND learns weights. This is sometimes more flexible than fixed max/average operations.

But max-pooling is still common in older architectures (VGG, classical CNNs) and remains valid for many tasks.

## Pooling layers have no parameters

Unlike conv layers, pooling has no learnable weights — just a fixed operation. This means pooling adds zero training cost beyond the forward/backward computation.

---