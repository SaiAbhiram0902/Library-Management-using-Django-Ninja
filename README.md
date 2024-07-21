# Online Library-Management-using-Django-Ninja

This is a simplified backend for an online library management system built using Django-Ninja. The system allows users to perform various actions such as viewing available books, borrowing books, and returning borrowed books. Additionally, admin users can add, update, and delete books.

## Features

### Admin Actions:
- Add new books to the library.
- Update book details.
- Delete books from the library.
- View all books in the library.

### User Actions:
- View the list of available books.
- Borrow a book.
- Return a borrowed book.

## Requirements

- Python 3.8+
- Django 3.2+
- Django Ninja
- SQLite (default database)
- Other specified in requirements.txt

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/SaiAbhiram0902/Library-Management-using-Django-Ninja.git
    cd Library-Management-using-Django-Ninja
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply the migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the server:**

    ```bash
    python manage.py runserver
    ```

7. **Access the admin panel:**
    - Open your browser and go to `http://127.0.0.1:8000/admin`.
    - Log in using the superuser credentials.

## API Endpoints

### Admin Endpoints:

- **Add a new book:**
    - `POST /api/admin/books/`
- **Update book details:**
    - `PUT /api/admin/books/{id}/`
- **Delete a book:**
    - `DELETE /api/admin/books/{id}/`
- **List all books:**
    - `GET /api/admin/books/`

### User Endpoints:

- **View available books:**
    - `GET /api/books/`
- **Borrow a book:**
    - `POST /api/borrow/`
- **Return a borrowed book:**
    - `POST /api/return/`

## Demo Video

Watch the [demo video](https://drive.google.com/file/d/1C9azizZ867xPdnMi7giDpq31CsK35juI/view?usp=drive_link) demonstrating the setup and usage of the project.

