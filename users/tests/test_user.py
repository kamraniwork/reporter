from utils.base_test import BaseTest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from django.core import mail
from utils.constants.base_constants import BaseConstants

User = get_user_model()


class UserTest(BaseTest):

    def test_register_user_by_email(self):
        """ Test for register user with email and check is_active field """

        response = self.client.post(reverse("auth:register-register-email"), data=self.user_info_email)

        user = User.objects.get(email=self.user_info_email[BaseConstants.email])
        self.assertTrue(user.is_active)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_error_user_by_email(self):
        """ Test error for register user with email when email is repetitious """
        self.user_info_email[BaseConstants.email] = "ali@gmail.com"
        response = self.client.post(reverse("auth:register-register-email"), data=self.user_info_email)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_user_custom_email(self):
        """ Test register user if email is uppercase """

        self.user_info_email['email'] = 'TEST@GMAIL.com'
        response = self.client.post(reverse("auth:register-register-email"), data=self.user_info_email)

        user = User.objects.get(email='test@gmail.com')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
