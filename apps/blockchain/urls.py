from django.urls import path
from . import views

urlpatterns = [
    path("", views.blockchain_dashboard, name="blockchain_dashboard"),
    path("timestamp/<int:idea_id>/", views.timestamp_idea, name="timestamp_idea"),
    path("certificate/<int:pk>/", views.blockchain_certificate, name="blockchain_certificate"),
    path("verify/", views.verify_certificate, name="verify_certificate"),
]
