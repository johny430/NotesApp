from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

note_tag_association = Table('note_tag', Base.metadata,
                             Column('note_id', Integer, ForeignKey('notes.id')),
                             Column('tag_id', Integer, ForeignKey('tags.id'))
                             )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    notes = relationship("Note", back_populates="owner")


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="notes")

    tags = relationship("Tag", secondary=note_tag_association, back_populates="notes")


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    notes = relationship("Note", secondary=note_tag_association, back_populates="tags")
