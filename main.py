from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import database
import os

app = FastAPI(title="Code Quest Backend")
ADMIN_KEY = "changeme123"  # change this to your own secret before deploying

# Allow your itch.io page (and, for now, anything) to call this API.
# Once deployed, tighten allow_origins to your actual itch.io URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the scores table on startup if it doesn't exist yet
database.init_db()


class ScoreSubmission(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    xp: int = Field(ge=0, le=1_000_000)  # basic sanity limits


@app.get("/")
def root():
    return {"message": "Code Quest backend is running."}


@app.post("/submit-score")
def submit_score(entry: ScoreSubmission):
    database.save_score(entry.name, entry.xp)
    return {"status": "saved", "name": entry.name, "xp": entry.xp}


@app.get("/leaderboard")
def leaderboard():
    return database.get_top_scores(limit=10)

@app.delete("/clear-leaderboard")
def clear_leaderboard(key: str):
    if key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid key")
    database.clear_scores()
    return {"status": "cleared"}
