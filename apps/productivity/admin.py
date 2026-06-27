from django.contrib import admin
from .models import (
    Task,
    Milestone,
    CalendarEvent,
    Workspace,
    WorkspaceMember,
    WorkspaceDocument,
)

admin.site.register(Task)
admin.site.register(Milestone)
admin.site.register(CalendarEvent)
admin.site.register(Workspace)
admin.site.register(WorkspaceMember)
admin.site.register(WorkspaceDocument)
