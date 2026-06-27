from django.contrib import admin
from .models import Evaluation, FundingTip, ChatConversation, ChatMessage


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = [
        "idea",
        "overall_rating",
        "innovation_score",
        "market_potential",
        "funding_probability",
        "created_at",
    ]
    list_filter = ["incubation_recommendation"]


@admin.register(FundingTip)
class FundingTipAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active"]
    list_filter = ["is_active"]


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "created_at"]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["conversation", "role", "created_at"]
    list_filter = ["role"]
