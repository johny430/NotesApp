from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models


async def create_note(db: AsyncSession, title: str, content: str, user_id: int, tags: list):
    note = models.Note(title=title, content=content, owner_id=user_id)
    if tags:
        note.tags = await get_or_create_tags(db, tags)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_notes_by_user(db: AsyncSession, user_id: int):
    query = select(models.Note).filter(models.Note.owner_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_note_by_id(db: AsyncSession, note_id: int, user_id: int):
    query = select(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == user_id)
    result = await db.execute(query)
    return result.scalar()


async def update_note(db: AsyncSession, note: models.Note, title: str, content: str, tags: list):
    note.title = title
    note.content = content
    if tags:
        note.tags = await get_or_create_tags(db, tags)
    await db.commit()
    await db.refresh(note)
    return note


async def delete_note(db: AsyncSession, note: models.Note):
    await db.delete(note)
    await db.commit()


async def get_or_create_tags(db: AsyncSession, tag_names: list):
    tags = []
    for name in tag_names:
        tag = await db.execute(select(models.Tag).filter(models.Tag.name == name))
        tag = tag.scalar()
        if not tag:
            tag = models.Tag(name=name)
            db.add(tag)
            await db.commit()
            await db.refresh(tag)
        tags.append(tag)
    return tags
