from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Investor, FundingApplication, Incubator, InvestorWatchlist, DueDiligenceChecklist, StartupComparison
from apps.ideas.models import StartupIdea
from apps.evaluation.ai_enhanced import calculate_valuation, calculate_funding_probability, generate_investment_growth


def investor_directory(request):
    investors = Investor.objects.filter(is_active=True)
    inv_type = request.GET.get("type", "")
    if inv_type:
        investors = investors.filter(investor_type=inv_type)
    watchlist_ids = []
    if request.user.is_authenticated:
        watchlist_ids = InvestorWatchlist.objects.filter(user=request.user).values_list("investor_id", flat=True)
    return render(request, "funding/investors.html", {
        "investors": investors,
        "investor_types": Investor.INVESTOR_TYPE,
        "current_type": inv_type,
        "watchlist_ids": list(watchlist_ids),
    })


@login_required
def apply_funding(request, investor_id=None):
    ideas = StartupIdea.objects.filter(user=request.user)
    investor = None
    if investor_id:
        investor = get_object_or_404(Investor, pk=investor_id)
    if request.method == "POST":
        idea = get_object_or_404(StartupIdea, pk=request.POST.get("idea"), user=request.user)
        FundingApplication.objects.create(
            user=request.user, idea=idea, investor=investor,
            amount_requested=request.POST.get("amount"),
            pitch_summary=request.POST.get("pitch_summary"),
        )
        messages.success(request, "Funding application submitted!")
        return redirect("investor_directory")
    return render(request, "funding/apply.html", {"ideas": ideas, "investor": investor})


@login_required
def my_applications(request):
    apps = FundingApplication.objects.filter(user=request.user)
    return render(request, "funding/my_applications.html", {"applications": apps})


@login_required
def valuation_calculator(request):
    result = None
    ideas = StartupIdea.objects.filter(user=request.user)
    if request.method == "POST":
        idea_id = request.POST.get("idea")
        if idea_id:
            idea = get_object_or_404(StartupIdea, pk=idea_id)
            result = calculate_valuation(idea)
    return render(request, "funding/calculator.html", {"ideas": ideas, "result": result})


@login_required
def growth_simulator(request):
    result = None
    if request.method == "POST":
        initial = float(request.POST.get("initial_investment", 10000))
        rate = float(request.POST.get("growth_rate", 15))
        years = int(request.POST.get("years", 10))
        growth_data = generate_investment_growth(initial, rate, years)
        result = {
            "data": growth_data, "initial": initial, "rate": rate, "years": years,
            "labels": [f'Year {p["year"]}' for p in growth_data],
            "values": [p["value"] for p in growth_data],
        }
    return render(request, "funding/growth_simulator.html", {"result": result})


def incubator_directory(request):
    incubators = Incubator.objects.filter(is_active=True)
    itype = request.GET.get("type", "")
    if itype:
        incubators = incubators.filter(incubator_type=itype)
    return render(request, "funding/incubators.html", {
        "incubators": incubators,
        "incubator_types": Incubator.INCUBATOR_TYPES,
        "current_type": itype,
    })


@login_required
def funding_probability(request):
    result = None
    ideas = StartupIdea.objects.filter(user=request.user)
    if request.method == "POST":
        idea_id = request.POST.get("idea")
        if idea_id:
            idea = get_object_or_404(StartupIdea, pk=idea_id)
            result = calculate_funding_probability(idea)
    return render(request, "funding/funding_probability.html", {"ideas": ideas, "result": result})


@login_required
def toggle_watchlist(request, investor_id):
    investor = get_object_or_404(Investor, pk=investor_id)
    watch, created = InvestorWatchlist.objects.get_or_create(user=request.user, investor=investor)
    if not created:
        watch.delete()
        messages.info(request, f"Removed {investor.name} from watchlist.")
    else:
        messages.success(request, f"Added {investor.name} to watchlist.")
    return redirect(request.META.get("HTTP_REFERER", "investor_directory"))


@login_required
def watchlist(request):
    items = InvestorWatchlist.objects.filter(user=request.user)
    return render(request, "funding/watchlist.html", {"watchlist_items": items})


@login_required
def due_diligence(request, idea_id):
    idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
    items = DueDiligenceChecklist.objects.filter(idea=idea)
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        if item_id:
            dd_item = get_object_or_404(DueDiligenceChecklist, pk=item_id, idea=idea)
            dd_item.is_completed = not dd_item.is_completed
            if dd_item.is_completed:
                dd_item.completed_by = request.user
                import datetime
                dd_item.completed_at = datetime.datetime.now()
            else:
                dd_item.completed_by = None
                dd_item.completed_at = None
            dd_item.save()
            messages.success(request, "Checklist updated!")
        return redirect("due_diligence", idea_id=idea.pk)
    categories = DueDiligenceChecklist._meta.get_field("category").choices
    return render(request, "funding/due_diligence.html", {"idea": idea, "items": items, "categories": categories})


@login_required
def due_diligence_add(request, idea_id):
    idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
    if request.method == "POST":
        DueDiligenceChecklist.objects.create(
            idea=idea,
            item=request.POST.get("item"),
            category=request.POST.get("category", "legal"),
        )
        messages.success(request, "Due diligence item added!")
        return redirect("due_diligence", idea_id=idea.pk)
    return redirect("due_diligence", idea_id=idea.pk)


@login_required
def startup_comparison(request):
    comparisons = StartupComparison.objects.filter(user=request.user)
    return render(request, "funding/comparison.html", {"comparisons": comparisons})


@login_required
def startup_comparison_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        idea_ids = request.POST.getlist("ideas")
        comp = StartupComparison.objects.create(name=name, user=request.user)
        ideas = StartupIdea.objects.filter(pk__in=idea_ids)
        comp.ideas.add(*ideas)
        messages.success(request, "Comparison created!")
        return redirect("startup_comparison_detail", pk=comp.pk)
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "funding/comparison_form.html", {"ideas": ideas})


@login_required
def startup_comparison_detail(request, pk):
    comp = get_object_or_404(StartupComparison, pk=pk, user=request.user)
    return render(request, "funding/comparison_detail.html", {"comparison": comp})
