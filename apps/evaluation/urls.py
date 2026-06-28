from django.urls import path
from . import views
from . import ai_views
from . import advanced_ai_views
from . import showcase_features

urlpatterns = [
    path("<int:pk>/", views.evaluation_detail, name="evaluation_detail"),
    path("funding-tips/", views.funding_tips, name="funding_tips"),
    path("ai/tools/", ai_views.ai_tools, name="ai_tools"),
    path("ai/chatbot/", ai_views.chatbot_view, name="chatbot"),
    path("ai/chatbot/api/", ai_views.chatbot_api, name="chatbot_api"),
    path("ai/voice-to-text/", ai_views.voice_to_text, name="voice_to_text"),
    path("ai/sentiment/", advanced_ai_views.sentiment_analysis, name="sentiment_analysis"),
    path("ai/tags/", advanced_ai_views.tag_generator, name="tag_generator"),
    path("ai/legal-checklist/", advanced_ai_views.legal_checklist, name="legal_checklist"),
    path("ai/terms/", advanced_ai_views.terms_generator, name="terms_generator"),
    path("ai/pitch-analyzer/", advanced_ai_views.pitch_deck_analyzer, name="pitch_analyzer"),
    path("ai/elevator-pitch/", advanced_ai_views.elevator_pitch_analyzer, name="elevator_pitch"),
    path("ai/rag-chat/", advanced_ai_views.rag_chat, name="rag_chat"),
    path("ai/rag-chat/api/", advanced_ai_views.rag_chat_api, name="rag_chat_api"),
    path("showcase/innovation-radar/<int:idea_id>/", showcase_features.innovation_radar, name="innovation_radar"),
    path("showcase/pitch-deck-generator/", showcase_features.ai_pitch_deck_generator, name="pitch_deck_generator"),
    path("showcase/business-plan-generator/", showcase_features.ai_business_plan_generator, name="business_plan_generator"),
]
