---
topic: deep-learning
difficulty: medium
tags: [segmentation, u-net, encoder-decoder, medical-imaging]
last_sent: null
review_count: 0
---

# U-Net (2015)

![U-Net architecture](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/segmentation/images/u-net-architecture.png)

The dominant architecture for image segmentation. Originally designed for biomedical image segmentation but used everywhere now.

## What is segmentation?

While classification predicts ONE label for the whole image, **segmentation predicts a label for every pixel**. Output is a mask the same size as the input.

- **Semantic segmentation** — each pixel gets a class (sky, person, road)
- **Instance segmentation** — same, but distinguishes individual instances (person 1, person 2)

U-Net handles semantic segmentation natively.

## Architecture: encoder-decoder with skip connections

```
Input image
   │
   ▼
[Encoder]  ← downsamples (conv + pool)
   │ ────skip connection────┐
   │                        │
   │                        ▼
   │                    [Decoder]  ← upsamples
   │                        │
   │ ────skip connection────│
   │                        │
   │                        ▼
   │                       ...
   │
   ▼                  Output mask (same H×W as input)
```

The structure looks like a "U" — encoder going down, decoder going up, with horizontal connections in between.

## How it works

**Encoder (contracting path):**
- Repeated `[3×3 conv → ReLU → 3×3 conv → ReLU → 2×2 max pool]` blocks
- Each block doubles the channels and halves the spatial size
- Captures **WHAT** is in the image (semantic features) but loses **WHERE** (spatial detail)

**Decoder (expansive path):**
- Repeated `[upsample → concatenate skip → 3×3 conv → ReLU → 3×3 conv → ReLU]` blocks
- Each block halves the channels and doubles the spatial size
- Recovers spatial resolution to produce a per-pixel output

**Skip connections:**
- Concatenate encoder feature maps to corresponding decoder layers
- Preserve fine spatial detail that was lost during downsampling

## Why skip connections matter

Without them, the decoder would only see the heavily compressed bottleneck representation — it would know "there's an object" but not exactly where its boundaries are. The skip connections give the decoder direct access to the high-resolution encoder features at each scale.

This is **critical for precise segmentation boundaries**. Medical applications (cell membranes, tumor boundaries) need pixel-accurate masks.

## What gets concatenated

At each decoder level, the upsampled feature map is concatenated with the corresponding encoder feature map at the same resolution:

- Encoder layer 1 (full resolution) → concatenated to decoder's last upsampling
- Encoder layer 2 (½ resolution) → concatenated to decoder's second-to-last upsampling
- ...

The result is that the final output layer sees both the deep semantic features AND the original high-resolution texture details.

## Why it works so well

Three factors:

1. **Multi-scale features** — encoder captures features at multiple scales, decoder uses all of them
2. **Information preservation** — skip connections keep details that pure encoder-decoder would lose
3. **Trainable end-to-end** — the entire network is one differentiable function, optimized jointly

## Output

For binary segmentation: 1-channel output with sigmoid → probability that each pixel belongs to the foreground.

For multi-class: K-channel output with softmax → per-pixel class probabilities.

## Where U-Net is used

- **Medical imaging** — tumor detection, cell segmentation, organ boundaries (its original domain)
- **Satellite imagery** — building detection, land cover classification
- **Autonomous driving** — road segmentation, lane detection
- **Generative models** — diffusion models use U-Net as the denoising backbone

## Training tricks

- **Data augmentation** is critical — segmentation datasets are usually small
- **Weighted loss** for imbalanced classes — small objects get more weight
- **Dice loss** often used alongside cross-entropy — directly optimizes the IoU metric

## Modern variants

- **U-Net++** — nested skip connections for better feature aggregation
- **TransUNet** — transformer-based encoder
- **nnU-Net** — auto-configured U-Net for medical imaging, very strong baseline

## Comparison with SegNet

Both are encoder-decoder architectures. Key differences:

| | U-Net | SegNet |
|---|-------|--------|
| Skip connections carry | **Full feature maps** (concatenated) | **Pooling indices** (where the maxes were) |
| Memory cost | Higher | Lower |
| Reconstruction quality | Better | Slightly worse |
| Used for | Medical, general segmentation | Mobile / memory-constrained settings |

See `seg-net.md` for the SegNet alternative.

---

📝 **Image to add:** The classic U-Net diagram showing the U-shape with encoder, decoder, and horizontal skip connections. Save as `monorepo/dl/segmentation/images/u-net-architecture.png`. Good source: search "U-Net architecture diagram" or grab from the original Ronneberger 2015 paper.
