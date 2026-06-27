from django.contrib import admin
from .models import (
    MentorProfile,
    MentorshipSession,
    Discussion,
    DiscussionReply,
)


@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "company", "designation", "available", "rating"]
    list_filter = ["available"]


@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display = ["student", "mentor", "topic", "status", "preferred_date"]
    list_filter = ["status"]


admin.site.register(Discussion)
admin.site.register(DiscussionReply)
