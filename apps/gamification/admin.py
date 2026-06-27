from django.contrib import admin
from .models import Badge, UserBadge, UserXP, Challenge, UserChallenge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ["name", "badge_type", "xp_required"]
    list_filter = ["badge_type"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ["user", "badge", "earned_at"]


@admin.register(UserXP)
class UserXPAdmin(admin.ModelAdmin):
    list_display = ["user", "total_xp", "level"]


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "xp_reward",
        "start_date",
        "end_date",
        "is_active",
    ]
    list_filter = ["is_active"]


@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ["user", "challenge", "completed", "progress"]
    list_filter = ["completed"]
