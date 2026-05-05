from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import models
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (images, html)
static_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class UserLogin(BaseModel):
    username: str

class AdminLogin(BaseModel):
    username: str
    password: str

class WordAttempt(BaseModel):
    x: int
    y: int
    direction: str
    word: str

class ScoreSubmit(BaseModel):
    username: str
    score: int
    time_seconds: int

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        db_user = models.User(username=user.username, is_admin=False)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return {"message": "Login successful", "username": db_user.username, "is_admin": db_user.is_admin}

@app.post("/admin/login")
def admin_login(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(models.User).filter(
        models.User.username == admin.username,
        models.User.password == admin.password,
        models.User.is_admin == True
    ).first()
    if not db_admin:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    return {"message": "Admin login successful", "is_admin": True}

@app.get("/grid")
def get_grid(db: Session = Depends(get_db)):
    # Read grid dimensions from json
    json_path = os.path.join(os.path.dirname(__file__), '..', 'crossword_data.json')
    dimensions = {"width": 20, "height": 20}
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            dimensions = data.get("grid", dimensions)

    words = db.query(models.Word).all()
    # DO NOT SEND ACTUAL WORDS! Only metadata and clues.
    safe_words = []
    for w in words:
        safe_words.append({
            "id": w.id,
            "clue": w.clue,
            "direction": w.direction,
            "x": w.x,
            "y": w.y,
            "length": w.length
        })
    return {"dimensions": dimensions, "words": safe_words}

@app.post("/validate")
def validate_word(attempt: WordAttempt, db: Session = Depends(get_db)):
    word = db.query(models.Word).filter(
        models.Word.x == attempt.x,
        models.Word.y == attempt.y,
        models.Word.direction == attempt.direction
    ).first()
    
    if not word:
        return {"correct": False, "points": 0}
        
    if word.word.upper() == attempt.word.upper():
        return {"correct": True, "points": 5}
    return {"correct": False, "points": 0}

@app.post("/score")
def submit_score(score_data: ScoreSubmit, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == score_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    new_score = models.Score(
        user_id=user.id,
        score=score_data.score,
        time_seconds=score_data.time_seconds
    )
    db.add(new_score)
    db.commit()
    return {"message": "Score saved successfully"}

@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    # Calculate top scores based on lowest time
    scores = db.query(models.Score).order_by(
        models.Score.time_seconds.asc()
    ).limit(10).all()
    
    result = []
    for s in scores:
        result.append({
            "username": s.user.username,
            "score": s.score,
            "time_seconds": s.time_seconds
        })
    return result
