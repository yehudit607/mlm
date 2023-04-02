from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .pagination import UserPagination
from .schema import UserCreateSchema, UserUpdateSchema
from .serializer import UserSerializer
from .service import UserService
from .exceptions import UserException, user_exception
from ..infra import exceptions
from ..permissions.permissions import IsAdminUser


class UserListCreateView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination

    def get(self, request, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, kwargs["pk"])
        return self.list(request)

    def get_queryset(self):
        user_id = self.kwargs.get("pk", None)
        users = UserService.get(user_id)
        return users

    def retrieve(self, request, user_id):
        user = UserService.get(user_id)
        if not user:
            return JsonResponse({"error": "Not Found"}, status=HTTPStatus.NOT_FOUND)
        return JsonResponse(self.serializer_class(user).data, status=HTTPStatus.OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            user_data = UserCreateSchema(data=request.data)
            if user_data.is_valid(raise_exception=True):
                user = UserService.create_user(user_data.validated_data)
            else:
                raise UserException(
                    f"Schema is not valid with errors: {user_data.errors}",
                    HTTPStatus.BAD_REQUEST,
                )
            return JsonResponse(
                self.serializer_class(user).data,
                status=HTTPStatus.CREATED,
            )

        except UserException as ex:
            return user_exception(ex)
        except Exception as ex:
            return exceptions.general_exception()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            user_id = self.kwargs.get("pk")
            user_data = UserUpdateSchema(data=request.data)
            if user_data.is_valid(raise_exception=True):
                user = UserService.update_user(user_id, user_data.validated_data)
            else:
                raise UserException(
                    f"Schema is not valid with errors: {user_data.errors}",
                    HTTPStatus.BAD_REQUEST,
                )
            return JsonResponse(
                self.serializer_class(user).data,
                status=HTTPStatus.OK,
            )

        except UserException as ex:
            return user_exception(ex)
        except Exception as ex:
            return exceptions.general_exception()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get("pk")
            UserService.delete_user(user_id)
            return JsonResponse(
                {"detail": "User deleted."},
                status=HTTPStatus.NO_CONTENT,
            )

        except UserException as ex:
            return user_exception(ex)
        except Exception as ex:
            return exceptions.general_exception()
