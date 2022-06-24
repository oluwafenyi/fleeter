
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accounts.models import User
from posts.models import Post


class PostsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient(format="json")

    def test_post_creation(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com", display_name="John Doe")
        self.client.force_authenticate(user_1)

        data = {
            "text": "Hello World",
            "image": open(settings.BASE_DIR / "tests" / "data" / "wallhaven-4xj6eo.png", "rb")
        }
        response = self.client.post(reverse("posts-list"), data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Post.objects.count())

    def test_post_creation_no_data(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com", display_name="John Doe")
        self.client.force_authenticate(user_1)

        data = {}
        response = self.client.post(reverse("posts-list"), data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, Post.objects.count())

    def test_post_creation_either_text_or_image(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com", display_name="John Doe")
        self.client.force_authenticate(user_1)

        data = {
            "text": "Hello World",
            "image": open(settings.BASE_DIR / "tests" / "data" / "wallhaven-4xj6eo.png", "rb")
        }
        for key in data:
            response = self.client.post(reverse("posts-list"), data={key: data[key]}, format="multipart")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_does_not_exist(self):
        response = self.client.get(reverse("posts-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_successful(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com", display_name="John Doe")
        post_text = "Hello"
        Post.objects.create(text=post_text, creator=user_1)
        response = self.client.get(reverse("posts-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["text"], post_text)

    def test_delete_post_successful(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com", display_name="John Doe")
        Post.objects.create(text="Hello", creator=user_1)
        self.client.force_authenticate(user_1)
        response = self.client.delete(reverse("posts-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_delete_post_forbidden(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com", display_name="John Doe")
        user_2 = User.objects.create(username="second_user", email="user2@domain.com", display_name="Jane Doe")
        Post.objects.create(text="Hello", creator=user_1)
        self.client.force_authenticate(user_2)
        response = self.client.delete(reverse("posts-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post_unauthorized(self):
        user_1 = User.objects.create(username="first_user", email="user1@domain.com", display_name="John Doe")
        Post.objects.create(text="Hello", creator=user_1)
        response = self.client.delete(reverse("posts-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 1)
