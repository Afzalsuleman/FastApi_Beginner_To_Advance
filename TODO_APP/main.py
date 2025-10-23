from fastapi import FastAPI, Depends,Path, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

import Models
from Models import Todos

from db import engine,SessionLocal

app = FastAPI()

Models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
@app.get("/")
def read_all(db:db_dependency):
    return db.query(Todos).all()

@app.get("/todos/{id}")
def get_by_id(db:db_dependency,id:int=Path(gt=0)):
    return db.query(Todos).filter(Todos.id == id).first()