from django.urls import path
from . import views

urlpatterns = [
    path("investors/", views.investor_directory, name="investor_directory"),
    path("apply/", views.apply_funding, name="apply_funding"),
    path("apply/<int:investor_id>/", views.apply_funding, name="apply_funding_investor"),
    path("my-applications/", views.my_applications, name="my_applications"),
    path("calculator/", views.valuation_calculator, name="valuation_calculator"),
    path("simulator/", views.growth_simulator, name="growth_simulator"),
    path("incubators/", views.incubator_directory, name="incubator_directory"),
    path("funding-probability/", views.funding_probability, name="funding_probability"),
    path("watchlist/toggle/<int:investor_id>/", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("due-diligence/<int:idea_id>/", views.due_diligence, name="due_diligence"),
    path("due-diligence/<int:idea_id>/add/", views.due_diligence_add, name="due_diligence_add"),
    path("comparison/", views.startup_comparison, name="startup_comparison"),
    path("comparison/create/", views.startup_comparison_create, name="startup_comparison_create"),
    path("comparison/<int:pk>/", views.startup_comparison_detail, name="startup_comparison_detail"),
]
