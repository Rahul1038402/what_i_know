---
difficulty: hard
last_sent: '2026-08-28T13:17:05.360681+00:00'
review_count: 3
tags:
- autoencoder
- vae
- generative
- reparameterization
- latent-space
topic: deep-learning
---

# Variational Autoencoders (VAE)

![VAE architecture](https://raw.githubusercontent.com/Rahul1038402/what_i_know/main/monorepo/dl/autoencoders/images/vae-architecture.png)

A generative model that fixes the unstructured latent space problem of vanilla autoencoders. Once trained, you can **sample** new data by drawing random points from the latent space.

## What VAE fixes

Vanilla autoencoders learn a latent space, but it's **unstructured** — you can't sample from it meaningfully. Random points in z-space decode to garbage.

VAEs solve this by **constraining the latent space to follow a known distribution** (standard normal). After training, sampling random points from `N(0, I)` and decoding them produces valid, realistic outputs.

## Architecture: the key change

Instead of the encoder outputting a single point `z`, it outputs **two vectors**: a mean `μ` and a standard deviation `σ`. These define a Gaussian distribution over the latent space:

```
Input x
   │
   ▼
[Encoder]
   │
   ├──▶ μ (mean vector)
   └──▶ σ (std deviation vector)
       │
   Sample z ~ N(μ, σ²)   ← latent code drawn from this distribution
       │
   ▼
[Decoder]
   │
   ▼
Reconstructed x̂
```

So the encoder outputs a **distribution**, not a point. We then sample from that distribution to get the latent code.

## The reparameterization trick

Sampling `z ~ N(μ, σ²)` directly is a problem — randomness blocks gradient flow. Backprop can't flow through "draw a random sample."

The trick: rewrite the sampling as

```
z = μ + σ · ε        where ε ~ N(0, 1)
```

Now `μ` and `σ` are deterministic outputs of the encoder, and the randomness is isolated in `ε` (which has no parameters). Gradients flow back through `μ` and `σ` cleanly.

This is **the** trick that makes VAEs trainable. Before this insight (Kingma & Welling, 2013), training generative latent-variable models with deep networks was extremely hard.

## The loss function

VAEs use the ELBO loss:

```
L_VAE = L_RECON + L_KL
```

- **`L_RECON`** = reconstruction error (MSE or BCE between `x` and `x̂`)
- **`L_KL`** = KL divergence forcing `q(z|x)` to be close to `N(0, I)`

For Gaussian distributions:

```
KL[N(μ, σ²) || N(0, I)] = (1/2) · Σⱼ [μⱼ² + σⱼ² - log(σⱼ²) - 1]
```

See `loss-functions/vae-loss.md` for full derivation.

## Why this produces a structured latent space

The KL term forces every input's encoded distribution to be close to `N(0, I)`. This means:

- All encoded points cluster around the origin
- The encoded distributions overlap
- Different inputs map to overlapping regions of latent space
- Random points sampled from `N(0, I)` will probably land in a region the decoder has seen

Result: **the latent space becomes continuous and meaningful**.

## Generating new data

After training, generation is trivial:

```python
z = sample from N(0, I)
x_new = decoder(z)
```

`x_new` is a brand new sample that looks like the training data but isn't a copy of any specific example.

## Latent space interpolation

Walk along a line between two latent codes:

```python
z_mix = (1 - t) * z_a + t * z_b   # for t in [0, 1]
x_mix = decoder(z_mix)
```

You get smooth transitions between the two original inputs. Famous demos: morph one face into another, smoothly age a person's photo, interpolate between poses.

## VAE vs vanilla autoencoder

| | Vanilla AE | VAE |
|---|------------|-----|
| Encoder outputs | Single point z | Distribution (μ, σ) |
| Latent space | Unstructured | Structured (close to N(0,I)) |
| Can generate new samples? | No (random z → garbage) | **Yes** |
| Smooth interpolation? | No | **Yes** |
| Loss | Reconstruction only | Reconstruction + KL |
| Use case | Compression, denoising | Generation, smooth representations |

## Trade-offs

**VAE pros:**
- Principled probabilistic framework
- Stable training (no GAN-style instability)
- Smooth latent space, easy interpolation

**VAE cons:**
- Outputs are **blurrier** than GAN outputs (because of the MSE/Gaussian assumption in reconstruction)
- Quality usually worse than GANs or diffusion models for images
- Balance between L_RECON and L_KL is tricky

## Modern variants

- **β-VAE** — increases the weight on KL term to get **disentangled** latent dimensions
- **VQ-VAE** — uses discrete (vector-quantized) latent space, fixed the blurriness, used in DALL-E
- **Hierarchical VAE (NVAE, VDVAE)** — multiple latent layers for sharper outputs

## VAE's place in 2026

VAEs aren't state-of-the-art for raw image generation anymore (diffusion models won). But:

- VAE encoders are still used inside diffusion models (Stable Diffusion uses a VAE for compression)
- The reparameterization trick is foundational for any model with stochastic latent variables
- VAEs remain useful when you need a **probabilistic** latent space, not just generation

## The big picture

Vanilla AE: "compress and reconstruct."
VAE: "compress, reconstruct, AND make the latent space samplable."

That second property is what makes VAEs **generative** while vanilla autoencoders are not.

---