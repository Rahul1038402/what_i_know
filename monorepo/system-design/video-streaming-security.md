---
difficulty: medium
last_sent: '2026-07-14T04:29:54.557716+00:00'
review_count: 3
tags:
- streaming
- security
- drm
- hls
topic: system-design
---

# Video streaming security layers

How streaming platforms protect video content from being downloaded, stacked from simplest tricks to hardware DRM.

## The core problem

You must send video bytes to the user's device for the player to render them, but you don't want the user to keep them. No scheme actually solves this — each layer raises the cost of bypassing until it exceeds the content's value.

## Layer 1: HLS chunking

Video chopped into thousands of 2-10s `.ts` segments. A master `.m3u8` playlist lists available bitrates; variant playlists list segments in order. Audio and video often split into separate streams.

Real purpose: adaptive bitrate, fast startup, CDN caching. Side effect: no single URL to right-click. Stops casual users immediately.

## Layer 2: Signed URL tokens

Every segment URL embeds an HMAC-based token:

```
/spees/w/<workspace>/v/<video>/u/<user>/t/<token>/...
```

Server computes `HMAC(user_id + video_id + expiry + secret)` and verifies on every request. Tokens expire in minutes. Same idea as AWS S3 presigned URLs.

Without valid auth cookies, every segment returns 403. This is why generic downloaders fail even when the playlist parses.

## Layer 3: AES-128 encryption at rest

Segments encrypted on storage. The playlist tells the player where to fetch the key:

```
#EXT-X-KEY:METHOD=AES-128,URI="key-endpoint",IV=0x...
```

The IV (initialization vector) is published in the clear — it's not secret, just ensures identical plaintext blocks encrypt differently. The actual key is what matters.

Standard HLS: key endpoint returns exactly **16 raw bytes**. yt-dlp handles this layer cleanly when auth works.

## Layer 4: Custom key wrapping

Key endpoint returns more than 16 bytes (Spayee returns 48). Custom unwrap logic that only the platform's player knows. Common schemes:

- Real key XOR'd with a session-derived value
- AES-encrypting the real key with a second key hardcoded in player JS
- Real key scattered at fixed offsets within the blob
- Key + HMAC signature + padding
- Custom binary format with the key as one field

Bypassing requires reverse-engineering minified JS. Platforms can silently change the wrapping by pushing a new player build, breaking existing downloaders overnight.

Legal line: circumventing this scheme triggers anti-circumvention laws (US DMCA, India's Copyright Act Section 65A).

## Layer 5: Hardware DRM (Widevine, FairPlay, PlayReady)

Different universe. Encryption happens inside a **TEE** (Trusted Execution Environment) — a separate hardware chip. Keys never enter normal RAM. Decrypted frames travel through a protected video path direct to the screen.

Widevine license flow:

1. Browser requests license with a device challenge
2. Challenge proves the device has a valid, unrevoked Widevine cert
3. Server returns a license encrypted to that specific device
4. Widevine module decrypts the license, extracts the content key, decrypts video — all inside the secure enclave

Three security levels:

- **L1**: hardware path (high-end Android, iPhones) — supports 4K
- **L2**: middle tier (rarely used)
- **L3**: software-only (desktop browsers) — typically capped at 720p

L3 has been broken (key extraction). L1 has held up — requires hardware-level attacks. This is why Netflix streams 4K on smart TVs but only 720p in Chrome.

Also why screen recording sometimes shows a black rectangle — the OS honors the protected video path's no-capture flag.

## Layer 6: Supporting measures

- **Forensic watermarking** — invisible per-user pixel modifications that survive re-encoding; identifies which account leaked
- **Player integrity checks** — anti-debug, browser-automation detection
- **Domain locking** — license server validates `Origin`/`Referer` headers
- **Per-session URL randomization** — same chunk has different URLs per viewer per session

## Why layered defense works

Each layer filters a different attacker tier:

| Layer | Stops |
|-------|-------|
| 1 — chunking | Right-click savers |
| 2 — auth | Generic downloaders without cookies |
| 3 — AES | Scripted segment fetchers |
| 4 — custom wrap | yt-dlp users |
| 5 — hardware DRM | Everyone except chip-level researchers |

By layer 5, only a tiny population can bypass — they release one rip everyone else copies, so the platform focuses anti-piracy on that small group.

## Real platform stacks

- College LMS (Spayee, Teachable): L1-L4
- YouTube: L1-L3 (mostly URL signing)
- Coursera: L1-L4
- Netflix, Disney+: L1-L5 (full Widevine L1 where supported)

## Trade-offs

- More security = more legitimate-user friction
- Hardware DRM limits compatibility (no Linux, older devices)
- Higher security = licensing costs (Widevine isn't free)
- Match security to threat model — college LMS doesn't need Netflix-grade protection

## Further reading

- W3C Encrypted Media Extensions (EME) spec
- Widevine architecture overview
- "A Glimpse of the Matrix" paper — Widevine L3 internals