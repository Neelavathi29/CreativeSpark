from django.contrib import admin
from .models import ContactMessage, Testimonial, StartupQuote, Notification, VisitorCounter, AccountActivityLog, EmailTemplate, SiteConfiguration, AuditLog, SystemHealth, BackupRecord


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "is_read", "created_at"]
    list_filter = ["is_read"]
    search_fields = ["name", "email", "subject"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "rating", "is_active"]
    list_filter = ["is_active", "rating"]


@admin.register(StartupQuote)
class StartupQuoteAdmin(admin.ModelAdmin):
    list_display = ["author", "is_active"]
    list_filter = ["is_active"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "notification_type", "is_read", "created_at"]
    list_filter = ["notification_type", "is_read"]
    search_fields = ["title"]


@admin.register(VisitorCounter)
class VisitorCounterAdmin(admin.ModelAdmin):
    list_display = ["date", "count"]
    list_filter = ["date"]


@admin.register(AccountActivityLog)
class AccountActivityLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "ip_address", "timestamp"]
    list_filter = ["action"]
    search_fields = ["user__username"]


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "is_active"]
    list_filter = ["is_active"]


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ["site_name", "contact_email", "enable_registration", "maintenance_mode"]


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["action", "user", "model_name", "ip_address", "created_at"]
    list_filter = ["action"]
    search_fields = ["action", "user__username"]


@admin.register(SystemHealth)
class SystemHealthAdmin(admin.ModelAdmin):
    list_display = ["component", "status", "last_checked"]
    list_filter = ["status"]


@admin.register(BackupRecord)
class BackupRecordAdmin(admin.ModelAdmin):
    list_display = ["filename", "file_size", "backup_type", "created_by", "created_at"]
    list_filter = ["backup_type"]
