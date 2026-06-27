from django.urls import path
from . import views

urlpatterns = [
    path("tasks/", views.task_board, name="task_board"),
    path("tasks/<int:idea_id>/", views.task_board, name="idea_tasks"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="delete_task"),
    path(
        "tasks/<int:task_id>/<str:status>/",
        views.update_task_status,
        name="update_task_status",
    ),
    path("milestones/<int:idea_id>/", views.milestones, name="milestones"),
    path(
        "milestones/<int:milestone_id>/update/",
        views.update_milestone,
        name="update_milestone",
    ),
    path("calendar/", views.calendar_view, name="calendar_view"),
    path("workspaces/", views.workspace_list, name="workspace_list"),
    path(
        "workspaces/create/", views.workspace_create, name="workspace_create"
    ),
    path(
        "workspaces/<int:pk>/", views.workspace_detail, name="workspace_detail"
    ),
]
