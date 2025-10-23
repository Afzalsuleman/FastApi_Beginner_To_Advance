import datetime
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, Body
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: datetime):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]
class book_request(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
                                 "example": {
                                     "title": "A new book",
                                     "author": "codingwithroby",
                                     "description": "A new description of a book",
                                     "rating": 5,
                                     'published_date': 2029
                                 }
                             }
    }

@app.get("/books",status_code=status.HTTP_200_OK)
def get_books():
    return BOOKS

@app.get("/books/published_date",status_code=status.HTTP_200_OK)
def get_published_date(published_date: int=Query(gt=1999, lt=2031)):
    book_toReturn=[]
    for book in BOOKS:
        if book.published_date == published_date:
            book_toReturn.append(book)
    return book_toReturn

@app.get("/books/ratings",status_code=status.HTTP_200_OK)
def get_ratings(book_rating: int=Query(gt=0, lt=6)):
    rated_books=[]
    for book in BOOKS:
        if book.rating == book_rating:
            rated_books.append(book)
    return rated_books

@app.get("/books/{book_id},status_code=status.HTTP_200_OK")
def get_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

def get_id(book: Book,status_code=status.HTTP_200_OK):
    book.id=1 if len(BOOKS) == 0 else BOOKS[-1].id+1
    return book;

@app.post("/books/create_book",status_code=status.HTTP_201_CREATED)
def create_book(new_book: book_request):
    nnew_book = Book(**new_book.model_dump())
    BOOKS.append(get_id(nnew_book))
    return BOOKS

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
def update_book(update_book: book_request):
    falg=False
    for i in range (len(BOOKS)):
        if BOOKS[i].id == update_book.id:
            BOOKS[i]= update_book
            falg=True
            return BOOKS
        if not falg:
            raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(gt=0)):
    book_deleted=False
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            book_deleted=True
    if not book_deleted:
            raise HTTPException(status_code=404, detail="Book not found")

