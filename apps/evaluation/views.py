from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evaluation, FundingTip
from apps.ideas.models import StartupIdea


@login_required
def evaluation_detail(request, pk):
    idea = get_object_or_404(StartupIdea, pk=pk)
    evaluation = get_object_or_404(Evaluation, idea=idea)

    radar_data = {
        "innovation": evaluation.innovation_score,
        "feasibility": evaluation.feasibility_score,
        "market_potential": evaluation.market_potential,
        "scalability": evaluation.scalability_score,
        "risk": evaluation.risk_score,
    }

    context = {
        "idea": idea,
        "evaluation": evaluation,
        "radar_data": radar_data,
    }
    return render(request, "evaluation/evaluation_detail.html", context)


@login_required
def funding_tips(request):
    tips = FundingTip.objects.filter(is_active=True)
    return render(request, "evaluation/funding_tips.html", {"tips": tips})
