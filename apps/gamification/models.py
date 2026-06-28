from django.db import models
from django.conf import settings


class Badge(models.Model):
    BADGE_TYPES = (
        ("idea", "Idea Submission"),
        ("evaluation", "Evaluation"),
        ("mentor", "Mentorship"),
        ("community", "Community"),
        ("milestone", "Milestone"),
        ("special", "Special"),
        ("verified", "Verified"),
        ("award", "Award"),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class", default="bi-award")
    xp_required = models.IntegerField(default=0)
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES, default="special")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="users")
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "badge"]
        ordering = ["-earned_at"]

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class UserXP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="xp")
    total_xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    ideas_submitted = models.IntegerField(default=0)
    ideas_approved = models.IntegerField(default=0)
    mentorship_sessions = models.IntegerField(default=0)
    comments_made = models.IntegerField(default=0)
    likes_given = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Lv.{self.level} ({self.total_xp}XP)"


class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="bi-star")
    xp_reward = models.IntegerField(default=50)
    badge_reward = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class UserChallenge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="challenges")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="participants")
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0, help_text="Progress percentage 0-100")
    completed_at = models.DateTimeField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "challenge"]
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"


class VerifiedBadge(models.Model):
    VERIFIED_TYPES = (
        ("startup", "Verified Startup"),
        ("mentor", "Verified Mentor"),
        ("investor", "Verified Investor"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="verified_badge")
    badge_type = models.CharField(max_length=20, choices=VERIFIED_TYPES)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="verified_by")
    verified_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_badge_type_display()}"


class MonthlyAward(models.Model):
    AWARD_TYPES = (
        ("innovator", "Monthly Innovator"),
        ("community_choice", "Community Choice"),
        ("rising_star", "Rising Star"),
        ("top_mentor", "Top Mentor"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="awards")
    award_type = models.CharField(max_length=30, choices=AWARD_TYPES)
    month = models.DateField(help_text="First day of the month")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "award_type", "month"]
        ordering = ["-month"]

    def __str__(self):
        return f"{self.user.username} - {self.get_award_type_display()} ({self.month.strftime('%B %Y')})"
