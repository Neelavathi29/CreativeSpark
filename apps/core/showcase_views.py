from django.shortcuts import render
from apps.ideas.models import StartupIdea
from apps.funding.models import FundingApplication
from apps.analytics.models import FundingTimeline
from django.db.models import Sum, Count


def world_startup_map(request):
    ideas = StartupIdea.objects.filter(status="approved")
    locations = []
    for idea in ideas:
        if idea.latitude and idea.longitude:
            locations.append({
                "name": idea.startup_name,
                "lat": float(idea.latitude),
                "lng": float(idea.longitude),
                "industry": idea.get_industry_display(),
                "status": idea.status,
                "url": f"/ideas/{idea.id}/",
            })
    context = {
        "locations": locations,
        "total_startups": ideas.count(),
        "industries": StartupIdea.INDUSTRY_CHOICES,
    }
    return render(request, "core/world_map.html", context)


def live_funding_tracker(request):
    total_applications = FundingApplication.objects.count()
    total_amount = FundingApplication.objects.filter(status="accepted").aggregate(total=Sum("amount_requested"))
    total_accepted = FundingApplication.objects.filter(status="accepted").count()
    total_pending = FundingApplication.objects.filter(status="submitted").count()
    recent_applications = FundingApplication.objects.order_by("-created_at")[:10]
    timeline = FundingTimeline.objects.select_related("idea").order_by("-date")[:20]
    return render(request, "core/live_funding_tracker.html", {
        "total_applications": total_applications,
        "total_amount": total_amount["total"] or 0,
        "total_accepted": total_accepted,
        "total_pending": total_pending,
        "recent_applications": recent_applications,
        "timeline": timeline,
    })
