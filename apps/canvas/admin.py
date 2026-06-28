from django.contrib import admin
from .models import CanvasProject


@admin.register(CanvasProject)
class CanvasProjectAdmin(admin.ModelAdmin):
    list_display = ["idea", "canvas_type", "created_by", "created_at", "updated_at"]
    list_filter = ["canvas_type"]
