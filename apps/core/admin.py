from django.contrib import admin
from .models import (
    ContactMessage,
    Testimonial,
    StartupQuote,
    Notification,
    VisitorCounter,
    AccountActivityLog,
)


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
    list_display = [
        "user",
        "title",
        "notification_type",
        "is_read",
        "created_at",
    ]
    list_filter = ["is_read", "notification_type"]
    search_fields = ["user__username", "title"]


@admin.register(VisitorCounter)
class VisitorCounterAdmin(admin.ModelAdmin):
    list_display = ["date", "count"]
    list_filter = ["date"]


@admin.register(AccountActivityLog)
class AccountActivityLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "timestamp"]
    list_filter = ["action", "timestamp"]
    search_fields = ["user__username", "action"]
