from ninja import NinjaAPI, Schema, Router
from typing import List
from library.models import Book, Borrow, User
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Initialize the Ninja API
api = NinjaAPI()

# Define schema for Book model
class BookSchema(Schema):
    id: int
    title: str
    author: str
    published_date: str
    is_borrowed: bool

# Define schema for creating a Book
class BookCreateSchema(Schema):
    title: str
    author: str
    published_date: str

# Define schema for Borrow model
class BorrowSchema(Schema):
    id: int
    user_id: int
    book_id: int
    borrowed_date: str
    return_date: str = None

# Define schema for borrowing a book
class BorrowRequestSchema(Schema):
    user_id: int
    book_id: int

# Create routers for admin and user
admin_router = Router()
user_router = Router()

# Endpoint to add a book
@admin_router.post("/books", response=BookSchema)
def add_book(request, payload: BookCreateSchema):
    book = Book.objects.create(**payload.dict())
    return book

# Endpoint to update a book
@admin_router.put("/books/{book_id}", response=BookSchema)
def update_book(request, book_id: int, payload: BookCreateSchema):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return book

# Endpoint to delete a book
@admin_router.delete("/books/{book_id}", response=dict)
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}

# Endpoint to list all books
@admin_router.get("/books", response=List[BookSchema])
def list_books(request):
    books = Book.objects.all()
    return books

# Endpoint to list available books
@user_router.get("/books", response=List[BookSchema])
def list_available_books(request):
    books = Book.objects.filter(is_borrowed=False)
    return books

# Endpoint to borrow a book
@user_router.post("/borrow", response=BorrowSchema)
def borrow_book(request, payload: BorrowRequestSchema):
    book = get_object_or_404(Book, id=payload.book_id)
    if book.is_borrowed:
        return {"error": "Book is already borrowed"}
    user = get_object_or_404(User, id=payload.user_id)
    borrow = Borrow.objects.create(book=book, user=user, borrowed_date=timezone.now())
    book.is_borrowed = True
    book.save()
    return borrow

# Endpoint to return a borrowed book
@user_router.post("/return", response=BorrowSchema)
def return_book(request, borrow_id: int):
    borrow = get_object_or_404(Borrow, id=borrow_id)
    borrow.return_date = timezone.now()
    borrow.book.is_borrowed = False
    borrow.book.save()
    borrow.save()
    return borrow

# Add routers to the API
api.add_router("/admin", admin_router)
api.add_router("/user", user_router)
