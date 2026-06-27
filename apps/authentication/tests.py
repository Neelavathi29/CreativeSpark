from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .security_models import TwoFactorAuth, LoginActivity

User = get_user_model()


class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

    def test_register_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authentication/register.html")

    def test_register_post(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "role": "student",
                "password1": "VeryStrongP@ss123",
                "password2": "VeryStrongP@ss123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_post_success(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, 302)

    def test_login_post_fail(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertNotEqual(response.status_code, 200)

    def test_profile_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("edit_profile"),
            {
                "username": "testuser",
                "email": "updated@example.com",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")


class TwoFactorAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="2fauser", password="testpass123"
        )
        self.client.login(username="2fauser", password="testpass123")

    def test_security_settings_view(self):
        response = self.client.get(reverse("security_settings"))
        self.assertEqual(response.status_code, 200)

    def test_toggle_2fa_on(self):
        response = self.client.get(reverse("toggle_two_factor"))
        self.assertEqual(response.status_code, 302)
        tfa = TwoFactorAuth.objects.get(user=self.user)
        self.assertTrue(tfa.is_enabled)
        self.assertIsNotNone(tfa.secret_key)

    def test_toggle_2fa_off(self):
        TwoFactorAuth.objects.create(
            user=self.user, is_enabled=True, secret_key="test"
        )
        response = self.client.get(reverse("toggle_two_factor"))
        self.assertEqual(response.status_code, 302)
        tfa = TwoFactorAuth.objects.get(user=self.user)
        self.assertFalse(tfa.is_enabled)

    def test_login_redirect_to_2fa_when_enabled(self):
        TwoFactorAuth.objects.create(
            user=self.user, is_enabled=True, secret_key="test"
        )
        self.client.logout()
        response = self.client.post(
            reverse("login"),
            {"username": "2fauser", "password": "testpass123"},
        )
        self.assertIn("2fa_user_id", self.client.session)


class LoginActivityTest(TestCase):
    def test_create_login_activity(self):
        user = User.objects.create_user(
            username="loguser", password="testpass123"
        )
        activity = LoginActivity.objects.create(
            user=user, ip_address="127.0.0.1", is_successful=True
        )
        self.assertEqual(
            str(activity),
            f"loguser - 127.0.0.1 - Success",
        )
