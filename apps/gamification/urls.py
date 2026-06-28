from django.urls import path
from . import views

urlpatterns = [
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("badges/", views.badges_view, name="badges"),
    path("challenges/", views.challenge_list, name="challenge_list"),
    path("challenges/<int:pk>/join/", views.join_challenge, name="join_challenge"),
    path("challenges/<int:pk>/complete/", views.complete_challenge, name="complete_challenge"),
    path("hall-of-fame/", views.hall_of_fame, name="hall_of_fame"),
    path("verified-badges/", views.verified_badges_view, name="verified_badges"),
]
