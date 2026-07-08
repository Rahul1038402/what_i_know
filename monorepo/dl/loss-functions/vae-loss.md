---
difficulty: hard
last_sent: '2026-07-08T04:48:31.905982+00:00'
review_count: 3
tags:
- loss-functions
- vae
- elbo
- kl-divergence
- generative-models
topic: deep-learning
---

# VAE Loss (ELBO)

The loss function used to train Variational Autoencoders. Combines reconstruction quality with a constraint that the latent space be smooth and continuous.

## The full formula

```
L_VAE = L_RECON + L_KL
```

Two competing objectives, balanced together. The network must reconstruct the input well AND keep the latent distribution close to a standard normal.

## 1. Reconstruction loss

```
L_RECON = E[||x - D_θ(z)||²]
```

Standard MSE between input `x` and the decoder's reconstruction `D_θ(z)`. This term forces the decoder to produce outputs that look like the input.

For images, sometimes Binary Cross-Entropy is used instead of MSE — pixel-wise BCE works better for normalized [0,1] images.

## 2. KL divergence (regularization)

```
L_KL = KL[q_φ(z|x) || N(0, I)]
```

Forces the encoder's output distribution `q_φ(z|x)` to stay close to a standard normal `N(0, I)`. This is what makes VAEs different from regular autoencoders — the latent space gets organized.

For Gaussian distributions, KL has a closed form:

```
KL[N(μ, σ²) || N(0, I)] = (1/2) · Σⱼ [μⱼ² + σⱼ² - log(σⱼ²) - 1]
```

You can compute this directly from the encoder's outputs (μ and σ) — no sampling needed.

## What each term does

- **Reconstruction loss alone** → vanilla autoencoder. Latent space is unstructured, can't sample from it meaningfully.
- **KL divergence alone** → encoder collapses to always output N(0, I). Decoder gets garbage input, can't reconstruct.
- **Together** → encoder must produce useful, **organized** latent distributions that lie close to a Gaussian prior but are still discriminative enough for the decoder to reconstruct.

## The reparameterization trick

To backprop through the sampling step `z ~ N(μ, σ²)`, we rewrite it as:

```
z = μ + σ · ε    where ε ~ N(0, 1)
```

Now `μ` and `σ` are deterministic outputs of the encoder, and the randomness is isolated in `ε` (which has no parameters to learn). Gradients can flow back through `μ` and `σ`.

Without this trick, sampling would block gradients and the encoder couldn't be trained.

## ELBO interpretation

VAE loss is the **negative ELBO** (Evidence Lower BOund). Mathematically, minimizing this loss is equivalent to maximizing a lower bound on `log p(x)` — the probability the model assigns to the data. So VAEs are doing approximate maximum likelihood under a probabilistic model.

You don't need to know the proof to use VAEs, but the name "ELBO" comes up in papers a lot.

## Why this matters

Once trained, you can sample `z ~ N(0, I)` and decode it to get a brand new generated sample. The KL constraint is what makes this work — without it, random points in latent space wouldn't decode to anything sensible.

This is also what makes VAEs useful for interpolation: walk along a line in latent space and the decoded outputs change smoothly.

See `autoencoders/variational-autoencoders.md` for the full architecture.