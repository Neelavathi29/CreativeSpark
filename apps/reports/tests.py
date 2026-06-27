from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.ideas.models import StartupIdea
from apps.evaluation.models import Evaluation

User = get_user_model()


class ReportsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="rptuser", password="testpass123"
        )
        self.idea = StartupIdea.objects.create(
            user=self.user,
            startup_name="ReportTest",
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

    def test_report_dashboard_requires_login(self):
        response = self.client.get(reverse("report_dashboard"))
        self.assertNotEqual(response.status_code, 200)

    def test_report_dashboard_authenticated(self):
        self.client.login(username="rptuser", password="testpass123")
        response = self.client.get(reverse("report_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_export_csv_all(self):
        self.client.login(username="rptuser", password="testpass123")
        response = self.client.get(reverse("export_csv_all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment", response["Content-Disposition"])

    def test_export_csv_single(self):
        self.client.login(username="rptuser", password="testpass123")
        response = self.client.get(
            reverse("export_csv", args=[self.idea.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_export_pdf_all(self):
        self.client.login(username="rptuser", password="testpass123")
        response = self.client.get(reverse("export_pdf_all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_export_excel_all(self):
        self.client.login(username="rptuser", password="testpass123")
        response = self.client.get(reverse("export_excel_all"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "spreadsheetml",
            response["Content-Type"],
        )
