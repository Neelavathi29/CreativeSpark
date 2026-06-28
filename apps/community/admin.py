from django.contrib import admin
from .models import UserFollow, SuccessStory, StartupShowcase, ChatRoom, ChatMessage, Podcast, Webinar, WebinarRegistration, ForumQuestion, ForumAnswer


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ["follower", "following", "created_at"]


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "achievement", "is_featured", "is_approved"]
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


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ["title", "host", "guest", "episode_number", "is_published", "created_at"]
    list_filter = ["is_published"]


@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ["title", "presenter", "scheduled_date", "is_active"]
    list_filter = ["is_active"]


@admin.register(WebinarRegistration)
class WebinarRegistrationAdmin(admin.ModelAdmin):
    list_display = ["webinar", "user", "registered_at", "attended"]


@admin.register(ForumQuestion)
class ForumQuestionAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "is_resolved", "views_count", "created_at"]
    list_filter = ["is_resolved"]


@admin.register(ForumAnswer)
class ForumAnswerAdmin(admin.ModelAdmin):
    list_display = ["question", "user", "is_accepted", "created_at"]
    list_filter = ["is_accepted"]
