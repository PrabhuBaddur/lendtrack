import sqlite3
from contextlib import contextmanager

conn = sqlite3.connect("library.db")

conn.execute("""
      CREATE TABLE IF NOT EXISTS books(
      book_id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      author TEXT NOT NULL,
      isbn TEXT UNIQUE NOT NULL,
      total_copies INTEGER NOT NULL,
      available_copies INTEGER NOT NULL 
      )
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS members(
   member_id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT NOT NULL,
   email TEXT UNIQUE NOT NULL  
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS transactions(
  transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id INTEGER NOT NULL,
  member_id INTEGER NOT NULL,
  borrowed_at TEXT NOT NULL,
  due_date TEXT NOT NULL,
  returned_at TEXT,
  FOREIGN KEY (book_id) REFERENCES books(book_id),
  FOREIGN KEY (member_id) REFERENCES members(member_id)
)
""")

@contextmanager
def get_connection():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# with get_connection() as conn:
#     conn.execute(
#        "INSERT INTO members(name,email) VALUES(?,?)",
#        ("prab","prabdev@gmail.com")
#     )

# with get_connection() as conn:
#     rows = conn.execute("SELECT * FROM members").fetchall()
#     for row in rows:
#         print(dict(row))

# with get_connection() as conn:
#     conn.execute(
#         "INSERT INTO books (title, author, isbn, total_copies, available_copies) VALUES (?, ?, ?, ?, ?)",
#         ("Clean Code", "Robert Martin", "ISBN001", 2, 2)
#     )

# with get_connection() as conn:
#     conn.execute(
#         "INSERT INTO transactions (book_id, member_id, borrowed_at, due_date) VALUES (?, ?, ?, ?)",
#         (1, 1, "2026-07-19T10:00:00", "2026-08-02T10:00:00")
#     )

def get_active_loans_with_details():
    with get_connection() as conn:
        query = """
        SELECT
            t.transaction_id,
            b.title,
            m.name AS member_name,
            t.due_date
        FROM transactions t
        INNER JOIN books b ON t.book_id = b.book_id
        INNER JOIN members m ON t.member_id = m.member_id
        WHERE t.returned_at IS NULL
    """
        rows = conn.execute(query).fetchall()
        return [dict(row) for row in rows]