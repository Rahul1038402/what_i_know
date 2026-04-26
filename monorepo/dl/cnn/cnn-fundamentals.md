---
topic: deep-learning
difficulty: medium
tags: [cnn, convolution, kernel, stride, padding, computer-vision]
last_sent: null
review_count: 0
---

# CNN Fundamentals

![Convolution operation](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/cnn/images/convolution-operation.png)

## Why CNNs exist

Fully-connected networks fail on images because:
- A 224×224 RGB image has 150,528 inputs → millions of weights even for one hidden layer
- Same object in two different positions looks "completely different" to the network
- Spatial structure (which pixels are neighbors) is lost when flattened

CNNs fix all three problems with three core ideas:

1. **Local receptive fields** — Each neuron sees only a small patch at a time
2. **Weight sharing** — The same filter slides over the entire image
3. **Translational invariance** — The model's response is the same regardless of object location in the input

## The convolution operation

A **filter (kernel)** of size F×F slides across the input with a certain **stride S**. At each position, it computes a dot product between the filter and the patch of input it's covering, plus a bias term:

```
output[i,j] = Σ Σ (filter[a,b] · input[i+a, j+b]) + bias
```

This produces **one value** in the output feature map. Sliding produces the full feature map.

## Output size formula

```
O = (I - F + 2P) / S + 1
```

Where:
- `I` — Input size (height or width)
- `F` — Filter size
- `P` — Padding (zeros added to borders)
- `S` — Stride (how many pixels to move per step)

**Example:** 28×28 input, 5×5 filter, no padding, stride 1:
```
O = (28 - 5 + 0) / 1 + 1 = 24
```
Output is 24×24.

## Padding

- **Valid padding** (P=0) — Output is smaller than input
- **Same padding** (P chosen so O=I) — Output is same size as input
- **Why padding matters** — Without it, edge pixels participate in fewer convolutions, are under-represented in the output

## Stride

- Stride 1 → dense output, same resolution as input (with same padding)
- Stride 2 → output is half-resolution (downsampling), reduces computation
- Stride > kernel size → some input pixels skipped entirely (rarely useful)

## Channels

Real images have multiple channels (RGB = 3). The filter has the **same number of channels as input**:

- Input: H × W × **C_in**
- Filter: F × F × **C_in** (one filter learns across all input channels)
- A layer has K filters → output: H × W × **K** (K = C_out)

So a 3×3 conv layer mapping 64 channels → 128 channels has `3 × 3 × 64 × 128 = 73,728` parameters. Far fewer than the equivalent fully-connected layer.

## What filters learn

Through training, filters become specialized:

- Layer 1: edge detectors (horizontal, vertical, diagonal), color blobs
- Layer 2: corners, simple textures, curves
- Layer 3: object parts (eye, wheel, leaf)
- Deep layers: full objects (face, car, dog)

This hierarchy emerges automatically from the data — nobody hand-codes "make this filter detect eyes."

## Receptive field

A neuron in deep layers "sees" a much larger area of the input than its filter size suggests. Two stacked 3×3 convs see a 5×5 region. Three stacked see 7×7. This is why **stacking small filters is preferred over single large filters** — same receptive field, fewer parameters, more non-linearities.

This insight from VGG (2014) is still standard practice today.

---

📝 **Image to add:** Diagram showing a 3×3 kernel sliding over an input matrix and producing an output feature map. Save as `monorepo/dl/cnn/images/convolution-operation.png`. Good source: search "convolutional operation diagram".
