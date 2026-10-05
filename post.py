"""Generate a LinkedIn post with Gemini (free tier) and publish it via LinkedIn's official API."""
import json
import os
import random
import sys

import requests

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
LINKEDIN_TOKEN = os.environ["LINKEDIN_ACCESS_TOKEN"]
LINKEDIN_PERSON_ID = os.environ.get("LINKEDIN_PERSON_ID", "").strip()
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"

# ---- EDIT THIS: describe yourself so posts sound like you ----
PERSONA = (
    "You write LinkedIn posts for a professional. "
    "EDIT: add your profession, audience and tone here, e.g. "
    "'a junior software developer sharing practical lessons with other beginners'."
)

STYLE_RULES = (
    "Rules: strong first-line hook; short paragraphs of 1-2 sentences; "
    "conversational and authentic, no corporate buzzwords; at most 2 emojis; "
    "120-200 words; end with a question that invites comments; "
    "put exactly 3 relevant hashtags on the final line. "
    "Output ONLY the post text, nothing else."
)


def pick_topic() -> str:
    with open("topics.json", encoding="utf-8") as f:
        topics = json.load(f)
    return random.choice(topics)


def generate_post(topic: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    prompt = f"{PERSONA}\n\n{STYLE_RULES}\n\nTopic: {topic}"
    resp = requests.post(
        url,
        headers={"x-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=60,
    )
    resp.raise_for_status()
    text = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    if not text:
        raise RuntimeError("Gemini returned an empty post")
    return text


def get_person_id() -> str:
    if LINKEDIN_PERSON_ID:
        return LINKEDIN_PERSON_ID
    resp = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {LINKEDIN_TOKEN}"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["sub"]


def publish(text: str) -> None:
    person_id = get_person_id()
    body = {
        "author": f"urn:li:person:{person_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    resp = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {LINKEDIN_TOKEN}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        },
        json=body,
        timeout=30,
    )
    if resp.status_code >= 400:
        print(f"LinkedIn error {resp.status_code}: {resp.text}", file=sys.stderr)
        resp.raise_for_status()
    print("Posted successfully:", resp.headers.get("x-restli-id", "(no id returned)"))


def main() -> None:
    topic = pick_topic()
    print(f"Topic: {topic}\n")
    post = generate_post(topic)
    print("--- Generated post ---")
    print(post)
    print("----------------------\n")
    if DRY_RUN:
        print("DRY_RUN is on: not publishing.")
        return
    publish(post)


if __name__ == "__main__":
    main()
