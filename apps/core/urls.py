from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("activity-log/", views.activity_log, name="activity_log"),
    path("set-language/", views.set_language, name="set_language"),
    path(
        "notifications/<int:pk>/read/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),
    path(
        "notifications/read-all/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read",
    ),
]
