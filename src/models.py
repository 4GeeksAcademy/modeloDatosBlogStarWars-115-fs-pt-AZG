from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_character = Table(
    "favorite_character",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("character_id", ForeignKey("character.id"))
)

favorite_planet = Table(
    "favorite_planet",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("planet_id", ForeignKey("planet.id"))
)



class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    favorite_character: Mapped[List["Character"]] = relationship("Character", secondary="favorite_character", back_populates="favorited_by")
    favorite_planet: Mapped[List["Planet"]] = relationship("Planet", secondary="favorite_planet", back_populates="favorite_by")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "favorite_character": [character.serialize() for character in favorite_character],
            "favorite_planet": [planet.serialize() for planet in favorite_planet]
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    favorited_by: Mapped[List["Character"]] = relationship("Character", secondary="favorite_character", back_populates="favorite_character")

    


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    favorited_by: Mapped[List["Planet"]] = relationship("Planet", secondary="favorite_planet", back_populates="favorite_planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
