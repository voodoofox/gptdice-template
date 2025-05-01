
# GPTDice Quest Generator (Template)

A **FastAPI** micro‑service that combines a cryptographically secure random number generator with OpenAI GPT
to create repeatable RPG quest text.

## Quick start on Replit

1. Fork this repo to your account.
2. Add an **OPENAI_API_KEY** secret.
3. Click **Run** – Replit will install `requirements.txt` and launch `uvicorn main:app`.
4. Your live endpoint will be displayed; test it:

```bash
curl -X POST {"url"}/generateQuest -H "Content-Type: application/json" -d '{"theme":"pirates", "seed":42}'
```

## Endpoint

`POST /generateQuest`

| Field | Type | Description |
|-------|------|-------------|
| `seed` | int? | Optional. If omitted, service draws a secure random seed. |
| `theme` | str | One of the keys in `templates/quests.yaml` (`generic` if missing). |

Returns JSON with the quest, seed, and a SHA‑256 proof for auditability.

---
