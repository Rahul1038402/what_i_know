---
difficulty: medium
last_sent: '2026-05-25T06:02:19.178285+00:00'
review_count: 2
tags:
- autoencoder
- unsupervised
- representation-learning
- dimensionality-reduction
topic: deep-learning
---

# Autoencoders

![Autoencoder structure](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/autoencoders/images/autoencoder-architecture.png)

## Structure

```
Input x → [Encoder] → Latent z → [Decoder] → Reconstructed x̂
```

The encoder compresses input `x` to a **lower-dimensional latent representation** `z`. The decoder reconstructs `x̂` from `z`. The training loss is reconstruction error, typically MSE:

```
L = ||x - x̂||²
```

## Why the latent vector is useful

The autoencoder is trained **unsupervised** — no labels needed. But to minimize reconstruction error, the bottleneck is **forced** to capture the most meaningful and discriminative features of the input while discarding noise and redundancy.

This compressed representation often **transfers well to downstream tasks** like classification, even though the autoencoder never saw any labels.

### Common misconceptions

The latent vector is NOT useful because:
- ❌ It's smaller — random downsampling would also be smaller but useless
- ❌ Reconstruction is "lossless" — it's not, information IS lost; the autoencoder learns to keep what matters

The latent vector IS useful because:
- ✅ Reconstruction loss forces the encoder to keep features that **predict the input back**
- ✅ Features that predict the input back are usually the same features that matter for downstream tasks

## Applications

**Denoising autoencoders** — Train with noisy input and clean target. The network learns to remove noise. Used in image cleanup, audio enhancement.

**Anomaly detection** — Train on normal data only. At test time, anomalous inputs will have high reconstruction error (the network never learned to reconstruct them). Used in fraud detection, manufacturing defects, network intrusion.

**Dimensionality reduction** — The latent space acts like a **nonlinear PCA**. Similar inputs map to nearby points in latent space. Useful for visualization (project to 2D/3D), clustering, search.

**Image-to-image translation** — Encoder maps from one domain (e.g., daytime photos), decoder produces another domain (e.g., nighttime photos). Used in style transfer, colorization.

## Convolutional autoencoders

Replace fully-connected layers with convolutional layers in the encoder, and **transposed convolutions** (or upsampling + conv) in the decoder. This:

- Preserves spatial structure
- Is far more parameter-efficient for image data
- Produces better reconstructions than FC autoencoders for images

Standard for any image-related autoencoder application.

## Architecture choice

```
Input image (28×28×1)
   │
[Conv 3×3, 16 filters, stride 2]   →  14×14×16
[Conv 3×3, 32 filters, stride 2]   →  7×7×32
   │
[Bottleneck — flatten + FC to z]   →  z (e.g., 32 dim)
   │
[FC + reshape]                     →  7×7×32
[Transposed conv 3×3, stride 2]    →  14×14×16
[Transposed conv 3×3, stride 2]    →  28×28×1
   │
Reconstructed image
```

The encoder progressively shrinks spatial dimensions while increasing channel depth; the decoder reverses this.

## Key limitation: unstructured latent space

> The latent space is **unstructured**. There's no constraint on how points are distributed in latent space. Two nearby points in z-space might decode to completely different outputs.

This means:

- ❌ You **can't meaningfully sample** from the latent space to generate new data
- ❌ Random points in z-space probably decode to garbage
- ❌ Linear interpolation in z-space doesn't produce smooth transitions

This is exactly what **VAEs (Variational Autoencoders) fix**. By constraining the latent space to follow a known distribution (Gaussian), VAEs make sampling and interpolation meaningful.

See `variational-autoencoders.md` for the next step.

## When to use a vanilla autoencoder

- **Anomaly detection** — you only need reconstruction error, latent structure doesn't matter
- **Denoising** — input/output is well-defined, no need for sampling
- **Pre-training** — get useful features for downstream supervised tasks
- **Dimensionality reduction** — when nonlinear PCA is enough

## When you need something else

- **Generation** — use VAE or GAN, not vanilla AE
- **Smooth latent space** — use VAE
- **Disentangled representations** — use β-VAE, FactorVAE
- **State-of-the-art quality** — use diffusion models or modern GANs

---