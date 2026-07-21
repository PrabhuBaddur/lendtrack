# Lendtrack 📚

A backend Library Management System built with Python and FastAPI. This project demonstrates core backend engineering principles, including custom database context management, object-oriented programming (OOP), and practical implementations of Data Structures and Algorithms (DSA).

## Core Technical Features
* **RESTful API architecture:** Built with FastAPI and Pydantic for strict data validation and automated documentation.
* **Database Engineering:** Uses raw SQLite3 queries wrapped in a custom `@contextmanager` to ensure safe database connections, commits, and error rollbacks.
* **Applied DSA:** Implements custom `merge_sort` and `binary_search` algorithms in Python for data processing.
* **Memory-Efficient Processing:** Utilizes Python generators (`yield`) to stream overdue loans, optimizing memory usage.
* **Object-Oriented Design (OOP):** Demonstrates class inheritance (`member` extending `Person`), encapsulation via `@property` decorators, and custom dunder methods (`__eq__`, `__hash__`).
* **Jinja2 Web Dashboard:** Includes a clean, read-only frontend UI to view real-time book inventory.

## Tech Stack
* **Language:** Python
* **Framework:** FastAPI
* **Database:** SQLite
* **Templating:** Jinja2
* **Server:** Uvicorn

## How to Run Locally

1. **Install Dependencies:**
   ```bash
   pip install fastapi uvicorn pydantic jinja2
   ```

2. **Start the Server:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the Application:**
   * **API Documentation (Swagger UI):** http://127.0.0.1:8000/docs
   * **Inventory Dashboard:** http://127.0.0.1:8000/ui

## Key API Endpoints
* `GET /books` - List all books (Sorted via custom Merge Sort)
* `POST /books` - Add a new book to the inventory
* `POST /members` - Register a new library member
* `POST /loans/borrow` - Process a book borrowing transaction
* `GET /loans/active` - View currently active loans via SQL INNER JOINs
* `GET /loans/overdue` - View overdue loans
* `GET /reports/most-borrowed` - View top borrowed books using Python's `collections.Counter`

---
**Author:** Prabhudev M Baddur
