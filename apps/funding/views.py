from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Investor, FundingApplication, Incubator
from apps.ideas.models import StartupIdea
from apps.evaluation.ai_enhanced import (
    calculate_valuation,
    calculate_funding_probability,
    generate_investment_growth,
)


def investor_directory(request):
    investors = Investor.objects.filter(is_active=True)
    inv_type = request.GET.get("type", "")
    if inv_type:
        investors = investors.filter(investor_type=inv_type)

    return render(
        request,
        "funding/investors.html",
        {
            "investors": investors,
            "investor_types": Investor.INVESTOR_TYPE,
            "current_type": inv_type,
        },
    )


@login_required
def apply_funding(request, investor_id=None):
    ideas = StartupIdea.objects.filter(user=request.user)
    investor = None
    if investor_id:
        investor = get_object_or_404(Investor, pk=investor_id)

    if request.method == "POST":
        idea = get_object_or_404(
            StartupIdea, pk=request.POST.get("idea"), user=request.user
        )
        FundingApplication.objects.create(
            user=request.user,
            idea=idea,
            investor=investor,
            amount_requested=request.POST.get("amount"),
            pitch_summary=request.POST.get("pitch_summary"),
        )
        messages.success(request, "Funding application submitted!")
        return redirect("investor_directory")

    return render(
        request,
        "funding/apply.html",
        {
            "ideas": ideas,
            "investor": investor,
        },
    )


@login_required
def my_applications(request):
    apps = FundingApplication.objects.filter(user=request.user)
    return render(
        request, "funding/my_applications.html", {"applications": apps}
    )


@login_required
def valuation_calculator(request):
    result = None
    ideas = StartupIdea.objects.filter(user=request.user)

    if request.method == "POST":
        idea_id = request.POST.get("idea")
        if idea_id:
            idea = get_object_or_404(StartupIdea, pk=idea_id)
            result = calculate_valuation(idea)

    return render(
        request,
        "funding/calculator.html",
        {
            "ideas": ideas,
            "result": result,
        },
    )


@login_required
def growth_simulator(request):
    result = None
    if request.method == "POST":
        initial = float(request.POST.get("initial_investment", 10000))
        rate = float(request.POST.get("growth_rate", 15))
        years = int(request.POST.get("years", 10))
        growth_data = generate_investment_growth(initial, rate, years)
        result = {
            "data": growth_data,
            "initial": initial,
            "rate": rate,
            "years": years,
            "labels": [f'Year {p["year"]}' for p in growth_data],
            "values": [p["value"] for p in growth_data],
        }

    return render(
        request,
        "funding/growth_simulator.html",
        {
            "result": result,
        },
    )


def incubator_directory(request):
    incubators = Incubator.objects.filter(is_active=True)
    itype = request.GET.get("type", "")
    if itype:
        incubators = incubators.filter(incubator_type=itype)
    incubator_types = Incubator.INCUBATOR_TYPES
    return render(
        request,
        "funding/incubators.html",
        {
            "incubators": incubators,
            "incubator_types": incubator_types,
            "current_type": itype,
        },
    )


@login_required
def funding_probability(request):
    result = None
    ideas = StartupIdea.objects.filter(user=request.user)
    if request.method == "POST":
        idea_id = request.POST.get("idea")
        if idea_id:
            idea = get_object_or_404(StartupIdea, pk=idea_id)
            result = calculate_funding_probability(idea)

    return render(
        request,
        "funding/funding_probability.html",
        {
            "ideas": ideas,
            "result": result,
        },
    )
