from django.db import models
from django.conf import settings


class Whiteboard(models.Model):
    idea = models.ForeignKey("ideas.StartupIdea", on_delete=models.CASCADE, null=True, blank=True, related_name="whiteboards")
    title = models.CharField(max_length=200)
    content = models.JSONField(default=dict, help_text="Whiteboard canvas data as JSON")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="whiteboards")
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="collab_whiteboards")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class SharedNote(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    idea = models.ForeignKey("ideas.StartupIdea", on_delete=models.CASCADE, null=True, blank=True, related_name="shared_notes")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shared_notes")
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="collab_notes")
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class NoteVersion(models.Model):
    note = models.ForeignKey(SharedNote, on_delete=models.CASCADE, related_name="versions")
    content = models.TextField()
    version_number = models.PositiveIntegerField()
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-version_number"]
        unique_together = ["note", "version_number"]

    def __str__(self):
        return f"{self.note.title} v{self.version_number}"


class Poll(models.Model):
    question = models.CharField(max_length=300)
    idea = models.ForeignKey("ideas.StartupIdea", on_delete=models.CASCADE, null=True, blank=True, related_name="polls")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="polls")
    is_active = models.BooleanField(default=True)
    allow_multiple = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.question


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200)
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="poll_votes")

    def __str__(self):
        return self.text

    def vote_count(self):
        return self.votes.count()


class TeamVote(models.Model):
    idea = models.ForeignKey("ideas.StartupIdea", on_delete=models.CASCADE, related_name="team_votes")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team_votes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class TeamVoteOption(models.Model):
    vote = models.ForeignKey(TeamVote, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class TeamVoteResponse(models.Model):
    vote = models.ForeignKey(TeamVote, on_delete=models.CASCADE, related_name="responses")
    option = models.ForeignKey(TeamVoteOption, on_delete=models.CASCADE)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["vote", "voter"]

    def __str__(self):
        return f"{self.voter.username} voted on {self.vote.title}"


class FileVersion(models.Model):
    file = models.FileField(upload_to="file_versions/")
    filename = models.CharField(max_length=255)
    version_number = models.PositiveIntegerField()
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    idea = models.ForeignKey("ideas.StartupIdea", on_delete=models.CASCADE, null=True, blank=True, related_name="file_versions")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-version_number"]

    def __str__(self):
        return f"{self.filename} v{self.version_number}"


class ActivityTimeline(models.Model):
    ACTION_TYPES = (
        ("created", "Created"),
        ("updated", "Updated"),
        ("deleted", "Deleted"),
        ("commented", "Commented"),
        ("voted", "Voted"),
        ("shared", "Shared"),
        ("submitted", "Submitted"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="timeline_activities")
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    description = models.CharField(max_length=300)
    idea = models.ForeignKey("ideas.StartupIdea", on_delete=models.SET_NULL, null=True, blank=True, related_name="timeline_activities")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Activity timelines"

    def __str__(self):
        return f"{self.user.username} {self.action_type}: {self.description[:50]}"
