from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification


def create_notification(user, title, message, notification_type="info", link=None):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        link=link,
    )


def notify_idea_submitted(sender, instance, created, **kwargs):
    if created:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            create_notification(
                admin,
                "New Startup Idea Submitted",
                f"{instance.user.username} submitted '{instance.startup_name}'",
                "info",
                f"/ideas/{instance.pk}/",
            )


def notify_idea_status_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = sender.objects.get(pk=instance.pk)
            if old.status != instance.status:
                create_notification(
                    instance.user,
                    f"Idea Status Updated: {instance.get_status_display()}",
                    f"Your idea '{instance.startup_name}' is now {instance.get_status_display()}",
                    "success" if instance.status in ("approved", "launched") else "warning",
                    f"/ideas/{instance.pk}/",
                )
        except sender.DoesNotExist:
            pass


def notify_session_booked(sender, instance, created, **kwargs):
    if created:
        create_notification(
            instance.mentor.user,
            "New Mentorship Session Booked",
            f"{instance.student.username} booked a session on '{instance.topic}'",
            "info",
            "/mentors/my-sessions/",
        )


def notify_session_status_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = sender.objects.get(pk=instance.pk)
            if old.status != instance.status:
                target = instance.student
                title = f"Session {instance.get_status_display()}"
                msg = f"Your session on '{instance.topic}' is now {instance.get_status_display()}"
                ntype = "success" if instance.status == "confirmed" else "warning"
                create_notification(target, title, msg, ntype, "/mentors/my-sessions/")
        except sender.DoesNotExist:
            pass