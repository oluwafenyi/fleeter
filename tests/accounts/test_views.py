
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accounts.models import User


class AccountsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient(format="json")

    def test_account_creation(self):
        data = {
            "username": "johndoe",
            "email": "user@domain.com",
            "password": "StrongPassword1",
            "confirm_password": "StrongPassword1",
            "display_name": "John Doe"
        }
        response = self.client.post(reverse("accounts-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().display_name, "John Doe")

    def test_account_creation_missing_parameter(self):
        data = {
            "username": "johndoe",
            "email": "user@domain.com",
            "password": "StrongPassword1",
            "confirm_password": "StrongPassword1",
            "display_name": "John Doe"
        }
        for key in data:
            copy = data.copy()
            copy.pop(key)
            response = self.client.post(reverse("accounts-list"), data=copy)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(key, response.json())

    def test_account_creation_non_matching_passwords(self):
        data = {
            "username": "johndoe",
            "email": "user@domain.com",
            "password": "StrongPassword1",
            "confirm_password": "StrongPassword2",
            "display_name": "John Doe"
        }
        response = self.client.post(reverse("accounts-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_password", response.json())

    def test_user_follow(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com")
        user_2 = User.objects.create(username="second_user", email="user2@domain.com")
        self.client.force_authenticate(user_1)
        data = {
            "target_user_id": user_2.id
        }
        response = self.client.post(reverse("accounts-following", kwargs={"pk": user_1.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user_1.follows(user_2))

    def test_user_cannot_follow_self(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com")
        self.client.force_authenticate(user_1)
        data = {
            "target_user_id": user_1.id
        }
        response = self.client.post(reverse("accounts-following", kwargs={"pk": user_1.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_1.follows(user_1))

    def test_user_follow_forbidden(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com")
        user_2 = User.objects.create(username="second_user", email="user2@domain.com")
        self.client.force_authenticate(user_2)
        data = {
            "target_user_id": user_2.id
        }
        response = self.client.post(reverse("accounts-following", kwargs={"pk": user_1.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(user_1.follows(user_2))

    def test_user_unfollow(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com")
        user_2 = User.objects.create(username="second_user", email="user2@domain.com")
        user_1.follow_user(user_2)
        self.client.force_authenticate(user_1)
        data = {
            "target_user_id": user_2.id
        }
        response = self.client.delete(reverse("accounts-following", kwargs={"pk": user_1.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(user_1.follows(user_2))

    def test_user_unfollow_forbidden(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com")
        user_2 = User.objects.create(username="second_user", email="user2@domain.com")
        user_1.follow_user(user_2)
        self.client.force_authenticate(user_2)
        data = {
            "target_user_id": user_2.id
        }
        response = self.client.delete(reverse("accounts-following", kwargs={"pk": user_1.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(user_1.follows(user_2))
