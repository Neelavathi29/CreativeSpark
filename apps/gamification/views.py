from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Badge, UserBadge, UserXP, Challenge, UserChallenge, VerifiedBadge, MonthlyAward
from django.db.models import Sum, Count


def leaderboard(request):
    top_users = UserXP.objects.select_related("user").order_by("-total_xp")[:50]
    return render(request, "gamification/leaderboard.html", {"top_users": top_users})


def badges_view(request):
    all_badges = Badge.objects.all()
    user_badges = []
    if request.user.is_authenticated:
        user_badges = UserBadge.objects.filter(user=request.user).values_list("badge_id", flat=True)
    return render(request, "gamification/badges.html", {
        "all_badges": all_badges,
        "user_badges": list(user_badges),
    })


@login_required
def challenge_list(request):
    challenges = Challenge.objects.filter(is_active=True)
    user_challenges = UserChallenge.objects.filter(user=request.user)
    return render(request, "gamification/challenges.html", {
        "challenges": challenges,
        "user_challenges": {uc.challenge_id: uc for uc in user_challenges},
    })


@login_required
def join_challenge(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk, is_active=True)
    UserChallenge.objects.get_or_create(user=request.user, challenge=challenge)
    messages.success(request, "Joined challenge!")
    return redirect("challenge_list")


@login_required
def complete_challenge(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk, is_active=True)
    uc, _ = UserChallenge.objects.get_or_create(user=request.user, challenge=challenge)
    if not uc.completed:
        uc.completed = True
        uc.progress = 100
        import datetime
        uc.completed_at = datetime.datetime.now()
        uc.save()
        user_xp, _ = UserXP.objects.get_or_create(user=request.user)
        user_xp.total_xp += challenge.xp_reward
        user_xp.level = max(1, user_xp.total_xp // 100 + 1)
        user_xp.save()
        if challenge.badge_reward:
            UserBadge.objects.get_or_create(user=request.user, badge=challenge.badge_reward)
        messages.success(request, f"Challenge completed! +{challenge.xp_reward}XP")
    return redirect("challenge_list")


def hall_of_fame(request):
    awards = MonthlyAward.objects.select_related("user").order_by("-month")[:50]
    return render(request, "gamification/hall_of_fame.html", {"awards": awards})


@login_required
def verified_badges_view(request):
    badges = VerifiedBadge.objects.filter(user=request.user)
    return render(request, "gamification/verified_badges.html", {"verified_badges": badges})
