
import os, random, hashlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import yaml

app = FastAPI(title="GPTDice Quest Generator")

class QuestRequest(BaseModel):
    seed: int | None = None
    theme: str = "generic"

with open(os.path.join(os.path.dirname(__file__), "templates", "quests.yaml"), "r", encoding="utf-8") as f:
    templates = yaml.safe_load(f) or {}

def secure_random_int() -> int:
    # 64‑bit cryptographically secure random integer
    return random.SystemRandom().randint(0, 2**64-1)

@app.post("/generateQuest")
async def generate_quest(req: QuestRequest):
    seed = req.seed if req.seed is not None else secure_random_int()
    random.seed(seed)

    template = templates.get(req.theme.lower(), templates.get("generic", "Generate a concise quest using seed {seed}."))
    prompt = template.format(seed=seed)

    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    quest_text = resp.choices[0].message.content.strip()
    proof = hashlib.sha256(str(seed).encode()).hexdigest()

    return {"seed": seed,
            "prompt": prompt,
            "quest": quest_text,
            "sha256_proof": proof}
