from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database import get_connection, get_active_loans_with_details
from services import (
    merge_sort, binary_search, stream_overdue_loans,
    most_borrowed_books, loans_grouped_by_member
)
from exceptions import (
    LibraryException, BookNotFoundError, MemberNotFoundError,
    BookNotAvailableError
)

app = FastAPI(title="Library Management System")


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    total_copies: int = 1


class MemberCreate(BaseModel):
    name: str
    email: str


class BorrowRequest(BaseModel):
    book_id: int
    member_id: int


EXCEPTION_STATUS_MAP = {
    BookNotFoundError: 404,
    MemberNotFoundError: 404,
    BookNotAvailableError: 409,
}


@app.exception_handler(LibraryException)
def library_exception_handler(request, exc: LibraryException):
    status_code = EXCEPTION_STATUS_MAP.get(type(exc), 400)
    return JSONResponse(status_code=status_code, content={"error": str(exc)})


@app.post("/books")
def create_book(payload: BookCreate):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO books (title, author, isbn, total_copies, available_copies) VALUES (?, ?, ?, ?, ?)",
            (payload.title, payload.author, payload.isbn, payload.total_copies, payload.total_copies)
        )
        row = conn.execute("SELECT * FROM books WHERE book_id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)


@app.get("/books")
def list_books():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM books").fetchall()
        books = [dict(row) for row in rows]
    return merge_sort(books)


@app.post("/members")
def create_member(payload: MemberCreate):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO members (name, email) VALUES (?, ?)",
            (payload.name, payload.email)
        )
        row = conn.execute("SELECT * FROM members WHERE member_id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)


@app.post("/loans/borrow")
def borrow(payload: BorrowRequest):
    with get_connection() as conn:
        book = conn.execute("SELECT * FROM books WHERE book_id = ?", (payload.book_id,)).fetchone()
        if not book:
            raise BookNotFoundError(payload.book_id)
        if book["available_copies"] <= 0:
            raise BookNotAvailableError(payload.book_id)

        member = conn.execute("SELECT * FROM members WHERE member_id = ?", (payload.member_id,)).fetchone()
        if not member:
            raise MemberNotFoundError(payload.member_id)

        from datetime import datetime, timedelta
        now = datetime.utcnow()
        due = now + timedelta(days=14)

        cur = conn.execute(
            "INSERT INTO transactions (book_id, member_id, borrowed_at, due_date) VALUES (?, ?, ?, ?)",
            (payload.book_id, payload.member_id, now.isoformat(), due.isoformat())
        )
        conn.execute(
            "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = ?",
            (payload.book_id,)
        )
        row = conn.execute("SELECT * FROM transactions WHERE transaction_id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)


@app.get("/loans/active")
def active_loans():
    return get_active_loans_with_details()


@app.get("/loans/overdue")
def overdue_loans():
    return list(stream_overdue_loans())


@app.get("/reports/most-borrowed")
def most_borrowed(top_n: int = 5):
    return most_borrowed_books(top_n)


@app.get("/reports/loans-by-member")
def loans_by_member():
    return loans_grouped_by_member()


@app.get("/")
def root():
    return {"message": "Library API running. See /docs"}