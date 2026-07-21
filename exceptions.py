class LibraryException(Exception):
    """Base class for all library-related errors."""
    pass


class BookNotFoundError(LibraryException):
    def __init__(self, book_id: int):
        self.book_id = book_id
        super().__init__(f"Book with id {book_id} not found.")

class MemberNotFoundError(LibraryException):
    def __init__(self,member_id: int):
        self.member_id = member_id
        super().__init__(f"Member with id {member_id} not found.")

class BookNotAvailableError(LibraryException):
    def __init__(self, book_id: int):
        self.book_id = book_id
        super().__init__(f"Book with id {book_id} has no copy Avaliable.")