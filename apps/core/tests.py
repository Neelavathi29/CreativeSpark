from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Notification, ContactMessage, VisitorCounter

User = get_user_model()


class CoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    def test_about_view(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_get(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_post(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Test",
                "email": "a@b.com",
                "subject": "Hello",
                "message": "Hi",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_faq_view(self):
        response = self.client.get(reverse("faq"))
        self.assertEqual(response.status_code, 200)

    def test_activity_log_requires_login(self):
        response = self.client.get(reverse("activity_log"))
        self.assertNotEqual(response.status_code, 200)

    def test_activity_log_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("activity_log"))
        self.assertEqual(response.status_code, 200)

    def test_mark_notification_read(self):
        self.client.login(username="testuser", password="testpass123")
        notif = Notification.objects.create(
            user=self.user, title="Test", message="Test"
        )
        response = self.client.get(
            reverse("mark_notification_read", args=[notif.pk])
        )
        self.assertEqual(response.status_code, 302)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)

    def test_mark_all_notifications_read(self):
        self.client.login(username="testuser", password="testpass123")
        Notification.objects.create(user=self.user, title="N1", message="M1")
        Notification.objects.create(user=self.user, title="N2", message="M2")
        response = self.client.get(reverse("mark_all_notifications_read"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Notification.objects.filter(is_read=False).count(), 0
        )

    def test_visitor_counter(self):
        count_before = VisitorCounter.objects.count()
        self.client.get(reverse("home"))
        self.assertEqual(VisitorCounter.objects.count(), count_before + 1)


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="notifuser", password="testpass123"
        )

    def test_create_notification(self):
        notif = Notification.objects.create(
            user=self.user,
            title="Test Title",
            message="Test Message",
            notification_type="success",
        )
        self.assertEqual(str(notif), f"{self.user.username} - Test Title")
        self.assertFalse(notif.is_read)

    def test_default_values(self):
        notif = Notification.objects.create(
            user=self.user, title="Default", message="Check"
        )
        self.assertEqual(notif.notification_type, "info")
        self.assertIsNone(notif.link)


class ContactMessageModelTest(TestCase):
    def test_create_contact_message(self):
        msg = ContactMessage.objects.create(
            name="Alice", email="alice@test.com", subject="Hi", message="Hello"
        )
        self.assertEqual(str(msg), "Alice - Hi")
