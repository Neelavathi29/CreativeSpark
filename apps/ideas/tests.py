from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import StartupIdea, Category, IdeaLike, IdeaBookmark, IdeaComment

User = get_user_model()


class IdeaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="ideauser", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Tech", slug="tech"
        )

    def _make_idea(self, name="TestApp", **kwargs):
        defaults = dict(
            user=self.user,
            startup_name=name,
            founder_name="Tester",
            industry="technology",
            problem_statement="Solving a problem",
            proposed_solution="Our solution",
            target_customers="Everyone",
            business_model="SaaS",
            revenue_model="Subscription",
            competitor_analysis="None",
            unique_selling_proposition="Speed",
            required_investment=50000,
            team_members="Alice, Bob",
            expected_timeline="6 months",
            category=self.category,
        )
        defaults.update(kwargs)
        return StartupIdea.objects.create(**defaults)

    def test_create_startup_idea(self):
        idea = self._make_idea()
        self.assertEqual(str(idea), "TestApp")
        self.assertEqual(idea.status, "draft")
        self.assertEqual(idea.views_count, 0)

    def test_default_values(self):
        idea = self._make_idea("DefaultApp", category=None)
        self.assertEqual(idea.likes_count, 0)
        self.assertEqual(idea.bookmarks_count, 0)


class IdeaViewsTest(TestCase):
    def _make_idea(self, name="TestIdea", **kwargs):
        defaults = dict(
            user=self.user,
            startup_name=name,
            founder_name="Tester",
            industry="technology",
            problem_statement="Problem",
            proposed_solution="Solution",
            target_customers="Market",
            business_model="SaaS",
            revenue_model="Subscription",
            competitor_analysis="None",
            unique_selling_proposition="Speed",
            required_investment=50000,
            team_members="Alice, Bob",
            expected_timeline="6 months",
        )
        defaults.update(kwargs)
        return StartupIdea.objects.create(**defaults)

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="viewuser", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Tech", slug="tech"
        )
        self.idea = self._make_idea()

    def test_idea_list_requires_login(self):
        response = self.client.get(reverse("idea_list"))
        self.assertNotEqual(response.status_code, 200)

    def test_idea_list_authenticated(self):
        self.client.login(username="viewuser", password="testpass123")
        response = self.client.get(reverse("idea_list"))
        self.assertEqual(response.status_code, 200)

    def test_idea_list_pagination(self):
        self.client.login(username="viewuser", password="testpass123")
        for i in range(15):
            self._make_idea(name=f"Idea{i}")
        response = self.client.get(reverse("idea_list"))
        self.assertIn("page_obj", response.context)

    def test_idea_detail(self):
        self.client.login(username="viewuser", password="testpass123")
        response = self.client.get(
            reverse("idea_detail", args=[self.idea.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_idea_detail_increments_view_count(self):
        self.client.login(username="viewuser", password="testpass123")
        self.client.get(reverse("idea_detail", args=[self.idea.pk]))
        self.idea.refresh_from_db()
        self.assertEqual(self.idea.views_count, 1)

    def test_idea_create_get(self):
        self.client.login(username="viewuser", password="testpass123")
        response = self.client.get(reverse("idea_create"))
        self.assertEqual(response.status_code, 200)

    def test_idea_create_post(self):
        self.client.login(username="viewuser", password="testpass123")
        response = self.client.post(
            reverse("idea_create"),
            {
                "startup_name": "NewIdea",
                "founder_name": "Founder",
                "industry": "finance",
                "problem_statement": "A big problem",
                "proposed_solution": "A great solution",
                "target_customers": "Everyone",
                "business_model": "SaaS",
                "revenue_model": "Freemium",
                "competitor_analysis": "None",
                "unique_selling_proposition": "Speed",
                "required_investment": "50000",
                "team_members": "Alice",
                "expected_timeline": "6 months",
                "category": self.category.pk,
            },
        )
        if response.status_code != 302:
            print(response.context["form"].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            StartupIdea.objects.filter(startup_name="NewIdea").exists()
        )

    def test_my_ideas(self):
        self.client.login(username="viewuser", password="testpass123")
        response = self.client.get(reverse("my_ideas"))
        self.assertEqual(response.status_code, 200)

    def test_like_idea(self):
        self.client.login(username="viewuser", password="testpass123")
        response = self.client.get(
            reverse("like_idea", args=[self.idea.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            IdeaLike.objects.filter(
                user=self.user, idea=self.idea
            ).exists()
        )

    def test_bookmark_idea(self):
        self.client.login(username="viewuser", password="testpass123")
        response = self.client.get(
            reverse("bookmark_idea", args=[self.idea.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            IdeaBookmark.objects.filter(
                user=self.user, idea=self.idea
            ).exists()
        )

    def test_add_comment(self):
        self.client.login(username="viewuser", password="testpass123")
        response = self.client.post(
            reverse("add_comment", args=[self.idea.pk]),
            {"content": "Great idea!"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(IdeaComment.objects.count(), 1)
