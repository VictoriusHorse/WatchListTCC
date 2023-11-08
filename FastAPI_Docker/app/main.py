from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from app import crud
from app import schemas
from app import database
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from databases import Database

databases = Database("mysql+pymysql://tccapp:yE2KGUn7!Nqchvd@watchlist.mysql.database.azure.com/app_db")

app = FastAPI(
    title="My App",
    description="Description of my app.",
    version="1.0",
    docs_url='/docs',
    openapi_url='/openapi.json',
    redoc_url=None)
database.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/movies/", response_model=schemas.Movie)
def read_Movie(movie_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_movie(db, movie_id=movie_id)
    return db_user

@app.get("/poster/", response_model=schemas.Poster)
def read_poster(movie_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_poster(db, movie_id=movie_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Poster not found")
    return db_user

@app.get("/recommend/", response_model=list[schemas.Recommend])
def read_recommend(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_recommend(db, skip=skip, limit=limit)
    return items

@app.get("/not_recommend/", response_model=list[schemas.NotRecommend])
async def read_db():
    await databases.connect()
    data = await databases.fetch_all("SELECT recommend.movieId, recommend.title, recommend.description, recommend.poster FROM recommend LEFT JOIN items ON items.movieId = recommend.movieID WHERE items.id IS NULL LIMIT 0,10")
    return data



