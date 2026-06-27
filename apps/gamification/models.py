from django.db import models
from django.conf import settings


class Badge(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="bi-award")
    xp_required = models.IntegerField(default=0)
    badge_type = models.CharField(
        max_length=50,
        choices=[
            ("idea", "Idea Submitter"),
            ("evaluation", "Top Rated"),
            ("mentor", "Mentorship"),
            ("community", "Community"),
            ("milestone", "Milestone"),
            ("special", "Special"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="badges",
    )
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "badge")

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class UserXP(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="xp"
    )
    total_xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    ideas_submitted = models.IntegerField(default=0)
    ideas_approved = models.IntegerField(default=0)
    mentorship_sessions = models.IntegerField(default=0)
    comments_made = models.IntegerField(default=0)
    likes_given = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.user.username} - Level {self.level}"
            f" ({self.total_xp} XP)"
        )

    def add_xp(self, amount):
        self.total_xp += amount
        new_level = (self.total_xp // 100) + 1
        if new_level > self.level:
            self.level = new_level
        self.save()


class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="bi-trophy")
    xp_reward = models.IntegerField(default=50)
    badge_reward = models.ForeignKey(
        Badge, on_delete=models.SET_NULL, null=True, blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title


class UserChallenge(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="challenges",
    )
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name="participants"
    )
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(
        default=0, help_text="Progress percentage 0-100"
    )
    completed_at = models.DateTimeField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "challenge")

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"
