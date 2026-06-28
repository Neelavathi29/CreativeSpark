from django.db import models
from django.conf import settings


class StartupHealthScore(models.Model):
    idea = models.OneToOneField("ideas.StartupIdea", on_delete=models.CASCADE, related_name="health_score")
    overall_score = models.IntegerField(default=0, help_text="Overall health score 0-100")
    team_score = models.IntegerField(default=0)
    market_score = models.IntegerField(default=0)
    product_score = models.IntegerField(default=0)
    financial_score = models.IntegerField(default=0)
    traction_score = models.IntegerField(default=0)
    calculated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.idea.startup_name} Health: {self.overall_score}"


class KpiDashboard(models.Model):
    idea = models.OneToOneField("ideas.StartupIdea", on_delete=models.CASCADE, related_name="kpi_dashboard")
    monthly_active_users = models.IntegerField(default=0)
    revenue_mrr = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    burn_rate = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Monthly burn rate")
    runway_months = models.IntegerField(default=0)
    customer_acquisition_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lifetime_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gross_margin = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Percentage")
    churn_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Monthly churn %")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KPI - {self.idea.startup_name}"


class CashFlowForecast(models.Model):
    idea = models.ForeignKey("ideas.StartupIdea", on_delete=models.CASCADE, related_name="cash_flow_forecasts")
    month = models.DateField()
    projected_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    projected_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    actual_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    actual_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["month"]
        unique_together = ["idea", "month"]

    def __str__(self):
        return f"{self.idea.startup_name} - {self.month}"


class FundingTimeline(models.Model):
    idea = models.ForeignKey("ideas.StartupIdea", on_delete=models.CASCADE, related_name="funding_timeline")
    event_type = models.CharField(max_length=50, choices=(
        ("seed", "Seed Round"),
        ("angel", "Angel Investment"),
        ("pre_seed", "Pre-Seed"),
        ("series_a", "Series A"),
        ("series_b", "Series B"),
        ("series_c", "Series C"),
        ("grant", "Grant"),
        ("bootstrapped", "Bootstrapped"),
        ("revenue", "Revenue Funded"),
    ))
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    investor_name = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.idea.startup_name} - {self.get_event_type_display()}"
