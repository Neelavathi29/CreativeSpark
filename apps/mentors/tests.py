from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import MentorProfile, MentorshipSession, Discussion, DiscussionReply

User = get_user_model()


class MentorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="mentoruser",
            password="testpass123",
            role="mentor",
        )
        self.student = User.objects.create_user(
            username="studentuser",
            password="testpass123",
            role="student",
        )

    def test_create_mentor_profile(self):
        profile = MentorProfile.objects.create(
            user=self.user,
            expertise="Python, Django",
            bio="Experienced developer",
            available=True,
        )
        self.assertTrue(
            "Mentor:" in str(profile)
            and self.user.username in str(profile)
        )
        self.assertTrue(profile.available)

    def test_create_mentorship_session(self):
        mentor = MentorProfile.objects.create(
            user=self.user, expertise="Python", bio="Dev"
        )
        session = MentorshipSession.objects.create(
            mentor=mentor,
            student=self.student,
            topic="Django ORM",
            preferred_date="2026-07-01",
            preferred_time="10:00:00",
            status="pending",
        )
        self.assertTrue(
            self.student.username in str(session)
            and self.user.username in str(session)
        )

    def test_create_discussion(self):
        mentor = MentorProfile.objects.create(
            user=self.user, expertise="Python", bio="Dev"
        )
        discussion = Discussion.objects.create(
            mentor=mentor,
            user=self.student,
            title="How to scale?",
            content="Need advice on scaling.",
        )
        self.assertEqual(str(discussion), "How to scale?")

    def test_create_discussion_reply(self):
        mentor = MentorProfile.objects.create(
            user=self.user, expertise="Python", bio="Dev"
        )
        discussion = Discussion.objects.create(
            mentor=mentor, user=self.student, title="Help", content="Help me"
        )
        reply = DiscussionReply.objects.create(
            discussion=discussion,
            user=self.user,
            content="Sure, here's how.",
        )
        self.assertEqual(str(reply), f"Reply by {self.user.username}")


class MentorViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="mentorview",
            password="testpass123",
            role="mentor",
        )
        self.student = User.objects.create_user(
            username="studentview",
            password="testpass123",
            role="student",
        )
        self.profile = MentorProfile.objects.create(
            user=self.user, expertise="Python", bio="Bio", available=True
        )

    def test_mentor_list(self):
        response = self.client.get(reverse("mentor_list"))
        self.assertEqual(response.status_code, 200)

    def test_mentor_detail(self):
        response = self.client.get(
            reverse("mentor_detail", args=[self.profile.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_book_session_get(self):
        self.client.login(username="studentview", password="testpass123")
        response = self.client.get(
            reverse("book_session", args=[self.profile.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_book_session_post(self):
        self.client.login(username="studentview", password="testpass123")
        response = self.client.post(
            reverse("book_session", args=[self.profile.pk]),
            {
                "topic": "Django",
                "preferred_date": "2026-07-15",
                "preferred_time": "14:00:00",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MentorshipSession.objects.count(), 1)

    def test_my_sessions_student(self):
        self.client.login(username="studentview", password="testpass123")
        response = self.client.get(reverse("my_sessions"))
        self.assertEqual(response.status_code, 200)

    def test_my_sessions_mentor(self):
        self.client.login(username="mentorview", password="testpass123")
        response = self.client.get(reverse("my_sessions"))
        self.assertEqual(response.status_code, 200)

    def test_create_discussion(self):
        self.client.login(username="studentview", password="testpass123")
        response = self.client.post(
            reverse("create_discussion", args=[self.profile.pk]),
            {
                "title": "Test Question",
                "content": "Need help with Django",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Discussion.objects.count(), 1)

    def test_discussion_detail(self):
        self.client.login(username="studentview", password="testpass123")
        discussion = Discussion.objects.create(
            mentor=self.profile,
            user=self.student,
            title="Q",
            content="Question",
        )
        response = self.client.get(
            reverse("discussion_detail", args=[discussion.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_submit_feedback(self):
        self.client.login(username="studentview", password="testpass123")
        session = MentorshipSession.objects.create(
            mentor=self.profile,
            student=self.student,
            topic="Test",
            preferred_date="2026-07-01",
            preferred_time="10:00:00",
            status="completed",
        )
        response = self.client.post(
            reverse("submit_feedback", args=[session.pk]),
            {"feedback": "Great session!", "rating": "5"},
        )
        self.assertEqual(response.status_code, 302)
        session.refresh_from_db()
        self.assertEqual(session.feedback, "Great session!")
        self.assertEqual(session.rating, 5)
