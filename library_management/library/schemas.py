from ninja import Schema
from datetime import date

# Schema for Book model
class BookSchema(Schema):
    title: str
    author: str
    published_date: date  # Publication date of the book

# Schema for Borrow model
class BorrowSchema(Schema):
    user_id: int  # ID of the user who borrows the book
    book_id: int  # ID of the borrowed book
