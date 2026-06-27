from django.contrib import admin
from .models import (
    IndustryTrend,
    Competitor,
    MarketAnalysis,
    NewsArticle,
    LearningResource,
    JobPosting,
    Event,
)

admin.site.register(IndustryTrend)
admin.site.register(Competitor)
admin.site.register(MarketAnalysis)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "source", "is_active", "created_at"]
    list_filter = ["is_active", "category"]
    search_fields = ["title", "summary"]


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ["title", "resource_type", "category", "is_active"]
    list_filter = ["resource_type", "is_active"]


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "job_type", "is_active", "created_at"]
    list_filter = ["job_type", "is_active"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "event_type",
        "start_date",
        "is_featured",
        "is_active",
    ]
    list_filter = ["event_type", "is_featured", "is_active"]
