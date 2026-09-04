---
difficulty: hard
last_sent: '2026-09-04T06:24:16.837449+00:00'
review_count: 6
tags:
- cnn
- inception
- googlenet
- architecture
- 1x1-conv
topic: deep-learning
---

# Inception (GoogLeNet, 2014)

![Inception module](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/cnn/images/inception-module.png)

## The core problem it solves

At any layer, **you don't know what filter size is best**. Small filters capture fine textures; large filters capture broader patterns. Pick wrong, and the network can't represent what it needs.

Stacking different filter sizes sequentially makes the network too deep. **Why not just use them in parallel?**

## The Inception module

Run multiple filter sizes **in parallel within the same layer**, then concatenate all outputs along the channel dimension:

- 1×1 conv branch
- 3×3 conv branch
- 5×5 conv branch
- 3×3 max pooling branch (followed by 1×1 conv)

Each branch sees the same input but extracts features at a different scale. The network learns which scale matters at each layer.

Output of the module = concatenation of all four branches' outputs along the channel axis.

## The 1×1 convolution bottleneck

This is the most important detail. Without it, Inception would be computationally infeasible.

**The problem:** A 5×5 conv on a 256-channel input is expensive:
```
5 × 5 × 256 × 128 = 819,200 parameters per filter set
```

**The solution:** A 1×1 conv first **reduces the channel dimension** (e.g., 256 → 64), then the 5×5 conv operates on 64 channels:

```
1×1 reducing 256 → 64:        256 × 64    = 16,384 params
5×5 on 64 channels with 128 filters: 5 × 5 × 64 × 128 = 204,800 params
                                                Total = 221,184 params
```

**Result: ~4× reduction.**

## Why 1×1 conv works as a "bottleneck"

A 1×1 conv with K filters is essentially a **per-pixel fully-connected layer** that mixes channels:

- Spatial dimension stays the same (1×1 kernel doesn't move pixels)
- Channel dimension is whatever you choose (K filters → K output channels)
- Cheap because the spatial size is 1

Used everywhere in modern architectures — ResNet bottleneck blocks, MobileNet, etc.

## Why parallel paths help

Different filters specialize:
- **1×1 path** — captures cross-channel correlations only
- **3×3 path** — captures local patterns
- **5×5 path** — captures larger patterns
- **Pooling path** — captures translation-invariant features

Concatenating gives the next layer access to **all of these representations simultaneously**. The network picks what's useful.

## GoogLeNet specifics

- 22 layers deep (much deeper than previous winners)
- 9 Inception modules stacked
- **No fully-connected layers** at the end → uses Global Average Pooling
- **5M parameters** total — fewer than AlexNet's 60M, with much better accuracy
- Won ImageNet 2014

## Inception variants (worth knowing)

- **Inception v1** (GoogLeNet, 2014) — original
- **Inception v2 / v3** — added batch normalization, factorized convolutions (5×5 → two 3×3)
- **Inception v4** — combined with residual connections
- **Xception** — extreme version using depthwise separable convolutions

## Key takeaway

Inception's contribution was the idea that **multiple receptive fields in parallel** beat a single fixed choice, and that **1×1 convs solve the parameter blowup**. Both ideas became standard in modern architectures.

---