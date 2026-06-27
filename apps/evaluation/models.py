from django.db import models
from django.conf import settings


class Evaluation(models.Model):
    idea = models.ForeignKey(
        "ideas.StartupIdea",
        on_delete=models.CASCADE,
        related_name="evaluations",
    )

    innovation_score = models.IntegerField(
        default=0, help_text="Score out of 100"
    )
    feasibility_score = models.IntegerField(
        default=0, help_text="Score out of 100"
    )
    market_potential = models.IntegerField(
        default=0, help_text="Score out of 100"
    )
    scalability_score = models.IntegerField(
        default=0, help_text="Score out of 100"
    )
    risk_score = models.IntegerField(
        default=0, help_text="Score out of 100, higher = less risky"
    )
    overall_rating = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.0
    )
    funding_probability = models.IntegerField(
        default=0, help_text="Funding probability score out of 100"
    )

    strengths = models.TextField(blank=True, null=True)
    weaknesses = models.TextField(blank=True, null=True)
    opportunities = models.TextField(blank=True, null=True)
    threats = models.TextField(blank=True, null=True)
    improvement_suggestions = models.TextField(blank=True, null=True)

    incubation_recommendation = models.CharField(
        max_length=200, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Evaluation for {self.idea.startup_name} - {self.overall_rating}"
        )


class FundingTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    source = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChatConversation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_conversations",
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title or f"Conversation {self.id}"


class ChatMessage(models.Model):
    ROLE_CHOICES = (
        ("user", "User"),
        ("assistant", "Assistant"),
    )
    conversation = models.ForeignKey(
        ChatConversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
