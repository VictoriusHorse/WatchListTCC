from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    owner_id = Column(Integer, ForeignKey("users.id"))
    movieId = Column(Integer, index=True)
    rating = Column(Integer, index=True)
    id = Column(Integer, primary_key=True, index=True)

    owner = relationship("User", back_populates="items")

class Movie(Base):
    __tablename__ = "Movies"
    movieId = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    genres = Column(String(255), index=True)
    poster = Column(String(9999999))

class Recommend(Base):
    __tablename__ = "recommend"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    movieId = Column(Integer, index=True)
    description = Column(String(255),index=True)
    poster = Column(String(9999999),index=True)
    userId = Column(Integer, index=True)

