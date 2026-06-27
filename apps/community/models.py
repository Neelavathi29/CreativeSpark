from django.db import models
from django.conf import settings


class UserFollow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class ChatRoom(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="chat_rooms"
    )
    name = models.CharField(max_length=200, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name or f"Chat {self.id}"


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"


class SuccessStory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="success_stories",
    )
    idea = models.ForeignKey(
        "ideas.StartupIdea", on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    achievement = models.CharField(
        max_length=200,
        help_text="Key achievement (e.g., 'Raised $1M Seed Round')",
    )
    image = models.ImageField(
        upload_to="success_stories/", blank=True, null=True
    )
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Success stories"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class StartupShowcase(models.Model):
    idea = models.OneToOneField(
        "ideas.StartupIdea", on_delete=models.CASCADE, related_name="showcase"
    )
    featured_image = models.ImageField(
        upload_to="showcase/", blank=True, null=True
    )
    website_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    funding_raised = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    is_published = models.BooleanField(default=False)
    featured_until = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Showcase: {self.idea.startup_name}"
