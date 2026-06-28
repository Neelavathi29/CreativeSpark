from django.db import models
from django.conf import settings


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class VisitorCounter(models.Model):
    count = models.IntegerField(default=0)
    date = models.DateField(unique=True)

    def __str__(self):
        return f"{self.date}: {self.count}"


class AccountActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="activity_logs")
    action = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = "Account activity logs"

    def __str__(self):
        return f"{self.user.username} - {self.action}"


class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    rating = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class StartupQuote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.quote[:50]}... - {self.author}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("info", "Info"),
        ("success", "Success"),
        ("warning", "Warning"),
        ("error", "Error"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default="info")
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class EmailTemplate(models.Model):
    name = models.CharField(max_length=200, unique=True)
    subject = models.CharField(max_length=300)
    body = models.TextField(help_text="Use {{ variable }} syntax for dynamic content")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=200, default="Creative Spark")
    tagline = models.CharField(max_length=300, blank=True)
    logo_url = models.URLField(blank=True)
    favicon_url = models.URLField(blank=True)
    primary_color = models.CharField(max_length=7, default="#0d6efd")
    secondary_color = models.CharField(max_length=7, default="#6c757d")
    contact_email = models.EmailField(default="hello@creativespark.io")
    enable_registration = models.BooleanField(default=True)
    enable_ai_features = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site configuration"
        verbose_name_plural = "Site configurations"

    def __str__(self):
        return self.site_name


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=200)
    model_name = models.CharField(max_length=100, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} by {self.user} at {self.created_at}"


class SystemHealth(models.Model):
    component = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=[
        ("healthy", "Healthy"),
        ("degraded", "Degraded"),
        ("down", "Down"),
    ], default="healthy")
    last_checked = models.DateTimeField(auto_now=True)
    details = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "System health"
        ordering = ["component"]

    def __str__(self):
        return f"{self.component}: {self.status}"


class BackupRecord(models.Model):
    filename = models.CharField(max_length=300)
    file_size = models.IntegerField(default=0, help_text="Size in bytes")
    backup_type = models.CharField(max_length=20, choices=[
        ("full", "Full"),
        ("partial", "Partial"),
    ], default="full")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.filename
