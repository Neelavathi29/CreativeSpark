from django.db import models
from django.conf import settings


class Investor(models.Model):
    INVESTOR_TYPE = (
        ("angel", "Angel Investor"),
        ("vc", "Venture Capital"),
        ("seed", "Seed Fund"),
        ("corporate", "Corporate VC"),
        ("grant", "Government Grant"),
        ("accelerator", "Accelerator"),
    )
    name = models.CharField(max_length=200)
    investor_type = models.CharField(max_length=50, choices=INVESTOR_TYPE)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="investors/", blank=True, null=True)
    min_investment = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    max_investment = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    preferred_stages = models.CharField(
        max_length=200, help_text="Comma separated stages"
    )
    preferred_industries = models.TextField(
        help_text="Comma separated industries"
    )
    location = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    contact_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FundingApplication(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="funding_applications",
    )
    idea = models.ForeignKey(
        "ideas.StartupIdea",
        on_delete=models.CASCADE,
        related_name="funding_applications",
    )
    investor = models.ForeignKey(
        Investor, on_delete=models.SET_NULL, null=True, blank=True
    )
    amount_requested = models.DecimalField(max_digits=15, decimal_places=2)
    pitch_summary = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("reviewing", "Under Review"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="draft",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.idea.startup_name}"
            f" - {self.investor.name if self.investor else 'Direct'}"
        )


class Incubator(models.Model):
    INCUBATOR_TYPES = (
        ("incubator", "Incubator"),
        ("accelerator", "Accelerator"),
        ("both", "Both"),
    )
    name = models.CharField(max_length=200)
    incubator_type = models.CharField(max_length=20, choices=INCUBATOR_TYPES)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="incubators/", blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    focus_industries = models.TextField(help_text="Comma separated industries")
    programs = models.TextField(
        blank=True, null=True, help_text="Description of programs offered"
    )
    funding_range = models.CharField(max_length=200, blank=True, null=True)
    application_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
