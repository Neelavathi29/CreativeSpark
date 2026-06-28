from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StartupHealthScore, KpiDashboard, CashFlowForecast, FundingTimeline
from apps.ideas.models import StartupIdea
from decimal import Decimal


@login_required
def health_dashboard(request):
    ideas = StartupIdea.objects.filter(user=request.user)
    health_scores = StartupHealthScore.objects.filter(idea__in=ideas)
    return render(request, "analytics/health_dashboard.html", {
        "ideas": ideas,
        "health_scores": {hs.idea_id: hs for hs in health_scores},
    })


@login_required
def calculate_health(request, idea_id):
    idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
    health, created = StartupHealthScore.objects.get_or_create(idea=idea)
    evaluation = idea.evaluations.first()
    if evaluation:
        health.team_score = min(100, int(evaluation.feasibility_score * 0.8 + 20))
        health.market_score = evaluation.market_potential
        health.product_score = evaluation.innovation_score
        health.financial_score = min(100, int(evaluation.risk_score * 0.7 + 30))
        health.traction_score = min(100, int(health.product_score * 0.6 + evaluation.scalability_score * 0.4))
        health.overall_score = int((health.team_score + health.market_score + health.product_score + health.financial_score + health.traction_score) / 5)
    else:
        health.overall_score = 50
        health.team_score = 50
        health.market_score = 50
        health.product_score = 50
        health.financial_score = 50
        health.traction_score = 50
    health.save()
    messages.success(request, "Health score calculated!")
    return redirect("health_dashboard")


@login_required
def kpi_dashboard(request):
    ideas = StartupIdea.objects.filter(user=request.user)
    kpis = KpiDashboard.objects.filter(idea__in=ideas)
    return render(request, "analytics/kpi_dashboard.html", {
        "ideas": ideas,
        "kpis": {k.idea_id: k for k in kpis},
    })


@login_required
def kpi_update(request, idea_id):
    idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
    kpi, _ = KpiDashboard.objects.get_or_create(idea=idea)
    if request.method == "POST":
        kpi.monthly_active_users = int(request.POST.get("mau", 0))
        kpi.revenue_mrr = Decimal(request.POST.get("mrr", 0))
        kpi.burn_rate = Decimal(request.POST.get("burn_rate", 0))
        if kpi.burn_rate > 0:
            kpi.runway_months = int(kpi.revenue_mrr / kpi.burn_rate) if kpi.revenue_mrr > kpi.burn_rate else 0
        kpi.customer_acquisition_cost = Decimal(request.POST.get("cac", 0))
        kpi.lifetime_value = Decimal(request.POST.get("ltv", 0))
        kpi.gross_margin = Decimal(request.POST.get("gross_margin", 0))
        kpi.churn_rate = Decimal(request.POST.get("churn_rate", 0))
        kpi.save()
        messages.success(request, "KPI updated!")
        return redirect("kpi_dashboard")
    return render(request, "analytics/kpi_form.html", {"kpi": kpi, "idea": idea})


@login_required
def cash_flow(request):
    ideas = StartupIdea.objects.filter(user=request.user)
    forecasts = CashFlowForecast.objects.filter(idea__in=ideas).order_by("month")
    return render(request, "analytics/cash_flow.html", {
        "ideas": ideas,
        "forecasts": forecasts,
    })


@login_required
def cash_flow_add(request):
    if request.method == "POST":
        idea_id = request.POST.get("idea")
        idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
        import datetime
        month = datetime.date(int(request.POST["year"]), int(request.POST["month"]), 1)
        CashFlowForecast.objects.update_or_create(
            idea=idea, month=month,
            defaults={
                "projected_revenue": Decimal(request.POST.get("proj_revenue", 0)),
                "projected_expenses": Decimal(request.POST.get("proj_expenses", 0)),
            }
        )
        messages.success(request, "Cash flow entry added!")
        return redirect("cash_flow")
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "analytics/cash_flow_form.html", {"ideas": ideas})


@login_required
def funding_timeline(request):
    ideas = StartupIdea.objects.filter(user=request.user)
    timelines = FundingTimeline.objects.filter(idea__in=ideas).order_by("date")
    return render(request, "analytics/funding_timeline.html", {
        "ideas": ideas,
        "timelines": timelines,
    })


@login_required
def funding_timeline_add(request):
    if request.method == "POST":
        idea_id = request.POST.get("idea")
        idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
        import datetime
        FundingTimeline.objects.create(
            idea=idea,
            event_type=request.POST["event_type"],
            amount=Decimal(request.POST["amount"]),
            date=datetime.date(int(request.POST["year"]), int(request.POST["month"]), 1),
            investor_name=request.POST.get("investor_name", ""),
            notes=request.POST.get("notes", ""),
        )
        messages.success(request, "Funding event added!")
        return redirect("funding_timeline")
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "analytics/funding_timeline_form.html", {"ideas": ideas, "event_types": FundingTimeline._meta.get_field("event_type").choices})
