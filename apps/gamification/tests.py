from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Badge, UserBadge, UserXP, Challenge, UserChallenge

User = get_user_model()


class GamificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="gamuser", password="testpass123"
        )

    def test_create_badge(self):
        badge = Badge.objects.create(
            name="First Idea",
            slug="first-idea",
            description="Submit your first idea",
            badge_type="idea",
            xp_required=100,
        )
        self.assertEqual(str(badge), "First Idea")

    def test_user_badge(self):
        badge = Badge.objects.create(
            name="Pioneer", slug="pioneer",
            description="First milestone",
            badge_type="milestone",
        )
        ub = UserBadge.objects.create(
            user=self.user, badge=badge
        )
        self.assertEqual(
            str(ub), f"gamuser - Pioneer"
        )

    def test_user_xp_create(self):
        xp = UserXP.objects.create(user=self.user)
        self.assertEqual(str(xp), "gamuser - Level 1 (0 XP)")
        self.assertEqual(xp.level, 1)
        self.assertEqual(xp.total_xp, 0)

    def test_user_xp_add_xp(self):
        xp = UserXP.objects.create(user=self.user)
        xp.add_xp(250)
        self.assertEqual(xp.total_xp, 250)
        self.assertEqual(xp.level, 3)  # 250 // 100 + 1 = 3

    def test_create_challenge(self):
        challenge = Challenge.objects.create(
            title="30 Day Coding",
            description="Code every day",
            xp_reward=200,
            start_date="2026-01-01",
            end_date="2026-01-31",
        )
        self.assertEqual(str(challenge), "30 Day Coding")

    def test_user_challenge(self):
        challenge = Challenge.objects.create(
            title="Test Challenge",
            description="Do something",
            xp_reward=50,
            start_date="2026-01-01",
            end_date="2026-01-31",
        )
        uc = UserChallenge.objects.create(
            user=self.user, challenge=challenge
        )
        self.assertEqual(
            str(uc), "gamuser - Test Challenge"
        )
        self.assertFalse(uc.completed)


class GamificationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="gamview", password="testpass123"
        )
        UserXP.objects.create(user=self.user)

    def test_leaderboard_requires_login(self):
        response = self.client.get(reverse("leaderboard"))
        self.assertNotEqual(response.status_code, 200)

    def test_leaderboard_authenticated(self):
        self.client.login(
            username="gamview", password="testpass123"
        )
        response = self.client.get(reverse("leaderboard"))
        self.assertEqual(response.status_code, 200)

    def test_badges_view(self):
        self.client.login(
            username="gamview", password="testpass123"
        )
        response = self.client.get(reverse("badges"))
        self.assertEqual(response.status_code, 200)

    def test_challenge_list(self):
        self.client.login(
            username="gamview", password="testpass123"
        )
        response = self.client.get(reverse("challenge_list"))
        self.assertEqual(response.status_code, 200)

    def test_hall_of_fame(self):
        response = self.client.get(reverse("hall_of_fame"))
        self.assertEqual(response.status_code, 200)

    def test_join_challenge(self):
        self.client.login(
            username="gamview", password="testpass123"
        )
        challenge = Challenge.objects.create(
            title="Join Test",
            description="Test",
            xp_reward=10,
            start_date="2026-01-01",
            end_date="2026-12-31",
        )
        response = self.client.get(
            reverse("join_challenge", args=[challenge.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            UserChallenge.objects.filter(
                user=self.user, challenge=challenge
            ).exists()
        )

    def test_complete_challenge(self):
        self.client.login(
            username="gamview", password="testpass123"
        )
        challenge = Challenge.objects.create(
            title="Complete Test",
            description="Test",
            xp_reward=10,
            start_date="2026-01-01",
            end_date="2026-12-31",
        )
        uc = UserChallenge.objects.create(
            user=self.user, challenge=challenge
        )
        response = self.client.get(
            reverse("complete_challenge", args=[challenge.pk])
        )
        self.assertEqual(response.status_code, 302)
        uc.refresh_from_db()
        self.assertTrue(uc.completed)
