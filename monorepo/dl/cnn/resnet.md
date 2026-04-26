---
topic: deep-learning
difficulty: hard
tags: [cnn, resnet, residual, skip-connections, architecture]
last_sent: null
review_count: 0
---

# ResNet (2015)

![Residual block](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/cnn/images/residual-block.png)

## The degradation problem

When networks get very deep (>30 layers), accuracy actually **decreases** even on the training set. This is **NOT overfitting** (overfitting would show low training error, high test error).

It's a **degradation / optimization problem** — deeper networks are harder to optimize. The gradients vanish, the loss landscape gets weird, and stochastic gradient descent struggles.

This was a huge problem in 2014. Going from 16 layers (VGG) to 30+ layers made things worse, not better.

## The solution: Residual connections (skip connections)

Instead of learning the desired mapping `H(x)` directly, the block learns the **residual**:

```
F(x) = H(x) - x
```

The output of the block is then:

```
output = F(x) + x
```

The skip connection adds the input `x` directly to the block output, bypassing the weight layers.

## Why this works

Two reasons:

**1. Identity is easy to learn.** If the optimal mapping is close to identity (no change needed at this layer), the block just needs to learn `F(x) ≈ 0`, which is much easier than learning an identity mapping from scratch through several conv layers.

**2. Better gradient flow.** During backprop, gradients can flow **directly through the skip connection**, bypassing the weight layers. This solves the vanishing gradient problem in deep networks — even at layer 100, the gradient still has a clean path back to early layers.

## The residual block

```
       x ────────────────────┐
       │                     │
    [conv 3×3]               │
    [BatchNorm]              │ skip connection
    [ReLU]                   │
    [conv 3×3]               │
    [BatchNorm]              │
       │                     │
       ▼                     │
       (+) ◄─────────────────┘
       │
    [ReLU]
       │
       ▼
     output
```

The skip connection adds `x` element-wise to the conv output, then ReLU is applied.

## Bottleneck blocks (for ResNet-50+)

For deeper variants, a **bottleneck block** is used to keep computation manageable:

```
1×1 conv (reduce channels, e.g., 256 → 64)
3×3 conv (operate on reduced channels)
1×1 conv (restore channels, 64 → 256)
+ skip connection
```

Same idea as Inception's 1×1 bottleneck — reduce channels, do expensive op, restore. This keeps very deep ResNets computationally feasible.

## ResNet variants

| Variant | Layers | Block type |
|---------|--------|-----------|
| ResNet-18 | 18 | Basic (two 3×3 convs) |
| ResNet-34 | 34 | Basic |
| ResNet-50 | 50 | Bottleneck |
| ResNet-101 | 101 | Bottleneck |
| ResNet-152 | 152 | Bottleneck |

ResNet-50 became the de facto standard for image classification benchmarks for years.

## Impact

ResNet won ImageNet 2015 with **3.57% error** — beating human performance. More importantly, it proved **networks can scale to 100+ layers and keep improving**. Skip connections became a fundamental building block:

- DenseNet — concatenate skips instead of add
- Transformers — residual connections in every block
- U-Net — skip connections from encoder to decoder
- Diffusion models — residual blocks throughout

Almost every modern architecture uses some form of residual connection.

## Key insight

ResNet's contribution wasn't just "deeper network." It was the realization that **identity mappings are surprisingly hard to learn**, and the fix is to make them the default by adding the skip connection.

When you stack many residual blocks, the network can choose layer-by-layer whether to "do something" (`F(x)` learns useful changes) or "stay still" (`F(x)` learns to output 0). This adaptive depth is what makes very deep networks trainable.

---

📝 **Image to add:** Diagram of a residual block showing input x, two weight layers, skip connection going around them, addition, then ReLU. Save as `monorepo/dl/cnn/images/residual-block.png`. Good source: search "ResNet residual block diagram".
