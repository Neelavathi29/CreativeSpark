from django.contrib import admin
from .models import (
    UserFollow,
    SuccessStory,
    StartupShowcase,
    ChatRoom,
    ChatMessage,
)


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ["follower", "following", "created_at"]


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "user",
        "achievement",
        "is_featured",
        "is_approved",
    ]
    list_filter = ["is_featured", "is_approved"]


@admin.register(StartupShowcase)
class StartupShowcaseAdmin(admin.ModelAdmin):
    list_display = ["idea", "is_published", "funding_raised"]
    list_filter = ["is_published"]


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ["name", "is_group", "created_at"]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "room", "created_at"]
