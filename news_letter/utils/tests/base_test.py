import random
from typing import List, Optional
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.conf import settings
from news_letter.utils.constants.base_constants import BaseConstants
from .random_user import get_rand_emails, generate_email_name_and_password

User = get_user_model()


class BaseTest(APITestCase):
    """
    Base test case
    """
    client = APIClient

    def setUp(self):
        # for testing send email to user
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

        self.superuser: User = User.objects.create_superuser(email='mehran@gmail.com',
                                                             password='Mehran1234')

        self.user: User = User.objects.create_user(email='ali@gmail.com', password='Ali123456', is_active=True)

        randemail: List[str] = get_rand_emails(no_of_emails=1, length=10)
        self.user_info_email = {
            BaseConstants.email: randemail[0],
            BaseConstants.password: generate_email_name_and_password(10)
        }
