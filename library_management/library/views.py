import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django import forms
from library.models import Book, Borrow, User

# User registration form
class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# User login form
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# Home page view
def home(request):
    return render(request, 'library/home.html')

# Admin dashboard view (requires login)
@login_required
def admin_dashboard(request):
    books = Book.objects.all()
    return render(request, 'library/admin_dashboard.html', {'books': books})

# User dashboard view (requires login)
@login_required
def user_dashboard(request):
    books = Book.objects.filter(copies__gt=0)
    return render(request, 'library/user_dashboard.html', {'books': books})

# API endpoint to handle books (GET and POST methods)
@csrf_exempt
def api_books(request):
    if request.method == 'GET':
        books = Book.objects.all()
        data = [{'id': book.id, 'title': book.title, 'author': book.author, 'published_date': book.published_date, 'copies': book.copies} for book in books]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        book = Book.objects.create(
            title=data['title'],
            author=data['author'],
            published_date=data['published_date'],
            copies=data['copies']
        )
        return JsonResponse({'id': book.id}, status=201)
    return JsonResponse({'error': 'Invalid method'}, status=405)

# API endpoint to handle book details (PUT and DELETE methods)
@csrf_exempt
def api_book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        book.title = data['title']
        book.author = data['author']
        book.published_date = data['published_date']
        book.copies = data['copies']
        book.save()
        return JsonResponse({'id': book.id})
    elif request.method == 'DELETE':
        book.delete()
        return JsonResponse({'success': True})

# API endpoint to handle borrowing a book (POST method)
@csrf_exempt
def api_borrow_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        if book.copies == 0:
            return JsonResponse({'error': 'No copies available'}, status=400)
        Borrow.objects.create(book=book, user=request.user, borrowed_date=timezone.now())
        book.copies -= 1
        book.save()
        return JsonResponse({'success': True})
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

# API endpoint to handle returning a book (POST method)
@csrf_exempt
def api_return_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        borrow = Borrow.objects.get(book=book, user=request.user, return_date__isnull=True)
        borrow.return_date = timezone.now()
        borrow.save()
        book.copies += 1
        book.save()
        return JsonResponse({'success': True})
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    except Borrow.DoesNotExist:
        return JsonResponse({'error': 'Borrow record not found'}, status=404)

# User login view
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('admin_dashboard') if user.is_staff else redirect('user_dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'library/login.html', {'form': form})

# User registration view
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'library/register.html', {'form': form})

# User logout view
def logout_view(request):
    auth_logout(request)
    return redirect('login')
