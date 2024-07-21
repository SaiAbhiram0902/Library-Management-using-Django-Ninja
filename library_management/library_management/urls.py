from django.contrib import admin
from django.urls import path, include
from library.views import (
    home,
    admin_dashboard,
    user_dashboard,
    login_view,
    register_view,
    logout_view,
    api_books,
    api_book_detail,
    api_borrow_book,
    api_return_book,
)
from ninja import NinjaAPI

# Initialize the Ninja API instance
api = NinjaAPI()

@api.get("/books")
def list_books(request):
    books = Book.objects.all()
    data = [{'id': book.id, 'title': book.title, 'author': book.author, 'published_date': book.published_date, 'copies': book.copies} for book in books]
    return data

@api.post("/books")
def create_book(request, payload: dict):
    book = Book.objects.create(
        title=payload['title'],
        author=payload['author'],
        published_date=payload['published_date'],
        copies=payload['copies']
    )
    return {"id": book.id}

@api.get("/books/{book_id}")
def get_book(request, book_id: int):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return {"error": "Book not found"}, 404
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'published_date': book.published_date,
        'copies': book.copies,
    }

@api.put("/books/{book_id}")
def update_book(request, book_id: int, payload: dict):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return {"error": "Book not found"}, 404
    book.title = payload['title']
    book.author = payload['author']
    book.published_date = payload['published_date']
    book.copies = payload['copies']
    book.save()
    return {"id": book.id}

@api.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return {"error": "Book not found"}, 404
    book.delete()
    return {"success": True}

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('', home, name='home'),  # Home page URL
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),  # Admin dashboard URL
    path('user-dashboard/', user_dashboard, name='user_dashboard'),  # User dashboard URL
    path('login/', login_view, name='login'),  # Login URL
    path('register/', register_view, name='register'),  # Registration URL
    path('logout/', logout_view, name='logout'),  # Logout URL
    path('api/admin/books/', api_books, name='api_books'),  # Admin API for books list
    path('api/admin/books/<int:book_id>/', api_book_detail, name='api_book_detail'),  # Admin API for book details
    path('api/user/books/', api_books, name='user_books'),  # User API for books list
    path('api/user/books/borrow/<int:book_id>/', api_borrow_book, name='api_borrow_book'),  # User API for borrowing books
    path('api/user/books/return/<int:book_id>/', api_return_book, name='api_return_book'),  # User API for returning books
    path('api/', api.urls),  # Include all NinjaAPI routes
]
