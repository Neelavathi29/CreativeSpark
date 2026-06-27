from django.urls import path
from . import views

urlpatterns = [
    path("", views.market_analysis, name="market_analysis"),
    path("<int:pk>/", views.market_analysis, name="idea_market_analysis"),
    path("news/", views.news_feed, name="news_feed"),
    path("resources/", views.learning_resources, name="learning_resources"),
    path("jobs/", views.job_board, name="job_board"),
    path("events/", views.event_list, name="event_list"),
    path("map/", views.startup_map, name="startup_map"),
]
