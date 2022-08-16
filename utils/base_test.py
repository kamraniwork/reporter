from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.conf import settings
from utils.constants.base_constants import BaseConstants

User = get_user_model()


class BaseTest(APITestCase):
    """
    Base test case
    """
    client = APIClient

    def setUp(self):
        # for testing send email to user
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

        self.superuser = User.objects.create_superuser(email='mehran@gmail.com',
                                                       password='Mehran1234')

        self.user = User.objects.create_user(email='ali@gmail.com', password='Ali123456')
        self.user.is_active = True
        self.user.save()

        self.user_info_email = {
            BaseConstants.email: "test2@gmail.com",
            BaseConstants.password: "Test1234"
        }
