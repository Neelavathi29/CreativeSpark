from django.contrib import admin
from .models import StartupHealthScore, KpiDashboard, CashFlowForecast, FundingTimeline


@admin.register(StartupHealthScore)
class StartupHealthScoreAdmin(admin.ModelAdmin):
    list_display = ["idea", "overall_score", "calculated_at"]


@admin.register(KpiDashboard)
class KpiDashboardAdmin(admin.ModelAdmin):
    list_display = ["idea", "revenue_mrr", "burn_rate", "runway_months", "updated_at"]


@admin.register(CashFlowForecast)
class CashFlowForecastAdmin(admin.ModelAdmin):
    list_display = ["idea", "month", "projected_revenue", "projected_expenses"]
    list_filter = ["month"]


@admin.register(FundingTimeline)
class FundingTimelineAdmin(admin.ModelAdmin):
    list_display = ["idea", "event_type", "amount", "date", "investor_name"]
    list_filter = ["event_type"]
