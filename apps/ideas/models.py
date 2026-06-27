from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, default="bi-lightbulb")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class StartupIdea(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("incubating", "Incubating"),
        ("launched", "Launched"),
    )

    INDUSTRY_CHOICES = (
        ("technology", "Technology"),
        ("healthcare", "Healthcare"),
        ("education", "Education"),
        ("finance", "Finance"),
        ("ecommerce", "E-Commerce"),
        ("agriculture", "Agriculture"),
        ("entertainment", "Entertainment"),
        ("environment", "Environment"),
        ("social", "Social Impact"),
        ("other", "Other"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ideas",
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="ideas"
    )

    startup_name = models.CharField(max_length=200)
    founder_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    problem_statement = models.TextField()
    proposed_solution = models.TextField()
    target_customers = models.TextField()
    business_model = models.TextField()
    revenue_model = models.TextField()
    competitor_analysis = models.TextField()
    unique_selling_proposition = models.TextField()
    required_investment = models.DecimalField(max_digits=15, decimal_places=2)
    team_members = models.TextField(
        help_text="Comma separated team member names"
    )
    expected_timeline = models.CharField(max_length=200)
    pitch_deck = models.FileField(
        upload_to="pitch_decks/", blank=True, null=True
    )
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    encrypted_pitch_deck = models.FileField(
        upload_to="encrypted_pitch_decks/", blank=True, null=True
    )

    location_city = models.CharField(max_length=200, blank=True, null=True)
    location_country = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft"
    )
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    bookmarks_count = models.IntegerField(default=0)
    is_trending = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.startup_name

    def get_overall_rating(self):
        evaluation = self.evaluations.first()
        if evaluation:
            return evaluation.overall_rating
        return None


class Recommendation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendations",
    )
    idea = models.ForeignKey(
        StartupIdea, on_delete=models.CASCADE, related_name="recommendations"
    )
    score = models.FloatField(default=0)
    reason = models.CharField(max_length=200, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.user.username} -> {self.idea.startup_name}"


class IdeaLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    idea = models.ForeignKey(
        StartupIdea, on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "idea")


class IdeaBookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    idea = models.ForeignKey(
        StartupIdea, on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "idea")


class IdeaComment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    idea = models.ForeignKey(
        StartupIdea, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.idea.startup_name}"
