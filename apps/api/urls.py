from django.urls import path
from . import views

urlpatterns = [
    path("docs/", views.api_docs, name="api_docs"),
    path("health/", views.api_health, name="api_health"),
    path("token/", views.get_token, name="api_token"),
    path("ideas/", views.api_ideas_list, name="api_ideas_list"),
    path("ideas/<int:pk>/", views.api_idea_detail, name="api_idea_detail"),
    path("investors/", views.api_investors, name="api_investors"),
    path("webhook/", views.api_webhook, name="api_webhook"),
    path("webhooks/docs/", views.api_webhooks_docs, name="api_webhooks_docs"),
    path("keys/", views.api_keys_page, name="api_keys"),
    path("integrations/", views.api_integrations, name="api_integrations"),
]
