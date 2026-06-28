from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health_dashboard, name="health_dashboard"),
    path("health/<int:idea_id>/calculate/", views.calculate_health, name="calculate_health"),
    path("kpi/", views.kpi_dashboard, name="kpi_dashboard"),
    path("kpi/<int:idea_id>/update/", views.kpi_update, name="kpi_update"),
    path("cash-flow/", views.cash_flow, name="cash_flow"),
    path("cash-flow/add/", views.cash_flow_add, name="cash_flow_add"),
    path("funding-timeline/", views.funding_timeline, name="funding_timeline"),
    path("funding-timeline/add/", views.funding_timeline_add, name="funding_timeline_add"),
]
