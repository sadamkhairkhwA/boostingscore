"""OpenAI Images API: educational sticker/cartoon for a vocabulary word (PNG bytes)."""
import base64
import json
import os
from typing import Any

import httpx

from boostingscore.openai_key import resolve_openai_api_key


def _post_images(
    api_key: str, base_url: str, org: str | None, project: str | None, timeout: float, body: dict[str, Any]
) -> dict[str, Any]:
    payload = json.dumps(body, ensure_ascii=False, allow_nan=False)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8",
    }
    if org:
        headers["OpenAI-Organization"] = org
    if project:
        headers["OpenAI-Project"] = project
    url = base_url.rstrip("/") + "/images/generations"
    with httpx.Client(timeout=timeout) as client:
        r = client.post(url, headers=headers, content=payload.encode("utf-8"))
    if r.status_code != 200:
        try:
            err = r.json()
            msg = err.get("error", {}).get("message") or r.text[:800]
        except Exception:
            msg = r.text[:800]
        raise RuntimeError(f"Image API {r.status_code}: {msg}")
    return r.json()


def build_illustration_prompt(*, word: str, definition: str, topic: str, level: int) -> str:
    w = (word or "").strip()
    d = (definition or "").strip()[:400]
    t = (topic or "general").replace("_", " ")
    return (
        f'Friendly educational illustration in a flat cartoon / sticker style, simple bold shapes, '
        f"soft pastel colors, clean vector-like look, no photorealism. "
        f'One clear visual metaphor for the English vocabulary idea: "{w}". '
        f"IELTS study card, topic: {t}, difficulty about level {level} of 3. "
        f"Context for the idea (do not write this text in the image): {d or 'infer from the word safely'}. "
        f"Absolutely no letters, words, numbers, captions, logos, or watermarks in the image. "
        f"Classroom-safe, neutral, not violent or adult."
    )


def generate_illustration_png_bytes(
    *,
    word: str,
    definition: str = "",
    topic: str = "general",
    level: int = 2,
    model: str | None = None,
) -> bytes:
    api_key = resolve_openai_api_key()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    model = (model or os.environ.get("OPENAI_IMAGE_MODEL", "dall-e-3")).strip()
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    org = os.environ.get("OPENAI_ORGANIZATION") or os.environ.get("OPENAI_ORG_ID")
    project = os.environ.get("OPENAI_PROJECT")
    timeout = float(os.environ.get("OPENAI_IMAGE_TIMEOUT", "120"))

    prompt = build_illustration_prompt(
        word=word, definition=definition, topic=topic, level=level if level in (1, 2, 3) else 2
    )

    body: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "response_format": "b64_json",
    }
    if model.startswith("dall-e-3"):
        body["size"] = "1024x1024"
        body["quality"] = os.environ.get("OPENAI_IMAGE_QUALITY", "standard").strip() or "standard"
    else:
        body["size"] = "512x512"

    data = _post_images(api_key, base_url, org, project, timeout, body)
    items = data.get("data") or []
    if not items:
        raise RuntimeError("Image API returned no image data.")
    b64 = (items[0].get("b64_json") or "").strip()
    if not b64:
        raise RuntimeError("Image API returned empty image.")
    return base64.standard_b64decode(b64)
