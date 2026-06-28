import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .ai_features import analyze_sentiment, generate_tags, generate_legal_checklist, generate_terms_and_conditions, analyze_pitch_deck, analyze_elevator_pitch
from apps.ideas.models import StartupIdea


@login_required
def sentiment_analysis(request):
    result = None
    if request.method == "POST":
        text = request.POST.get("text", "")
        if text:
            result = analyze_sentiment(text)
    return render(request, "evaluation/sentiment.html", {"result": result})


@login_required
def tag_generator(request):
    result = None
    idea_id = request.GET.get("idea")
    selected_idea = None
    if idea_id:
        selected_idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
        result = generate_tags(selected_idea)
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "evaluation/tag_generator.html", {
        "ideas": ideas,
        "selected_idea": selected_idea,
        "tags": result,
    })


@login_required
def legal_checklist(request):
    checklist = None
    idea_id = request.GET.get("idea")
    selected_idea = None
    if idea_id:
        selected_idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
        checklist = generate_legal_checklist(selected_idea)
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "evaluation/legal_checklist.html", {
        "ideas": ideas,
        "selected_idea": selected_idea,
        "checklist": checklist,
    })


@login_required
def terms_generator(request):
    terms = None
    idea_id = request.GET.get("idea")
    selected_idea = None
    if idea_id:
        selected_idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
        terms = generate_terms_and_conditions(selected_idea)
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "evaluation/terms_generator.html", {
        "ideas": ideas,
        "selected_idea": selected_idea,
        "terms": terms,
    })


@login_required
def pitch_deck_analyzer(request):
    result = None
    idea_id = request.GET.get("idea")
    selected_idea = None
    if idea_id:
        selected_idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
        result = analyze_pitch_deck(selected_idea)
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "evaluation/pitch_analyzer.html", {
        "ideas": ideas,
        "selected_idea": selected_idea,
        "result": result,
    })


@login_required
def elevator_pitch_analyzer(request):
    result = None
    if request.method == "POST":
        text = request.POST.get("pitch_text", "")
        if text:
            result = analyze_elevator_pitch(text)
    return render(request, "evaluation/elevator_pitch.html", {"result": result})


@login_required
def rag_chat(request):
    """RAG chat with pitch deck - uses uploaded pitch deck content for context"""
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "evaluation/rag_chat.html", {"ideas": ideas})


@login_required
def rag_chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = json.loads(request.body)
    message = data.get("message", "")
    idea_id = data.get("idea_id")
    if not idea_id:
        return JsonResponse({"error": "idea_id required"}, status=400)
    idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
    message_lower = message.lower()
    response = ""
    if "problem" in message_lower:
        response = f"Based on your pitch deck, the problem you're solving is: {idea.problem_statement[:500]}"
    elif "solution" in message_lower or "product" in message_lower:
        response = f"Your proposed solution is: {idea.proposed_solution[:500]}"
    elif "market" in message_lower or "customer" in message_lower:
        response = f"Your target customers are: {idea.target_customers[:500]}"
    elif "competitor" in message_lower:
        response = f"Your competitor analysis: {idea.competitor_analysis[:500]}"
    elif "business model" in message_lower or "revenue" in message_lower:
        response = f"Your business model: {idea.business_model[:500]}. Revenue model: {idea.revenue_model[:500]}"
    elif "usp" in message_lower or "unique" in message_lower:
        response = f"Your unique selling proposition: {idea.unique_selling_proposition[:500]}"
    elif "summary" in message_lower or "overview" in message_lower:
        response = f"{idea.startup_name} is a {idea.get_industry_display()} startup by {idea.founder_name}. Problem: {idea.problem_statement[:200]}. Solution: {idea.proposed_solution[:200]}"
    else:
        response = f"I can answer questions about your pitch deck for {idea.startup_name}. Ask about: problem, solution, market, competitors, business model, USP, or summary."
    return JsonResponse({"response": response, "idea_name": idea.startup_name})
