from django.db import models
from django.conf import settings


class LoginActivity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="login_activities",
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    is_successful = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Login activities"
        ordering = ["-timestamp"]

    def __str__(self):
        return (
            f"{self.user.username} - {self.ip_address}"
            f" - {'Success' if self.is_successful else 'Failed'}"
        )


class TwoFactorAuth(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="two_factor",
    )
    is_enabled = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=100, blank=True, null=True)
    backup_codes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"2FA {'Enabled' if self.is_enabled else 'Disabled'}"
            f" - {self.user.username}"
        )
