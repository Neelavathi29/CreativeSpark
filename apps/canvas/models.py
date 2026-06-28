from django.db import models
from django.conf import settings


class CanvasProject(models.Model):
    CANVAS_TYPES = (
        ("business_model", "Business Model Canvas"),
        ("lean", "Lean Canvas"),
        ("swot", "SWOT Canvas"),
        ("value_proposition", "Value Proposition Canvas"),
        ("customer_persona", "Customer Persona"),
        ("user_journey", "User Journey Map"),
        ("risk_matrix", "Risk Matrix"),
        ("okr", "OKR Planner"),
    )
    idea = models.ForeignKey("ideas.StartupIdea", on_delete=models.CASCADE, related_name="canvas_projects")
    canvas_type = models.CharField(max_length=30, choices=CANVAS_TYPES)
    data = models.JSONField(default=dict, help_text="Canvas data as JSON")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="canvas_projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.get_canvas_type_display()} - {self.idea.startup_name}"
