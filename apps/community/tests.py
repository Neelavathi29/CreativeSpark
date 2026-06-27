from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import (
    UserFollow, ChatRoom, ChatMessage,
    SuccessStory, StartupShowcase,
)
from apps.ideas.models import StartupIdea, Category

User = get_user_model()


class CommunityModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="testpass123"
        )

    def test_user_follow(self):
        follow = UserFollow.objects.create(
            follower=self.user1, following=self.user2
        )
        self.assertEqual(
            str(follow), "user1 follows user2"
        )

    def test_chat_room(self):
        room = ChatRoom.objects.create(name="Test Room")
        room.participants.add(self.user1, self.user2)
        self.assertEqual(str(room), "Test Room")

    def test_chat_message(self):
        room = ChatRoom.objects.create()
        room.participants.add(self.user1)
        msg = ChatMessage.objects.create(
            room=room, sender=self.user1, content="Hello"
        )
        self.assertTrue("user1: Hello" in str(msg))

    def test_success_story(self):
        story = SuccessStory.objects.create(
            user=self.user1,
            title="My Journey",
            content="How I succeeded",
            achievement="Raised funding",
        )
        self.assertEqual(str(story), "My Journey")
        self.assertFalse(story.is_approved)

    def test_startup_showcase(self):
        idea = StartupIdea.objects.create(
            user=self.user1,
            startup_name="ShowcaseApp",
            founder_name="Tester",
            industry="technology",
            problem_statement="P",
            proposed_solution="S",
            target_customers="M",
            business_model="SaaS",
            revenue_model="Sub",
            competitor_analysis="N",
            unique_selling_proposition="X",
            required_investment=10000,
            team_members="A",
            expected_timeline="3m",
        )
        showcase = StartupShowcase.objects.create(idea=idea)
        self.assertEqual(
            str(showcase), "Showcase: ShowcaseApp"
        )


class CommunityViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="comuser", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="otheruser", password="testpass123"
        )

    def test_showcase(self):
        response = self.client.get(reverse("showcase"))
        self.assertEqual(response.status_code, 200)

    def test_success_stories(self):
        response = self.client.get(reverse("success_stories"))
        self.assertEqual(response.status_code, 200)

    def test_public_profile(self):
        response = self.client.get(
            reverse("public_profile", args=[self.user.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_follow_user_login_required(self):
        response = self.client.get(
            reverse("follow_user", args=[self.user2.pk])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_follow_user(self):
        self.client.login(username="comuser", password="testpass123")
        response = self.client.get(
            reverse("follow_user", args=[self.user2.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            UserFollow.objects.filter(
                follower=self.user, following=self.user2
            ).exists()
        )

    def test_chat_rooms_login_required(self):
        response = self.client.get(reverse("chat_rooms"))
        self.assertNotEqual(response.status_code, 200)

    def test_chat_rooms(self):
        self.client.login(username="comuser", password="testpass123")
        response = self.client.get(reverse("chat_rooms"))
        self.assertEqual(response.status_code, 200)

    def test_start_chat(self):
        self.client.login(username="comuser", password="testpass123")
        response = self.client.get(
            reverse("start_chat", args=[self.user2.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ChatRoom.objects.count(), 1)
