from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Badge, UserBadge, UserXP, Challenge, UserChallenge


@login_required
def leaderboard(request):
    top_users = UserXP.objects.select_related("user").order_by("-total_xp")[
        :20
    ]
    user_xp, _ = UserXP.objects.get_or_create(user=request.user)

    context = {
        "top_users": top_users,
        "user_xp": user_xp,
        "user_rank": (
            list(UserXP.objects.order_by("-total_xp")).index(user_xp) + 1
        ),
    }
    return render(request, "gamification/leaderboard.html", context)


@login_required
def badges_view(request):
    all_badges = Badge.objects.all()
    user_badges = UserBadge.objects.filter(user=request.user).values_list(
        "badge_id", flat=True
    )

    badges_with_status = []
    user_xp = UserXP.objects.filter(user=request.user).first()
    xp_total = user_xp.total_xp if user_xp else 0
    for badge in all_badges:
        earned = badge.id in user_badges
        locked = not earned and xp_total < badge.xp_required
        progress = (
            100
            if earned
            else min(
                100,
                int(
                    (xp_total / badge.xp_required * 100)
                    if badge.xp_required > 0
                    else 0
                ),
            )
        )
        badges_with_status.append(
            {
                "badge": badge,
                "earned": earned,
                "locked": locked,
                "progress": progress,
            }
        )

    return render(
        request, "gamification/badges.html", {"badges": badges_with_status}
    )


@login_required
def challenge_list(request):
    active_challenges = Challenge.objects.filter(
        is_active=True, end_date__gte=timezone.now().date()
    )
    past_challenges = Challenge.objects.filter(
        Q(is_active=False) | Q(end_date__lt=timezone.now().date())
    )[:5]

    user_challenges = UserChallenge.objects.filter(user=request.user)
    joined_ids = user_challenges.values_list("challenge_id", flat=True)

    context = {
        "active_challenges": active_challenges,
        "past_challenges": past_challenges,
        "joined_ids": list(joined_ids),
        "user_challenges": user_challenges,
    }
    return render(request, "gamification/challenges.html", context)


@login_required
def join_challenge(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    uc, created = UserChallenge.objects.get_or_create(
        user=request.user,
        challenge=challenge,
    )
    if created:
        messages.success(request, f"Joined challenge: {challenge.title}!")
    else:
        messages.info(
            request, "You are already participating in this challenge."
        )
    return redirect("challenge_list")


@login_required
def complete_challenge(request, pk):
    uc = get_object_or_404(UserChallenge, pk=pk, user=request.user)
    if not uc.completed:
        uc.completed = True
        uc.progress = 100
        uc.completed_at = timezone.now()
        uc.save()

        user_xp, _ = UserXP.objects.get_or_create(user=request.user)
        user_xp.add_xp(uc.challenge.xp_reward)

        if uc.challenge.badge_reward:
            UserBadge.objects.get_or_create(
                user=request.user, badge=uc.challenge.badge_reward
            )

        messages.success(
            request,
            f"Challenge completed! +{uc.challenge.xp_reward} XP earned!",
        )
    return redirect("challenge_list")


def hall_of_fame(request):
    top_all_time = UserXP.objects.select_related("user").order_by("-total_xp")[
        :10
    ]
    top_month = UserXP.objects.select_related("user").order_by(
        "-level", "-total_xp"
    )[:5]

    recent_badges = UserBadge.objects.select_related("user", "badge").order_by(
        "-earned_at"
    )[:10]

    return render(
        request,
        "gamification/hall_of_fame.html",
        {
            "top_all_time": top_all_time,
            "top_month": top_month,
            "recent_badges": recent_badges,
        },
    )
