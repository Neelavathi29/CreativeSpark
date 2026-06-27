from django.urls import path
from . import views
from . import ai_views

urlpatterns = [
    path("<int:pk>/", views.evaluation_detail, name="evaluation_detail"),
    path("funding-tips/", views.funding_tips, name="funding_tips"),
    path("ai/tools/", ai_views.ai_tools, name="ai_tools"),
    path("ai/chatbot/", ai_views.chatbot_view, name="chatbot"),
    path("ai/chatbot/api/", ai_views.chatbot_api, name="chatbot_api"),
    path("ai/voice-to-text/", ai_views.voice_to_text, name="voice_to_text"),
]
