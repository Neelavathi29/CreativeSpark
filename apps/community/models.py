from django.db import models
from django.conf import settings


class UserFollow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["follower", "following"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class ChatRoom(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="chat_rooms")
    name = models.CharField(max_length=200, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"Chat {self.id}"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"


class SuccessStory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="success_stories")
    idea = models.ForeignKey("ideas.StartupIdea", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    achievement = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="stories/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Success stories"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class StartupShowcase(models.Model):
    idea = models.OneToOneField("ideas.StartupIdea", on_delete=models.CASCADE, related_name="showcase")
    featured_image = models.ImageField(upload_to="showcase/", blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    funding_raised = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    featured_until = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Showcase: {self.idea.startup_name}"


class Podcast(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    audio_url = models.URLField()
    cover_image = models.ImageField(upload_to="podcasts/", blank=True, null=True)
    host = models.CharField(max_length=200, blank=True)
    guest = models.CharField(max_length=200, blank=True)
    duration_minutes = models.IntegerField(default=30)
    episode_number = models.IntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Webinar(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    presenter = models.CharField(max_length=200)
    presenter_bio = models.TextField(blank=True)
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    registration_link = models.URLField(blank=True)
    recording_url = models.URLField(blank=True)
    max_attendees = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-scheduled_date"]

    def __str__(self):
        return self.title


class WebinarRegistration(models.Model):
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="webinar_registrations")
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ["webinar", "user"]

    def __str__(self):
        return f"{self.user.username} - {self.webinar.title}"


class ForumQuestion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forum_questions")
    tags = models.CharField(max_length=300, blank=True, help_text="Comma separated tags")
    is_resolved = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ForumAnswer(models.Model):
    question = models.ForeignKey(ForumQuestion, on_delete=models.CASCADE, related_name="answers")
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forum_answers")
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_accepted", "created_at"]

    def __str__(self):
        return f"Answer by {self.user.username}"
