from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Custom User model extending AbstractUser
class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related name for user groups
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Custom related name for user permissions
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

# Book model to store book information
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    published_date = models.DateField()
    copies = models.PositiveIntegerField(default=1)  # Number of available copies
    is_borrowed = models.BooleanField(default=False)  # Borrowed status

    def __str__(self):
        return self.title

# Borrow model to manage book borrow records
class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who borrowed the book
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Borrowed book
    borrowed_date = models.DateField(auto_now_add=True)  # Date when the book was borrowed
    return_date = models.DateField(null=True, blank=True)  # Date when the book was returned

    def __str__(self):
        return f'{self.user} borrowed {self.book}'
