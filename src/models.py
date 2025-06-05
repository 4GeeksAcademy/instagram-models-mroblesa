from __future__ import annotations
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    username: Mapped[str] = mapped_column(String(120), nullable=False)

    author_id: Mapped[Comment]= relationship("Comment", back_populates= "author")
    


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name" : self.name,
            "username": self.username
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String[80], nullable=False)
    comment: Mapped[str] = mapped_column(String[400], nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    post_id: Mapped[List[Media]] = relationship("Media", back_populates="post_media")
    post_comment_id: Mapped[List[Comment]] = relationship("Comment", back_populates="post_comment")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "comment": self.comment,
            "user_id": self.list,
            
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    url: Mapped[str] = mapped_column(String[300], nullable= False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    post_media: Mapped[Post] = relationship(Post, back_populates="post_id")


    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "post_id": self.post_id
       }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    text: Mapped[str] = mapped_column(String[400], nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_comment_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    author: Mapped[User] = relationship("User", back_populates="author_id")
    post_comment: Mapped[Post] = relationship("Post", back_populates="post_comment_id")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "author_id": self.author_id,
            "post_comment_id": self.post_comment_id
        }
