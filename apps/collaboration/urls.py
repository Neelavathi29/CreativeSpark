from django.urls import path
from . import views

urlpatterns = [
    path("whiteboards/", views.whiteboard_list, name="whiteboard_list"),
    path("whiteboards/create/", views.whiteboard_create, name="whiteboard_create"),
    path("whiteboards/<int:pk>/", views.whiteboard_detail, name="whiteboard_detail"),
    path("notes/", views.shared_notes_list, name="shared_notes_list"),
    path("notes/create/", views.shared_note_create, name="shared_note_create"),
    path("notes/<int:pk>/", views.shared_note_detail, name="shared_note_detail"),
    path("polls/", views.poll_list, name="poll_list"),
    path("polls/create/", views.poll_create, name="poll_create"),
    path("polls/<int:pk>/", views.poll_detail, name="poll_detail"),
    path("team-votes/", views.team_vote_list, name="team_vote_list"),
    path("team-votes/<int:pk>/", views.team_vote_detail, name="team_vote_detail"),
    path("timeline/", views.timeline, name="collab_timeline"),
]
