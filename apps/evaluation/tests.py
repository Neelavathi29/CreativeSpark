from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Evaluation, FundingTip, ChatConversation, ChatMessage
from apps.ideas.models import StartupIdea, Category

User = get_user_model()


class EvaluationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="evuser", password="testpass123"
        )
        self.idea = StartupIdea.objects.create(
            user=self.user,
            startup_name="EvalTest",
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
            team_members="Alice",
            expected_timeline="6 months",
        )

    def test_create_evaluation(self):
        ev = Evaluation.objects.create(
            idea=self.idea,
            innovation_score=85,
            feasibility_score=70,
            market_potential=90,
            scalability_score=75,
            risk_score=60,
            overall_rating=7.5,
            strengths="Good team",
            weaknesses="Early stage",
        )
        expected = f"Evaluation for {self.idea.startup_name} - {ev.overall_rating}"
        self.assertEqual(str(ev), expected)

    def test_create_funding_tip(self):
        tip = FundingTip.objects.create(
            title="Apply Early", content="Apply for grants early."
        )
        self.assertEqual(str(tip), "Apply Early")
        self.assertTrue(tip.is_active)

    def test_create_chat_conversation(self):
        conv = ChatConversation.objects.create(
            user=self.user, title="My Chat"
        )
        self.assertEqual(str(conv), "My Chat")

    def test_create_chat_message(self):
        conv = ChatConversation.objects.create(user=self.user)
        msg = ChatMessage.objects.create(
            conversation=conv, role="user", content="Hello"
        )
        self.assertTrue("Hello" in str(msg))


class EvaluationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="evviewuser", password="testpass123"
        )
        self.idea = StartupIdea.objects.create(
            user=self.user,
            startup_name="ViewTest",
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
            team_members="Alice",
            expected_timeline="6 months",
        )
        self.evaluation = Evaluation.objects.create(
            idea=self.idea, overall_rating=8.0
        )

    def test_evaluation_detail(self):
        self.client.login(username="evviewuser", password="testpass123")
        response = self.client.get(
            reverse("evaluation_detail", args=[self.idea.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_funding_tips(self):
        self.client.login(username="evviewuser", password="testpass123")
        FundingTip.objects.create(
            title="Grant", content="Apply now"
        )
        response = self.client.get(reverse("funding_tips"))
        self.assertEqual(response.status_code, 200)
