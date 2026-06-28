from django.contrib import admin
from .models import Whiteboard, SharedNote, NoteVersion, Poll, PollOption, TeamVote, TeamVoteOption, TeamVoteResponse, FileVersion, ActivityTimeline


@admin.register(Whiteboard)
class WhiteboardAdmin(admin.ModelAdmin):
    list_display = ["title", "created_by", "idea", "created_at", "updated_at"]
    list_filter = ["created_at"]


@admin.register(SharedNote)
class SharedNoteAdmin(admin.ModelAdmin):
    list_display = ["title", "created_by", "is_public", "created_at"]
    list_filter = ["is_public"]


@admin.register(NoteVersion)
class NoteVersionAdmin(admin.ModelAdmin):
    list_display = ["note", "version_number", "edited_by", "created_at"]


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ["question", "created_by", "is_active", "created_at"]
    list_filter = ["is_active"]


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ["poll", "text", "vote_count"]


@admin.register(TeamVote)
class TeamVoteAdmin(admin.ModelAdmin):
    list_display = ["title", "idea", "created_by", "is_active", "created_at"]


@admin.register(TeamVoteOption)
class TeamVoteOptionAdmin(admin.ModelAdmin):
    list_display = ["vote", "text"]


@admin.register(TeamVoteResponse)
class TeamVoteResponseAdmin(admin.ModelAdmin):
    list_display = ["vote", "option", "voter", "voted_at"]


@admin.register(FileVersion)
class FileVersionAdmin(admin.ModelAdmin):
    list_display = ["filename", "version_number", "uploaded_by", "idea", "uploaded_at"]


@admin.register(ActivityTimeline)
class ActivityTimelineAdmin(admin.ModelAdmin):
    list_display = ["user", "action_type", "description", "idea", "created_at"]
    list_filter = ["action_type"]
