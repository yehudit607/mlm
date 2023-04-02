from http import HTTPStatus
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db.models import Q

from api.infra import exceptions
from api.models.book import Book
from api.books.exceptions import BookException, book_exception


class BookService:

    @classmethod
    def get(cls, book_id: Optional[int] = None, search: Optional[str] = None) -> list[Book]:
        if book_id is not None:
            try:
                return Book.objects.get(pk=book_id)
            except ObjectDoesNotExist:
                raise BookException("Book not found", status_code=HTTPStatus.NOT_FOUND)
        elif search is not None:
            return Book.objects.filter(Q(title__icontains=search) | Q(author__icontains=search))
        else:
            return Book.objects.all()

    @classmethod
    def create_book(cls, data: dict) -> Book:
        try:
            book = Book(title=data.get("title"),
                        author=data.get("author"),
                        publication_year=data.get("publication_year"),
                        total_copies=data.get("total_copies", 1),
                        available_copies=data.get("total_copies", 1),
                        isbn=data.get("isbn"),
                        description=data.get("description")

                        )
            book.save()
        except ValidationError as ex:
            raise BookException(str(ex), HTTPStatus.BAD_REQUEST)
        except Exception as ex:
            raise BookException(str(ex), HTTPStatus.INTERNAL_SERVER_ERROR)

        return book

    @classmethod
    def update_book(cls, book_id: int, data: dict) -> Book:
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise BookException(
                f"book id: {book_id} not found.",
                HTTPStatus.NOT_FOUND,
            )

        try:
            book.title = data.get("title", book.title)
            book.author = data.get("author", book.author)
            book.publication_year = data.get("publication_year", book.publication_year)
            book.total_copies = data.get("total_copies", book.total_copies)
            book.available_copies = data.get("available_copies", book.available_copies)
            book.isbn = data.get("isbn", book.isbn)
            book.description = data.get("description", book.description)

            book.save()
            book.refresh_from_db()
            return book
        except ValidationError as ex:
            raise BookException(str(ex), HTTPStatus.BAD_REQUEST)
        except Exception as ex:
            raise BookException(str(ex), HTTPStatus.INTERNAL_SERVER_ERROR)

    @classmethod
    def delete_book(cls, book_id: int):
        book = Book.objects.filter(id=book_id).first()
        if book:
            book.delete()
        else:
            raise BookException(
                f"book id: {book_id} not found.",
                HTTPStatus.BAD_REQUEST,
            )
