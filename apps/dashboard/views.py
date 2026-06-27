from datetime import date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from apps.ideas.models import StartupIdea, Category, Recommendation
from apps.evaluation.models import Evaluation
from apps.mentors.models import MentorshipSession
from apps.core.models import VisitorCounter
from apps.gamification.models import UserXP, UserBadge


@login_required
def home(request):
    user = request.user
    context = {}

    live_count = (
        VisitorCounter.objects.aggregate(total=Count("id"))["total"] or 0
    )
    today_count = VisitorCounter.objects.filter(date=date.today()).first()
    live_visitors = today_count.count if today_count else 0
    context["live_visitors"] = live_visitors
    context["total_visitors"] = live_count

    top_startups = (
        StartupIdea.objects.filter(status="approved")
        .annotate(eval_count=Count("evaluations"))
        .order_by("-views_count", "-likes_count")[:10]
    )
    context["top_startups"] = top_startups

    trending_categories = (
        Category.objects.annotate(idea_count=Count("ideas"))
        .filter(idea_count__gt=0)
        .order_by("-idea_count")
    )
    context["trending_categories"] = trending_categories

    monthly_data = []
    for i in range(6):
        month = date.today().replace(day=1) - timedelta(days=30 * i)
        count = StartupIdea.objects.filter(
            created_at__year=month.year, created_at__month=month.month
        ).count()
        monthly_data.append(
            {
                "month": month.strftime("%b %Y"),
                "count": count,
            }
        )
    monthly_data.reverse()
    context["monthly_data"] = monthly_data
    context["monthly_labels"] = [d["month"] for d in monthly_data]
    context["monthly_counts"] = [d["count"] for d in monthly_data]

    if user.is_authenticated:
        recommendations = Recommendation.objects.filter(
            user=user, is_read=False
        )[:5]
        context["recommendations"] = recommendations

    if user.role == "student" or user.role == "admin":
        ideas = StartupIdea.objects.filter(user=user)
        total_ideas = ideas.count()
        submitted = ideas.filter(status="submitted").count()
        approved = ideas.filter(status="approved").count()
        rejected = ideas.filter(status="rejected").count()

        evaluations = Evaluation.objects.filter(idea__in=ideas)
        avg_innovation = (
            evaluations.aggregate(avg=Avg("innovation_score"))["avg"] or 0
        )
        avg_feasibility = (
            evaluations.aggregate(avg=Avg("feasibility_score"))["avg"] or 0
        )
        avg_market = (
            evaluations.aggregate(avg=Avg("market_potential"))["avg"] or 0
        )
        avg_scalability = (
            evaluations.aggregate(avg=Avg("scalability_score"))["avg"] or 0
        )
        avg_overall = (
            evaluations.aggregate(avg=Avg("overall_rating"))["avg"] or 0
        )

        recent_activities = ideas.order_by("-updated_at")[:5]

        category_stats = Category.objects.annotate(
            idea_count=Count("ideas")
        ).filter(idea_count__gt=0)

        status_counts = {}
        for s, label in StartupIdea.STATUS_CHOICES:
            count = ideas.filter(status=s).count()
            if count > 0:
                status_counts[label] = count

        context.update(
            {
                "total_ideas": total_ideas,
                "submitted": submitted,
                "approved": approved,
                "rejected": rejected,
                "avg_innovation": round(avg_innovation, 1),
                "avg_feasibility": round(avg_feasibility, 1),
                "avg_market": round(avg_market, 1),
                "avg_scalability": round(avg_scalability, 1),
                "avg_overall": round(avg_overall, 1),
                "recent_activities": recent_activities,
                "category_stats": category_stats,
                "status_counts": status_counts,
            }
        )

        user_xp = UserXP.objects.filter(user=user).first()
        if user_xp:
            context["user_xp"] = user_xp
            badge_count = UserBadge.objects.filter(user=user).count()
            context["badge_count"] = badge_count

    elif user.role == "mentor":
        sessions = MentorshipSession.objects.filter(mentor__user=user)
        context.update(
            {
                "total_sessions": sessions.count(),
                "pending_sessions": sessions.filter(status="pending").count(),
                "completed_sessions": sessions.filter(
                    status="completed"
                ).count(),
                "recent_sessions": sessions.order_by("-created_at")[:5],
            }
        )

    return render(request, "dashboard/home.html", context)
