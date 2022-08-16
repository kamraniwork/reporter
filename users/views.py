import json
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    RegisterEmailSerializer
)
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from .tasks import send_email_confirm
from django.contrib.auth import get_user_model
from .transactions import set_user_password
from utils.exception.exceptions import AccessDeniedUser, DoesNotExistError
from utils.constants.base_constants import BaseConstants
from datetime import datetime

User = get_user_model()


class RegisterUser(ViewSet):
    """
    Register user with email and send welcome email
    """

    @action(detail=False, methods=[BaseConstants.post], name=BaseConstants.register_name_action)
    def register_email(self, request):
        """
        register user by email and send welcome email
        """

        serializer = RegisterEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data[BaseConstants.email].lower()
            password = serializer.data[BaseConstants.password]
            try:
                user = User.objects.get(email=email)
                if user is not None and user.is_active:
                    raise AccessDeniedUser
            except User.DoesNotExist:
                user = User.objects.create_user(email=email, password=password)
            set_user_password(user=user, password=password)
            send_email_confirm.delay(email)
            return Response(status=status.HTTP_201_CREATED)
        else:
            DoesNotExistError.default_detail = serializer.errors
            raise DoesNotExistError

    @action(detail=False, methods=[BaseConstants.post], name=BaseConstants.news_name_action)
    def news_email(self, request):
        serializer = RegisterEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data[BaseConstants.email].lower()
            password = serializer.data[BaseConstants.password]
            try:
                user = User.objects.get(email=email)
                if user is not None and user.is_active and user.check_password(password):
                    self._create_signaler_task(email)
                else:
                    raise DoesNotExistError
            except User.DoesNotExist:
                raise DoesNotExistError

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            DoesNotExistError.default_detail = serializer.errors
            raise DoesNotExistError

    @staticmethod
    def _create_signaler_task(email):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.SECONDS)

        PeriodicTask.objects.create(
            interval=schedule,
            name='Sending Signals {}'.format(datetime.now()),
            task='users.tasks.send_email_news',
            kwargs=json.dumps({
                BaseConstants.email: email
            })
        )
