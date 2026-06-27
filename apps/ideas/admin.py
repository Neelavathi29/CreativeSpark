from django.contrib import admin
from .models import (
    Category,
    StartupIdea,
    IdeaLike,
    IdeaBookmark,
    IdeaComment,
    Recommendation,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "created_at"]


@admin.register(StartupIdea)
class StartupIdeaAdmin(admin.ModelAdmin):
    list_display = ["startup_name", "user", "status", "industry", "created_at"]
    list_filter = ["status", "industry", "category"]
    search_fields = ["startup_name", "founder_name", "problem_statement"]
    actions = ["approve_ideas", "reject_ideas"]

    def approve_ideas(self, request, queryset):
        queryset.update(status="approved")

    approve_ideas.short_description = "Approve selected ideas"

    def reject_ideas(self, request, queryset):
        queryset.update(status="rejected")

    reject_ideas.short_description = "Reject selected ideas"


admin.site.register(IdeaLike)
admin.site.register(IdeaBookmark)
admin.site.register(IdeaComment)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ["user", "idea", "score", "is_read"]
    list_filter = ["is_read"]
