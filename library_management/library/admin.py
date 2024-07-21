from django.contrib import admin
from .models import Book, Borrow, User

# Register the Book model with the Django admin site
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view for books
    list_display = ('title', 'author', 'published_date', 'copies', 'is_borrowed')

# Register the Borrow model with the Django admin site
@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view for borrows
    list_display = ('user', 'book', 'borrowed_date', 'return_date')

# Register the User model with the Django admin site
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
