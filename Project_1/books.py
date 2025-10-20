from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Two', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


class Book(BaseModel):
    title: str
    author: str
    category: str


@app.get("/books")
# async is optional for API
async def read_all_books():
    return BOOKS


@app.get("/books/{title}")
def book_title(title: str):
    for book in BOOKS:
        if book['title'].casefold() == title.casefold():
            return book


@app.get("/books/")
def book_by_category(category: str):
    books = []
    for book in BOOKS:
        if book['category'].casefold() == category.casefold():
            books.append(book)
    return books


@app.get("/books/byAuthor/")
def books_by_author(author: str):
    books = []
    for book in BOOKS:
        if book['author'].casefold() == author.casefold():
            books.append(book)
    return books


@app.get("/books/{author}/")
def books_by_author_and_category(author: str, category: str):
    books = []
    for book in BOOKS:
        if (book['author'].casefold() == author.casefold() and
                book['category'].casefold() == category.casefold()):
            books.append(book)
    return books


@app.post("/books/create_book")
async def create_book(new_book: Book):
    BOOKS.append(new_book.dict())   # Convert Pydantic model → dict
    return BOOKS

@app.put("/books/update_book")
async def update_book(new_book: Book):
    for i in range(len(BOOKS)):
        if(BOOKS[i]['title'].casefold() == new_book.title.casefold()):
            BOOKS[i]= new_book.dict()
    return BOOKS

@app.delete("/books/delete_book")
async def delete_book(new_book: Book):
    for book in BOOKS:
        if(book['title'].casefold() == new_book.title.casefold()):
            BOOKS.remove(book)
    return BOOKS

