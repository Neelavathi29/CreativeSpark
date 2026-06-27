import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import ChatConversation, ChatMessage
from .ai_enhanced import (
    generate_startup_name,
    generate_business_plan,
    calculate_investor_readiness,
    calculate_valuation,
    compare_competitors,
    generate_executive_summary,
    calculate_funding_probability,
    chat_with_ai,
)
from apps.ideas.models import StartupIdea


@login_required
def ai_tools(request):
    name_result = None
    business_plan = None
    financials = None
    readiness = None
    competitor_data = None
    executive_summary = None
    funding_probability = None
    success_prediction = None

    ideas = StartupIdea.objects.filter(user=request.user)
    selected_idea = None

    idea_id = request.GET.get("idea")
    if idea_id:
        selected_idea = get_object_or_404(StartupIdea, pk=idea_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "generate_name":
            industry = request.POST.get("industry", "technology")
            name_result = generate_startup_name(industry)

        elif action == "business_plan":
            if selected_idea:
                business_plan, financials = generate_business_plan(
                    selected_idea
                )

        elif action == "investor_readiness":
            if selected_idea:
                readiness = calculate_investor_readiness(selected_idea)

        elif action == "competitor_analysis":
            if selected_idea:
                competitor_data = compare_competitors(selected_idea)

        elif action == "valuation":
            if selected_idea:
                valuation = calculate_valuation(selected_idea)
                return render(
                    request,
                    "evaluation/ai_tools.html",
                    {
                        "ideas": ideas,
                        "selected_idea": selected_idea,
                        "valuation": valuation,
                    },
                )

        elif action == "executive_summary":
            if selected_idea:
                executive_summary = generate_executive_summary(selected_idea)

        elif action == "funding_probability":
            if selected_idea:
                funding_probability = calculate_funding_probability(
                    selected_idea
                )

        elif action == "success_prediction":
            if selected_idea:
                evaluation = selected_idea.evaluations.first()
                if evaluation:
                    scores = {
                        "innovation": evaluation.innovation_score,
                        "feasibility": evaluation.feasibility_score,
                        "market_potential": evaluation.market_potential,
                        "scalability": evaluation.scalability_score,
                        "risk": evaluation.risk_score,
                        "overall": float(evaluation.overall_rating),
                        "funding_probability": (
                            evaluation.funding_probability or 0
                        ),
                    }
                    overall = float(evaluation.overall_rating)
                    if overall >= 4.0:
                        prediction = "Very High"
                    elif overall >= 3.0:
                        prediction = "High"
                    elif overall >= 2.0:
                        prediction = "Moderate"
                    else:
                        prediction = "Low"
                    success_prediction = {
                        "scores": scores,
                        "prediction": prediction,
                        "max_score": 5.0,
                    }

    context = {
        "ideas": ideas,
        "selected_idea": selected_idea,
        "name_result": name_result,
        "business_plan": business_plan,
        "financials": financials,
        "readiness": readiness,
        "competitor_data": competitor_data,
        "executive_summary": executive_summary,
        "funding_probability": funding_probability,
        "success_prediction": success_prediction,
        "industries": StartupIdea.INDUSTRY_CHOICES,
    }
    return render(request, "evaluation/ai_tools.html", context)


@login_required
def chatbot_view(request):
    conversations = ChatConversation.objects.filter(user=request.user)
    active_conversation = None
    conv_id = request.GET.get("conversation")

    if conv_id:
        active_conversation = get_object_or_404(
            ChatConversation, pk=conv_id, user=request.user
        )
    elif conversations.exists():
        active_conversation = conversations.first()

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        if message_text:
            if not active_conversation:
                active_conversation = ChatConversation.objects.create(
                    user=request.user, title=message_text[:50]
                )
            ChatMessage.objects.create(
                conversation=active_conversation,
                role="user",
                content=message_text,
            )
            response_text = chat_with_ai(message_text, request.user)
            ChatMessage.objects.create(
                conversation=active_conversation,
                role="assistant",
                content=response_text,
            )
            messages.success(request, "Response generated!")

    context = {
        "conversations": conversations,
        "active_conversation": active_conversation,
    }
    return render(request, "evaluation/chatbot.html", context)


@login_required
def chatbot_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)
    message_text = data.get("message", "").strip()
    conv_id = data.get("conversation_id")

    if not message_text:
        return JsonResponse({"error": "Message is required"}, status=400)

    if conv_id:
        conversation = get_object_or_404(
            ChatConversation, pk=conv_id, user=request.user
        )
    else:
        conversation = ChatConversation.objects.create(
            user=request.user, title=message_text[:50]
        )

    ChatMessage.objects.create(
        conversation=conversation, role="user", content=message_text
    )

    response_text = chat_with_ai(message_text, request.user)

    ChatMessage.objects.create(
        conversation=conversation, role="assistant", content=response_text
    )

    return JsonResponse(
        {
            "response": response_text,
            "conversation_id": conversation.id,
        }
    )


def voice_to_text(request):
    transcript = None
    if request.method == "POST":
        transcript = request.POST.get("transcript", "")
        if transcript:
            messages.success(request, "Voice input received!")
    return render(
        request, "evaluation/voice_to_text.html", {"transcript": transcript}
    )
