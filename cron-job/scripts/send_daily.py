#!/usr/bin/env python3
"""Pick a weighted-random concept from the knowledge base and email it.

Optional LLM enhancement (via Groq) adds a quick recap and quiz questions.
If GROQ_API_KEY is missing or the call fails, falls back to the raw note.
"""

from __future__ import annotations

import os
import random
import smtplib
import sys
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import frontmatter
import markdown as md_lib

KNOWLEDGE_DIR = Path(os.environ.get("KNOWLEDGE_DIR", "monorepo"))
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

# LLM config — uses Groq's OpenAI-compatible endpoint
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
LLM_MODEL = os.environ.get("LLM_MODEL", "llama-3.3-70b-versatile")
LLM_ENABLED = os.environ.get("LLM_ENABLED", "true").lower() == "true"


def find_notes(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.md") if p.is_file() and p.name != "README.md"]


def score(post) -> float:
    """Higher score = more likely to be picked."""
    last = post.metadata.get("last_sent")
    reviews = post.metadata.get("review_count", 0) or 0
    if not last:
        return 1000.0  # never sent — top priority
    if isinstance(last, str):
        last = datetime.fromisoformat(last)
    if last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)
    days = (datetime.now(timezone.utc) - last).days
    return max(days * 10 - reviews * 5, 1.0)


def pick(notes: list[Path]):
    loaded = [(p, frontmatter.load(p)) for p in notes]
    weights = [score(post) for _, post in loaded]
    return random.choices(loaded, weights=weights, k=1)[0]


def enhance_with_llm(content: str, title: str, topic: str) -> str | None:
    """Ask Groq to add a recap and quiz questions to the note.

    Returns enhanced markdown, or None if the LLM call fails or is disabled.
    """
    if not LLM_ENABLED:
        return None

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("GROQ_API_KEY not set, skipping LLM enhancement", file=sys.stderr)
        return None

    try:
        from openai import OpenAI
    except ImportError:
        print("openai package not installed, skipping LLM enhancement", file=sys.stderr)
        return None

    client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)

    system_prompt = (
        "You are helping a software engineer review technical concepts via daily email. "
        "Your job is to enhance their existing notes with a quick recap at the top "
        "and quiz questions at the bottom. Be precise and technically accurate. "
        "Output only valid markdown with no preamble or explanation."
    )

    user_prompt = f"""Topic: {title}
Category: {topic}

Here is the note:

---
{content}
---

Enhance this note for daily email review. Return markdown in EXACTLY this format:

## Quick recap

[2-3 sentences capturing the core idea, written for someone half-awake reading email]

---

[the original note content, unchanged]

---

## Quiz

**1.** [easy recall question]

**2.** [application question — when would you use this, or what would happen if X]

**3.** [tradeoff or design-decision question]

<details>
<summary>Answers</summary>

**1.** [concise answer]

**2.** [concise answer with reasoning]

**3.** [concise answer with reasoning]

</details>"""

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=2500,
        )
        enhanced = response.choices[0].message.content
        if enhanced and len(enhanced) > 100:
            print(f"LLM enhancement succeeded ({len(enhanced)} chars)")
            return enhanced
        print("LLM returned suspiciously short content, falling back", file=sys.stderr)
        return None
    except Exception as e:
        print(f"LLM enhancement failed: {e}", file=sys.stderr)
        return None


def render(post, path: Path) -> tuple[str, str]:
    title = path.stem.replace("-", " ").replace("_", " ").title()
    topic = post.metadata.get("topic", "general")
    difficulty = post.metadata.get("difficulty", "")

    enhanced = enhance_with_llm(post.content, title, topic)
    body_markdown = enhanced if enhanced else post.content

    body_html = md_lib.markdown(
        body_markdown,
        extensions=["fenced_code", "tables", "nl2br", "sane_lists", "md_in_html"],
    )

    meta_line = topic + (f" &middot; {difficulty}" if difficulty else "")
    enhanced_badge = (
        '<span style="font-size: 11px; color: #999; margin-left: 8px;">[AI-enhanced]</span>'
        if enhanced
        else ""
    )

    html = f"""
<html>
  <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
               max-width: 640px; margin: 0 auto; padding: 24px; color: #222; line-height: 1.6;">
    <p style="color: #888; font-size: 13px; margin: 0 0 8px;">
      Today's concept &middot; {meta_line}{enhanced_badge}
    </p>
    {body_html}
    <hr style="border: none; border-top: 1px solid #eee; margin-top: 32px;">
    <p style="color: #999; font-size: 12px;">Sent from your what_i_know knowledge base.</p>
  </body>
</html>
"""
    return title, html


def send(subject: str, html_body: str) -> None:
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASS"]
    recipient = os.environ.get("RECIPIENT", user)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = recipient
    msg.attach(MIMEText(html_body, "html"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)


def update_meta(path: Path, post) -> None:
    post.metadata["last_sent"] = datetime.now(timezone.utc).isoformat()
    post.metadata["review_count"] = (post.metadata.get("review_count", 0) or 0) + 1
    with open(path, "wb") as f:
        frontmatter.dump(post, f)


def main() -> None:
    notes = find_notes(KNOWLEDGE_DIR)
    if not notes:
        print(f"No notes found in {KNOWLEDGE_DIR}", file=sys.stderr)
        sys.exit(1)
    path, post = pick(notes)
    print(f"Picked: {path}")
    subject, html = render(post, path)
    send(f"Today's concept: {subject}", html)
    update_meta(path, post)
    print("Sent and metadata updated.")


if __name__ == "__main__":
    main()