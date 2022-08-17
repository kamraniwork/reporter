from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers.users import (
    RegisterEmailSerializer,
    NewsReporterEmailSerializer
)

from django.contrib.auth import get_user_model
from news_letter.utils.exceptions.exceptions import AccessDeniedUser, DoesNotExistError
from news_letter.utils.constants.base_constants import BaseConstants
from news_letter.utils.constants.user_constants import UserConstants

User = get_user_model()


class RegisterUser(ViewSet):
    """
    Register user with email and send welcome email
    """

    @action(detail=False, methods=[BaseConstants.post], name=UserConstants.register_name_action)
    def register_email(self, request):
        """
        register user by email and send welcome email
        """
        serializer = RegisterEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            DoesNotExistError.default_detail = serializer.errors
            raise DoesNotExistError

    @action(detail=False, methods=[BaseConstants.post], name=UserConstants.news_name_action)
    def news_email(self, request):
        serializer = NewsReporterEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            DoesNotExistError.default_detail = serializer.errors
            raise DoesNotExistError
