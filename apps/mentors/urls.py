from django.urls import path
from . import views

urlpatterns = [
    path("", views.mentor_list, name="mentor_list"),
    path("<int:pk>/", views.mentor_detail, name="mentor_detail"),
    path("<int:pk>/book/", views.book_session, name="book_session"),
    path(
        "<int:pk>/discussion/create/",
        views.create_discussion,
        name="create_discussion",
    ),
    path("my-sessions/", views.my_sessions, name="my_sessions"),
    path(
        "discussion/<int:pk>/",
        views.discussion_detail,
        name="discussion_detail",
    ),
    path(
        "session/<int:pk>/feedback/",
        views.submit_feedback,
        name="submit_feedback",
    ),
]
