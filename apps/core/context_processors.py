import random
from .models import StartupQuote, Notification
from apps.gamification.models import UserXP


def site_settings(request):
    quote_qs = StartupQuote.objects.filter(is_active=True)
    quote_ids = list(quote_qs.values_list("id", flat=True))
    if quote_ids:
        daily_quote = StartupQuote.objects.get(
            pk=random.choice(quote_ids)
        )
    else:
        daily_quote = None
    context = {
        "site_name": "Creative Spark",
        "daily_quote": daily_quote,
    }

    if hasattr(request, "user") and request.user.is_authenticated:
        notifications = Notification.objects.filter(
            user=request.user, is_read=False
        )[:10]
        context["user_notifications"] = notifications
        context["notification_count"] = notifications.count()

        user_xp = UserXP.objects.filter(user=request.user).first()
        if user_xp:
            context["user_xp"] = user_xp

    return context
