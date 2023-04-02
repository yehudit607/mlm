from django.http import JsonResponse


class UserException(ValueError):
    status_code: int
    message: str

    def __init__(self, message=None, status_code=None, *args):
        self.message = message
        self.status_code = status_code
        super(UserException, self).__init__(*args)


def user_exception(ex):
    return JsonResponse(
        {"Message": ex.message, "Status": ex.status_code},
        status=ex.status_code,
        safe=False,
    )
