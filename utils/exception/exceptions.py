from rest_framework import status
from rest_framework.exceptions import APIException, NotFound, PermissionDenied, NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, NotFound) \
            or isinstance(exc, PermissionDenied) \
            or isinstance(exc, NotAcceptable) \
            or isinstance(exc, ValidationError):
        response.data = {
            "error": exc.detail,  # custom exception message
        }

    # Raw data not exist error should be sent on "message" key.
    elif isinstance(exc, DoesNotExistError):
        response.data = {
            "status": exc.status_code,
            "detail": exc.detail,
            "code": exc.default_code
        }

    # Elasticsearch Index Not Found
    elif isinstance(exc, AccessDeniedUser):
        response = Response(status=status.HTTP_403_FORBIDDEN)
        response.data = {
            "status": exc.status_code,
            "detail": exc.detail,
            "code": exc.default_code
        }

    return response


class DoesNotExistError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "bad request. dose not exist data"
    default_code = "error"


class AccessDeniedUser(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "this email register before"
    default_code = "error"
