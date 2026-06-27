from django.db import models
from django.conf import settings


class MentorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mentor_profile",
    )
    expertise = models.TextField(help_text="Areas of expertise")
    experience_years = models.IntegerField(default=0)
    company = models.CharField(max_length=200, blank=True, null=True)
    designation = models.CharField(max_length=200, blank=True, null=True)
    available = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    bio = models.TextField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    total_sessions = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mentor: {self.user.get_full_name() or self.user.username}"


class MentorshipSession(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    mentor = models.ForeignKey(
        MentorProfile, on_delete=models.CASCADE, related_name="sessions"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mentorship_sessions",
    )
    topic = models.CharField(max_length=200)
    message = models.TextField(blank=True, null=True)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    meeting_link = models.URLField(
        blank=True,
        null=True,
        help_text="Video meeting link (Zoom/Google Meet)",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    feedback = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0, help_text="Rating out of 5")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.student.username} - {self.mentor.user.username}"
            f" - {self.topic}"
        )


class Discussion(models.Model):
    mentor = models.ForeignKey(
        MentorProfile, on_delete=models.CASCADE, related_name="discussions"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class DiscussionReply(models.Model):
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name="replies"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "Discussion replies"

    def __str__(self):
        return f"Reply by {self.user.username}"
