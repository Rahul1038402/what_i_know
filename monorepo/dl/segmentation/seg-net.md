---
difficulty: medium
last_sent: '2026-07-16T04:40:56.619823+00:00'
review_count: 2
tags:
- segmentation
- segnet
- encoder-decoder
- pooling-indices
topic: deep-learning
---

# SegNet (2015)

![SegNet architecture](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/segmentation/images/segnet-architecture.png)

A memory-efficient alternative to U-Net for image segmentation. Same encoder-decoder structure, but uses **pooling indices** instead of full skip connections.

## Architecture overview

Similar encoder-decoder structure to U-Net:

```
Input
   │
   ▼
[Encoder]  ← VGG-16-like, conv + max pool
   │ (stores pooling indices)
   ▼
[Decoder]  ← uses indices for unpooling
   │
   ▼
Output mask
```

Encoder is essentially VGG-16 without the fully-connected layers. Decoder mirrors it.

## The key idea: pooling indices

When max pooling happens in the encoder, SegNet **records WHERE the max value came from** in each pooling window:

```
Input window:        After max pool:    Indices stored:
[1  3]                                   [_  ✓]
[5  6]      →           [6]              [_  _]
                                          (top-right was the max)
```

These indices are saved (just integers, very small memory) and used during the decoder's **unpooling** step.

## Unpooling with stored indices

In the decoder, when we need to upsample:

1. Take the small feature map
2. Place each value at the index location stored from encoder pooling
3. Fill the rest with zeros

```
Decoder feature:          Indices from encoder:    Unpooled:
                          [_ ✓]                    [0 7]
[7]                       [_ _]                    [0 0]
```

This produces a sparse upsampled feature map. Subsequent conv layers fill in the gaps.

## Why this is memory-efficient

**U-Net** concatenates the encoder's full feature maps (e.g., 64×128×128 floats) into the decoder. Lots of memory.

**SegNet** only stores **integer indices** (one per pooling window). Order-of-magnitude less memory.

For a 256×256 image with 5 pooling levels, U-Net might store gigabytes of feature maps; SegNet stores megabytes of indices.

## Trade-off

The indices contain less information than full feature maps. SegNet only tells you "the max came from this corner of this window" — not "here are all the activations." Reconstructions are less precise.

This usually produces:
- **Slightly worse** segmentation quality than U-Net
- **Significantly less** memory usage
- **Faster** inference

## When to use SegNet vs U-Net

| Choose SegNet when | Choose U-Net when |
|--------------------|-------------------|
| Mobile / embedded deployment | Server-side / GPU-rich |
| Real-time inference needed | Quality is the priority |
| Large input images (memory-constrained) | Smaller images, can afford memory |
| Outdoor scene segmentation (broader context) | Medical imaging (precise boundaries) |

## Original paper context

SegNet was proposed by Cambridge researchers in 2015 (same year as U-Net). They specifically targeted **road scene understanding** for autonomous driving — broad segmentation classes (road, building, sky, car) where pixel-perfect boundaries matter less than overall efficiency.

## Modern relevance

Both U-Net and SegNet have been largely superseded for state-of-the-art segmentation by:
- **DeepLab** family (atrous convolutions)
- **Mask R-CNN** (instance segmentation)
- **Vision Transformers** (Swin, DETR variants)
- **SAM** (Segment Anything Model, 2023)

But SegNet's pooling-indices trick still appears in efficient architectures for edge devices.

## Key takeaway

> **U-Net = full feature map concatenation** (memory-heavy, accurate)
> **SegNet = pooling indices only** (memory-light, less precise)

Same shape, very different information transfer between encoder and decoder.

---