from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import (
    IndustryTrend, Competitor, MarketAnalysis,
    NewsArticle, LearningResource, JobPosting, Event,
)
from apps.ideas.models import StartupIdea

User = get_user_model()


class MarketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="mktuser", password="testpass123"
        )

    def test_industry_trend(self):
        trend = IndustryTrend.objects.create(
            name="AI Growth", growth_rate=25.5, market_size=500000
        )
        self.assertEqual(str(trend), "AI Growth")

    def test_competitor(self):
        trend = IndustryTrend.objects.create(
            name="Tech", growth_rate=10, market_size=1000
        )
        comp = Competitor.objects.create(
            name="CompetitorX",
            description="A rival",
            market_share=15.0,
            strength="Strong brand",
            weakness="High cost",
        )
        self.assertEqual(str(comp), "CompetitorX")

    def test_news_article(self):
        article = NewsArticle.objects.create(
            title="Startup News", summary="Big news today"
        )
        self.assertEqual(str(article), "Startup News")

    def test_learning_resource(self):
        resource = LearningResource.objects.create(
            title="Django Guide", url="http://example.com",
            resource_type="article"
        )
        self.assertEqual(str(resource), "Django Guide")

    def test_job_posting(self):
        job = JobPosting.objects.create(
            company="TechCo", title="Developer",
            description="Build stuff", job_type="full_time"
        )
        self.assertEqual(str(job), "Developer at TechCo")

    def test_event(self):
        event = Event.objects.create(
            title="Hackathon 2026",
            event_type="hackathon",
            start_date="2026-07-15T10:00:00Z",
        )
        self.assertEqual(str(event), "Hackathon 2026")


class MarketViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="mktview", password="testpass123"
        )

    def test_news_feed(self):
        NewsArticle.objects.create(
            title="Article 1", summary="Summary"
        )
        response = self.client.get(reverse("news_feed"))
        self.assertEqual(response.status_code, 200)

    def test_learning_resources(self):
        LearningResource.objects.create(
            title="Resource", url="http://example.com",
            resource_type="article"
        )
        response = self.client.get(reverse("learning_resources"))
        self.assertEqual(response.status_code, 200)

    def test_job_board(self):
        JobPosting.objects.create(
            company="Co", title="Job", description="Work",
            job_type="full_time"
        )
        response = self.client.get(reverse("job_board"))
        self.assertEqual(response.status_code, 200)

    def test_event_list(self):
        Event.objects.create(
            title="Event", event_type="workshop",
            start_date="2026-07-15T10:00:00Z"
        )
        response = self.client.get(reverse("event_list"))
        self.assertEqual(response.status_code, 200)

    def test_market_analysis_requires_login(self):
        response = self.client.get(reverse("market_analysis"))
        self.assertNotEqual(response.status_code, 200)

    def test_market_analysis_authenticated(self):
        self.client.login(username="mktview", password="testpass123")
        response = self.client.get(reverse("market_analysis"))
        self.assertEqual(response.status_code, 200)
