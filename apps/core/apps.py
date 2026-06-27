from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        from .signals import notify_idea_submitted, notify_idea_status_change
        from django.db.models.signals import post_save
        from apps.ideas.models import StartupIdea
        post_save.connect(notify_idea_submitted, sender=StartupIdea)
        post_save.connect(notify_idea_status_change, sender=StartupIdea)
