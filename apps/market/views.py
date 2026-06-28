from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import (
    IndustryTrend,
    Competitor,
    MarketAnalysis,
    NewsArticle,
    LearningResource,
    JobPosting,
    Event,
)
from apps.ideas.models import StartupIdea


def market_analysis(request, pk=None):
    idea = None
    analysis = None
    competitors = []

    if pk:
        idea = get_object_or_404(StartupIdea, pk=pk)
        analysis = MarketAnalysis.objects.filter(idea=idea).first()
        competitors = Competitor.objects.filter(idea=idea)

    trends = IndustryTrend.objects.filter(is_active=True)
    industries = dict(StartupIdea.INDUSTRY_CHOICES)

    trend_labels = [t.name for t in trends]
    trend_data = [float(t.growth_rate) for t in trends]
    market_sizes = [float(t.market_size) for t in trends]

    context = {
        "idea": idea,
        "analysis": analysis,
        "competitors": competitors,
        "trends": trends,
        "industries": industries,
        "trend_labels": trend_labels,
        "trend_data": trend_data,
        "market_sizes": market_sizes,
    }
    return render(request, "market/market_analysis.html", context)


def news_feed(request):
    news = NewsArticle.objects.filter(is_active=True)
    category = request.GET.get("category", "")
    if category:
        news = news.filter(category=category)
    categories = (
        NewsArticle.objects.values_list("category", flat=True)
        .distinct()
        .exclude(category__isnull=True)
        .exclude(category="")
    )
    return render(
        request,
        "market/news_feed.html",
        {
            "news": news,
            "categories": categories,
            "current_category": category,
        },
    )


def learning_resources(request):
    resources = LearningResource.objects.filter(is_active=True)
    rtype = request.GET.get("type", "")
    if rtype:
        resources = resources.filter(resource_type=rtype)
    resource_types = LearningResource.RESOURCE_TYPES
    return render(
        request,
        "market/learning_resources.html",
        {
            "resources": resources,
            "resource_types": resource_types,
            "current_type": rtype,
        },
    )


def job_board(request):
    jobs = JobPosting.objects.filter(is_active=True)
    jtype = request.GET.get("type", "")
    if jtype:
        jobs = jobs.filter(job_type=jtype)
    job_types = JobPosting.JOB_TYPES
    return render(
        request,
        "market/job_board.html",
        {
            "jobs": jobs,
            "job_types": job_types,
            "current_type": jtype,
        },
    )


def event_list(request):
    events = Event.objects.filter(is_active=True)
    etype = request.GET.get("type", "")
    if etype:
        events = events.filter(event_type=etype)
    event_types = Event.EVENT_TYPES
    return render(
        request,
        "market/event_list.html",
        {
            "events": events,
            "event_types": event_types,
            "current_type": etype,
        },
    )


def startup_map(request):
    ideas = StartupIdea.objects.filter(
        ~Q(latitude__isnull=True), ~Q(longitude__isnull=True)
    )[:50]

    startups_data = []
    for idea in ideas:
        startups_data.append(
            {
                "id": idea.id,
                "name": idea.startup_name,
                "industry": idea.get_industry_display(),
                "lat": float(idea.latitude),
                "lng": float(idea.longitude),
                "city": idea.location_city or "",
                "url": f"/ideas/{idea.id}/",
            }
        )

    return render(
        request,
        "market/startup_map.html",
        {
            "startups_json": startups_data,
        },
    )
