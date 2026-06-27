from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class DashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="dashuser", password="testpass123"
        )

    def test_home_requires_login(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertNotEqual(response.status_code, 200)

    def test_home_authenticated(self):
        self.client.login(username="dashuser", password="testpass123")
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/home.html")
