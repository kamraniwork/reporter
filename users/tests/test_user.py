from news_letter.utils.tests.base_test import BaseTest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from django.core import mail
from news_letter.utils.tests.random_user import get_rand_emails
from news_letter.utils.constants.user_constants import UserConstants

User = get_user_model()


class UserTest(BaseTest):

    def test_register_user_by_email(self):
        """ Test for register user with email and check is_active field """

        response = self.client.post(reverse('auth:register-register-email'), data=self.user_info_email)

        user: User = User.objects.get(email=self.user_info_email[UserConstants.email])
        self.assertTrue(user.is_active)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_error_user_by_email(self):
        """ Test error for register user with email when email is repetitious """
        self.user_info_email[UserConstants.email] = "ali@gmail.com"
        response = self.client.post(reverse('auth:register-register-email'), data=self.user_info_email)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_user_custom_email(self):
        """ Test register user if email is uppercase """
        randemail = get_rand_emails(no_of_emails=1, length=10)
        self.user_info_email[UserConstants.email] = randemail[0]
        response = self.client.post(reverse('auth:register-register-email'), data=self.user_info_email)

        user = User.objects.get(email=randemail[0].lower())
        self.assertEqual(user.email, randemail[0].lower())
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
