from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Investor, FundingApplication, Incubator
from apps.ideas.models import StartupIdea

User = get_user_model()


class FundingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="funduser", password="testpass123"
        )

    def test_create_investor(self):
        inv = Investor.objects.create(
            name="Seed Fund",
            investor_type="seed",
            description="Early stage fund",
            min_investment=10000,
            max_investment=500000,
        )
        self.assertEqual(str(inv), "Seed Fund")

    def test_create_funding_application(self):
        idea = StartupIdea.objects.create(
            user=self.user,
            startup_name="FundApp",
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
        app = FundingApplication.objects.create(
            user=self.user,
            idea=idea,
            amount_requested=50000,
            pitch_summary="We need funding",
            status="submitted",
        )
        self.assertEqual(
            str(app), "FundApp - Direct"
        )

    def test_create_incubator(self):
        inc = Incubator.objects.create(
            name="Spark Labs",
            incubator_type="incubator",
            description="Great program",
        )
        self.assertEqual(str(inc), "Spark Labs")


class FundingViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="fundview", password="testpass123"
        )
        self.idea = StartupIdea.objects.create(
            user=self.user,
            startup_name="FundView",
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

    def test_investor_directory(self):
        Investor.objects.create(
            name="Test Investor",
            investor_type="angel",
            description="Angel investor",
        )
        response = self.client.get(
            reverse("investor_directory")
        )
        self.assertEqual(response.status_code, 200)

    def test_incubator_directory(self):
        Incubator.objects.create(
            name="Test Incubator",
            incubator_type="incubator",
            description="A great incubator",
        )
        response = self.client.get(
            reverse("incubator_directory")
        )
        self.assertEqual(response.status_code, 200)

    def test_apply_funding_login_required(self):
        response = self.client.get(reverse("apply_funding"))
        self.assertNotEqual(response.status_code, 200)

    def test_apply_funding_authenticated(self):
        self.client.login(
            username="fundview", password="testpass123"
        )
        response = self.client.get(reverse("apply_funding"))
        self.assertEqual(response.status_code, 200)

    def test_my_applications_login_required(self):
        response = self.client.get(reverse("my_applications"))
        self.assertNotEqual(response.status_code, 200)

    def test_my_applications_authenticated(self):
        self.client.login(
            username="fundview", password="testpass123"
        )
        response = self.client.get(reverse("my_applications"))
        self.assertEqual(response.status_code, 200)
