from django.apps import AppConfig


class MentorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.mentors"

    def ready(self):
        from apps.core.signals import (
            notify_session_booked,
            notify_session_status_change,
        )
        from django.db.models.signals import post_save
        from .models import MentorshipSession
        post_save.connect(notify_session_booked, sender=MentorshipSession)
        post_save.connect(notify_session_status_change, sender=MentorshipSession)
