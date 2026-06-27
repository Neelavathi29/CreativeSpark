from django.urls import path
from . import views

urlpatterns = [
    path("", views.idea_list, name="idea_list"),
    path("my-ideas/", views.my_ideas, name="my_ideas"),
    path("create/", views.idea_create, name="idea_create"),
    path("<int:pk>/", views.idea_detail, name="idea_detail"),
    path("<int:pk>/edit/", views.idea_edit, name="idea_edit"),
    path("<int:pk>/like/", views.like_idea, name="like_idea"),
    path("<int:pk>/bookmark/", views.bookmark_idea, name="bookmark_idea"),
    path("<int:pk>/comment/", views.add_comment, name="add_comment"),
]
