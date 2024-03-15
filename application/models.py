from sqlalchemy.orm import (
    Mapped, mapped_column, relationship
)
from sqlalchemy import ForeignKey, BLOB
from application.database import db
from typing import List
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(nullable=True)
    requests: Mapped[List["Register"]] = relationship()
    # one to many relationship with Register


class Section(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    books: Mapped[List["Book"]] = relationship("Book", backref="section")
    # one to many relationship with Book


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    content: Mapped[BLOB] = mapped_column(BLOB)
    image: Mapped[BLOB] = mapped_column(BLOB)
    stock: Mapped[int]
    section_id: Mapped[int] = mapped_column(ForeignKey("section.id"))


class Register(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    book_name: Mapped[str]
    request_date: Mapped[str]
    approve_date: Mapped[str] = mapped_column(nullable=True)
    return_date: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str]
    request_type: Mapped[str]
