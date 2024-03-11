from sqlalchemy.orm import (
    Mapped, mapped_column, relationship
)
from sqlalchemy import ForeignKey
from database import db
from typing import List


class User(db.Model):
    __table__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]


class Section(db.Model):
    __tablename__ = "section_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    books: Mapped[List["Book"]] = relationship()


class Book(db.Model):
    __tablename__ = "book_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    section_id: Mapped[int] = mapped_column(ForeignKey("section_table.id"))
