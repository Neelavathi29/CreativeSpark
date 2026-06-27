from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("mentor", "Mentor"),
        ("admin", "Admin"),
    )
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="student"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(
        blank=True, null=True, help_text="Comma separated skills"
    )
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
