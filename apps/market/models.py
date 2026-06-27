from django.db import models
from django.conf import settings


class IndustryTrend(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    growth_rate = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Growth rate in %"
    )
    market_size = models.DecimalField(
        max_digits=15, decimal_places=2, help_text="Market size in USD"
    )
    icon = models.CharField(max_length=50, default="bi-graph-up")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-growth_rate"]

    def __str__(self):
        return self.name


class Competitor(models.Model):
    idea = models.ForeignKey(
        "ideas.StartupIdea",
        on_delete=models.CASCADE,
        related_name="competitors",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    market_share = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Market share in %"
    )
    strength = models.TextField()
    weakness = models.TextField()
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MarketAnalysis(models.Model):
    idea = models.ForeignKey(
        "ideas.StartupIdea",
        on_delete=models.CASCADE,
        related_name="market_analyses",
    )
    estimated_market_size = models.DecimalField(
        max_digits=15, decimal_places=2
    )
    target_audience = models.TextField()
    growth_opportunities = models.TextField()
    key_trends = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Market analysis for {self.idea.startup_name}"


class NewsArticle(models.Model):
    title = models.CharField(max_length=300)
    summary = models.TextField()
    content = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class LearningResource(models.Model):
    RESOURCE_TYPES = (
        ("course", "Course"),
        ("video", "Video"),
        ("article", "Article"),
        ("book", "Book"),
        ("tool", "Tool"),
        ("other", "Other"),
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    url = models.URLField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="resources/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class JobPosting(models.Model):
    JOB_TYPES = (
        ("internship", "Internship"),
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("contract", "Contract"),
        ("freelance", "Freelance"),
    )
    company = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    location = models.CharField(max_length=200, blank=True, null=True)
    is_remote = models.BooleanField(default=False)
    application_url = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} at {self.company}"


class Event(models.Model):
    EVENT_TYPES = (
        ("hackathon", "Hackathon"),
        ("workshop", "Workshop"),
        ("seminar", "Seminar"),
        ("conference", "Conference"),
        ("networking", "Networking"),
        ("pitch_competition", "Pitch Competition"),
        ("other", "Other"),
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    virtual_link = models.URLField(blank=True, null=True)
    is_virtual = models.BooleanField(default=False)
    organizer = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    registration_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.title
