from pydantic import BaseModel

class ItemBase(BaseModel):
    movieId: int
    rating: float


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

class Movie(BaseModel):
    movieId: int
    title: str
    description: str
    genres: str
    poster: str

class Poster(BaseModel):
    poster: bytes


class Recommend (BaseModel):
    id: int
    title: str
    movieId: int
    description: str
    poster: str
    userId: int

class NotRecommend (BaseModel):
    movieId: int
    title: str
    description: str
    poster: str

class Config:
    orm_mode = True

