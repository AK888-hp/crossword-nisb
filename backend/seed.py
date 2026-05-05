import json
import os
from database import SessionLocal, engine
import models

def seed():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Create admin user if not exists
    admin = db.query(models.User).filter(models.User.username == "CROSSCURRENT_ADMIN").first()
    if not admin:
        admin = models.User(username="CROSSCURRENT_ADMIN", is_admin=True, password="CROSSCURRENT_123")
        db.add(admin)
        db.commit()

    # Load words
    json_path = os.path.join(os.path.dirname(__file__), '..', 'crossword_data.json')
    if not os.path.exists(json_path):
        print(f"Data file not found at {json_path}")
        return

    # Clear old words so we don't mix old grid with new grid
    db.query(models.Word).delete()
    db.commit()

    with open(json_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        
    for word_data in data.get("words", []):
        word_text = word_data["word"]
        existing = db.query(models.Word).filter(models.Word.word == word_text).first()
        if not existing:
            new_word = models.Word(
                word=word_text,
                clue=word_data["clue"],
                direction=word_data["direction"],
                x=word_data["x"],
                y=word_data["y"],
                length=len(word_text)
            )
            db.add(new_word)
    
    db.commit()
    db.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed()
