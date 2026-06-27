from django.contrib import admin
from .models import Investor, FundingApplication, Incubator


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "investor_type",
        "min_investment",
        "max_investment",
        "is_active",
    ]
    list_filter = ["investor_type", "is_active"]


@admin.register(FundingApplication)
class FundingApplicationAdmin(admin.ModelAdmin):
    list_display = ["idea", "investor", "amount_requested", "status"]
    list_filter = ["status"]


@admin.register(Incubator)
class IncubatorAdmin(admin.ModelAdmin):
    list_display = ["name", "incubator_type", "location", "is_active"]
    list_filter = ["incubator_type", "is_active"]
