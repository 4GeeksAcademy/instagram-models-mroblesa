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
    password: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[List["FavPlanet"]] = relationship(back_populates= 'user')
    user: Mapped[List["FavPeople"]] = relationship(back_populates = 'user')
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name" : self.name
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable= False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    gravity: Mapped[int] = mapped_column(Integer, nullable=False)
    image: Mapped[str] = mapped_column(String(120), nullable=True)
    planets: Mapped[List["People"]] = relationship(back_populates='birth_planet')
    planet: Mapped["FavPlanet"] = relationship('planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "population": self.population,
            "gravity": self.gravity,
            "image": self.image,
            "planet_id": self.list
        }

class FavPlanet(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped[User] = relationship(User, back_populates="fav_planet")
    planet: Mapped["Planets"] = relationship("Planets")

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
       }

class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[str] = mapped_column(String(120), nullable=True)
    image: Mapped[str] = mapped_column(String(120), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    birth_planet: Mapped["Planets"] = relationship("Planets", back_populates='planets')
   
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "height": self.height,
            "image": self.image,
            "birth_planet": self.birth_planet
        }

class FavPeople(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    people_id : Mapped[int] = mapped_column(ForeignKey("people.id"))
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship("User", back_populates = 'fav_people')
    people: Mapped["People"] = relationship("People")

    def serialize_fav_people(self):
        return {
            "id": self.id,
            "people_id" : self.people_id,
            "user_id" : self.user_id
        }