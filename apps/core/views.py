from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from apps.ideas.models import StartupIdea
from apps.evaluation.models import Evaluation
from .models import (
    ContactMessage,
    VisitorCounter,
    AccountActivityLog,
    Notification,
)


def home(request):
    ideas = StartupIdea.objects.filter(status="approved")[:6]
    from apps.mentors.models import MentorProfile
    stats = {
        "total_ideas": StartupIdea.objects.count(),
        "approved_ideas": StartupIdea.objects.filter(
            status="approved"
        ).count(),
        "avg_rating": Evaluation.objects.aggregate(
            avg=Avg("overall_rating")
        )["avg"] or 0,
        "mentors_count": MentorProfile.objects.count(),
    }
    trending_ideas = StartupIdea.objects.filter(is_trending=True)[:3]
    top_rated = StartupIdea.objects.filter(status="approved")[:4]

    counter, _ = VisitorCounter.objects.get_or_create(date=date.today())
    counter.count += 1
    counter.save()

    image_carousel = StartupIdea.objects.filter(
        status="approved", logo__isnull=False
    )[:6]
    for idea in image_carousel:
        if not idea.logo:
            idea.logo = None

    context = {
        "ideas": ideas,
        "stats": stats,
        "trending_ideas": trending_ideas,
        "top_rated": top_rated,
        "image_carousel": image_carousel,
    }
    return render(request, "core/home.html", context)


def about(request):
    stats = {
        "total_ideas": StartupIdea.objects.count(),
        "approved_ideas": StartupIdea.objects.filter(
            status="approved"
        ).count(),
        "avg_rating": Evaluation.objects.aggregate(
            avg=Avg("overall_rating")
        )["avg"] or 0,
    }
    return render(request, "core/about.html", {"stats": stats})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        ContactMessage.objects.create(
            name=name, email=email, subject=subject, message=message
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")
    return render(request, "core/contact.html")


@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(
        Notification, pk=pk, user=request.user
    )
    notification.is_read = True
    notification.save()
    return redirect(notification.link or "dashboard:home")


@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(
        user=request.user, is_read=False
    ).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect(request.META.get("HTTP_REFERER", "dashboard:home"))


@login_required
def activity_log(request):
    activities = AccountActivityLog.objects.filter(user=request.user)[:50]
    return render(
        request, "core/activity_log.html", {"activities": activities}
    )


@login_required
def set_language(request):
    if request.method == "POST":
        lang = request.POST.get("language", "en")
        if lang in ["en", "te", "hi"]:
            from django.utils.translation import LANGUAGE_SESSION_KEY

            if hasattr(request, "session"):
                request.session[LANGUAGE_SESSION_KEY] = lang
            messages.success(request, f"Language changed to {lang}")
    return redirect(request.META.get("HTTP_REFERER", "home"))


def faq(request):
    faqs = [
        {
            "q": "What is Creative Spark?",
            "a": "Creative Spark is an AI-powered startup incubation"
            " platform that helps entrepreneurs validate, evaluate,"
            " and grow their business ideas.",
        },
        {
            "q": "How does the AI evaluation work?",
            "a": "Our AI engine analyzes your startup idea across"
            " multiple dimensions including innovation, feasibility,"
            " market potential, scalability, and risk to provide"
            " a comprehensive evaluation.",
        },
        {
            "q": "Who can use this platform?",
            "a": "The platform is open to students, aspiring"
            " entrepreneurs, mentors, and investors who want to"
            " participate in the startup ecosystem.",
        },
        {
            "q": "How do I submit a startup idea?",
            "a": "Simply register as a student, navigate to the ideas"
            " section, and fill out the detailed submission form"
            " with your startup details.",
        },
        {
            "q": "What is the mentorship program?",
            "a": "Our mentorship program connects you with experienced"
            " industry professionals who provide guidance and"
            " feedback on your startup.",
        },
        {
            "q": "How are ideas evaluated?",
            "a": "Ideas are evaluated based on innovation (25%),"
            " feasibility (20%), market potential (25%),"
            " scalability (20%), and risk assessment (10%).",
        },
        {
            "q": "Can I update my submitted idea?",
            "a": "Yes, you can edit your idea anytime before it goes"
            " under review. Once reviewed, you may need to contact"
            " the admin.",
        },
        {
            "q": "What kind of reports are available?",
            "a": "You can generate PDF and Excel reports including"
            " startup evaluation reports, market analysis, and"
            " performance summaries.",
        },
    ]
    return render(request, "core/faq.html", {"faqs": faqs})
