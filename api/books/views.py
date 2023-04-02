from http import HTTPStatus

from django.http import JsonResponse
from rest_framework import generics, mixins
from .exceptions import BookException, book_exception
from .pagination import BookPagination
from .schema import BookCreateSchema, BookUpdateSchema
from .serializer import BookSerializer
from .service import BookService
from api.infra import exceptions
from ..permissions.permissions import IsAdminUserOrReadOnly


class BookListCreateView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BookSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = BookPagination

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, kwargs["pk"])
        return self.list(request)

    def get_queryset(self):
        book_id = self.kwargs.get("pk", None)
        search = self.request.query_params.get("search", None)
        books = BookService.get(book_id, search)
        return books

    def retrieve(self, request, book_id):
        book = BookService.get(book_id)
        if not book:
            return JsonResponse({"error": "Not Found"}, status=404)
        return JsonResponse(self.serializer_class(book).data, status=200)

    def post(self, *args, **kwargs):
        try:
            book_data = BookCreateSchema(data=self.request.data)
            if book_data.is_valid(raise_exception=True):
                book = BookService.create_book(book_data.validated_data)
            else:
                raise BookException(
                    f"Schema is not valid with errors: {book_data.errors}",
                    HTTPStatus.BAD_REQUEST,
                )
            return JsonResponse(
                self.serializer_class(book).data,
                status=HTTPStatus.CREATED,
                safe=False,
            )

        except BookException as ex:
            return book_exception(ex)
        except Exception as ex:
            return exceptions.general_exception()

    def delete(self, request, *args, **kwargs):
        try:
            book_id = kwargs.get("pk")
            BookService.delete_book(book_id)
            return JsonResponse(
                {"detail": "Book deleted."},
                status=HTTPStatus.NO_CONTENT,
                safe=False,
            )

        except BookException as ex:
            return book_exception(ex)
        except Exception as ex:
            return exceptions.general_exception()

    def put(self, request, *args, **kwargs):
        try:
            book_id = self.kwargs.get("pk")
            book_data = BookUpdateSchema(data=self.request.data)
            if book_data.is_valid(raise_exception=True):
                book = BookService.update_book(book_id, book_data.validated_data)
            else:
                raise BookException(
                    f"Schema is not valid with errors: {book_data.errors}",
                    HTTPStatus.BAD_REQUEST,
                )
            return JsonResponse(
                self.serializer_class(book).data,
                status=HTTPStatus.OK,
            )

        except BookException as ex:
            return book_exception
