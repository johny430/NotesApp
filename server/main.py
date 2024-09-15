from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.engine import url
from sqlalchemy.ext.asyncio import AsyncSession

import auth
import db
import endpoints
import models

app = FastAPI()


@app.post("/register")
async def register(username: str, password: str, db: AsyncSession = Depends(db.get_db)):
    hashed_password = await auth.get_password_hash(password)
    user = models.User(username=username, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    return {"message": "User created successfully"}


@app.post("/token")
async def login_for_access_token(username: str, password: str, db: AsyncSession = Depends(db.get_db)):
    user = await auth.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = await auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/notes")
async def read_notes(db: AsyncSession = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return await endpoints.get_notes_by_user(db, current_user.id)


@app.post("/notes")
async def create_note(title: str, content: str, tags: list = [], db: AsyncSession = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return await endpoints.create_note(db, title, content, current_user.id, tags)


@app.put("/notes/{note_id}")
async def update_note(note_id: int, title: str, content: str, tags: list = [], db: AsyncSession = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    note = await endpoints.get_note_by_id(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return await endpoints.update_note(db, note, title, content, tags)


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    note = await url.get_note_by_id(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await endpoints.delete_note(db, note)
    return {"message": "Note deleted successfully"}
