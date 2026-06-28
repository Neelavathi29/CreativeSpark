from django.urls import path
from . import views

urlpatterns = [
    path("showcase/", views.showcase, name="showcase"),
    path("success-stories/", views.success_stories, name="success_stories"),
    path("add-story/", views.add_success_story, name="add_success_story"),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("profile/<int:user_id>/", views.public_profile, name="public_profile"),
    path("chat/", views.chat_rooms, name="chat_rooms"),
    path("chat/<int:pk>/", views.chat_room_detail, name="chat_room_detail"),
    path("chat/start/<int:user_id>/", views.start_chat, name="start_chat"),
    path("podcasts/", views.podcast_list, name="podcast_list"),
    path("webinars/", views.webinar_list, name="webinar_list"),
    path("webinars/<int:webinar_id>/register/", views.webinar_register, name="webinar_register"),
    path("forum/", views.forum_list, name="forum_list"),
    path("forum/ask/", views.forum_ask, name="forum_ask"),
    path("forum/<int:pk>/", views.forum_detail, name="forum_detail"),
]
