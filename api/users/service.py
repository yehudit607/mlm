from http import HTTPStatus
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password

from api.infra import exceptions
from api.models.user import User, create_username
from api.users.exceptions import UserException, user_exception
from django.core.exceptions import ValidationError


class UserService:

    @classmethod
    def get(cls, user_id: Optional[int] = None) -> list[User]:
        if user_id is None:
            return User.objects.all()
        else:
            try:
                return User.objects.get(pk=user_id)
            except ObjectDoesNotExist:
                raise UserException("User not found", status_code=HTTPStatus.NOT_FOUND)

    @classmethod
    def create_user(cls, data: dict) -> User:
        try:
            password = make_password(data.get("password"))
            user = User(username=create_username(data.get("email").lower()),
                        password=password,
                        email=data.get("email").lower(),
                        is_admin=data.get("is_admin", False),
                        first_name=data.get("first_name"),
                        last_name=data.get("last_name")
                        )
            user.save()
        except ValidationError as ex:
            raise UserException(str(ex), HTTPStatus.BAD_REQUEST)
        except Exception as ex:
            raise UserException(str(ex), HTTPStatus.INTERNAL_SERVER_ERROR)

        return user

    @classmethod
    def update_user(cls, user_id: int, data: dict) -> User:
        user = User.objects.get(id=user_id)
        if user:
            try:
                user.username = data.get("user_name", user.username)
                user.password = data.get("password", user.password)
                user.is_admin = data.get("is_admin", user.is_admin)
                user.first_name = data.get("first_name", user.first_name)
                user.last_name = data.get("last_name", user.last_name)
                user.save()
                return user
            except ValidationError as ex:
                raise UserException(str(ex), HTTPStatus.BAD_REQUEST)
            except Exception as ex:
                raise UserException(str(ex), HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            raise UserException(
                f"user id: {user_id} not found.",
                HTTPStatus.NOT_FOUND,
            )

    @classmethod
    def delete_user(cls, user_id: int):
        user = User.objects.filter(id=user_id).first()
        if user:
            user.delete()
        else:
            raise UserException(
                f"user id: {user_id} not found.",
                HTTPStatus.BAD_REQUEST,
            )
