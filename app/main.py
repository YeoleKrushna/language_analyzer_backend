from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

from . import models, schemas
from .database import engine, get_db, Base
from .auth import router as auth_router
from .model_loader import correct_sentence

# ------------------------------
# Create all tables (if not exist)
# ------------------------------
Base.metadata.create_all(bind=engine)

# ------------------------------
# Initialize FastAPI app
# ------------------------------
app = FastAPI(title="Language Analyzer: Marathi")

# ------------------------------
# CORS Middleware
# ------------------------------
origins = [
    "https://yourusername.github.io",  # Replace with your GitHub Pages URL
    "http://localhost:5500"            # For local testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Include Auth Router
# ------------------------------
app.include_router(auth_router)

# ------------------------------
# Analyze Endpoint
# ------------------------------
@app.post("/analyze", response_model=schemas.HistoryOut)
def analyze_text(
    text: schemas.HistoryCreate,
    db: Session = Depends(get_db)
):
    # Correct sentence using your model
    corrected_text = correct_sentence(text.input_text)
    
    # Save to history if user_id provided
    if hasattr(text, "user_id") and text.user_id:
        history_entry = models.History(
            user_id=text.user_id,
            input_text=text.input_text,
            corrected_text=corrected_text
        )
        db.add(history_entry)
        db.commit()
        db.refresh(history_entry)
        return history_entry
    
    # If no user_id, just return corrected text without saving
    return {"input_text": text.input_text, "corrected_text": corrected_text, "timestamp": None}

# ------------------------------
# User History Endpoint
# ------------------------------
@app.get("/history", response_model=List[schemas.HistoryOut])
def get_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(models.History).filter(models.History.user_id == user_id).order_by(models.History.timestamp.desc()).all()
    return history

# ------------------------------
# User Profile Endpoint
# ------------------------------
@app.get("/profile", response_model=schemas.UserOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
