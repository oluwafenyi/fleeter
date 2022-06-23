
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase

from accounts.models import User


class AccountsModelsTest(APITestCase):
    def test_user_creation_exception_on_non_unique_email(self):
        User.objects.create(email="user@domain.com", username="johndoe")
        self.assertRaises(IntegrityError, User.objects.create, email="user@domain.com", username="john")

    def test_user_creation_exception_on_non_unique_username(self):
        User.objects.create(email="user@domain.com", username="johndoe")
        self.assertRaises(IntegrityError, User.objects.create, email="usertwo@domain.com", username="johndoe")
