import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.ideas.models import StartupIdea
from apps.evaluation.models import Evaluation
from apps.funding.models import Investor, FundingApplication


def api_docs(request):
    return render(request, "api/docs.html")


def api_health(request):
    return JsonResponse({"status": "healthy", "version": "1.0.0", "service": "Creative Spark API"})


def get_token(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if user:
            import hashlib
            import hmac
            token = hashlib.sha256(f"{user.username}:{user.password[:20]}:creativespark2026".encode()).hexdigest()
            return JsonResponse({"token": token, "user_id": user.id, "username": user.username})
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "POST required"}, status=405)


def api_ideas_list(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return JsonResponse({"error": "Authorization required"}, status=401)
    ideas = StartupIdea.objects.filter(status="approved")
    data = []
    for idea in ideas:
        data.append({
            "id": idea.id,
            "name": idea.startup_name,
            "industry": idea.get_industry_display(),
            "problem": idea.problem_statement[:200],
            "solution": idea.proposed_solution[:200],
            "views": idea.views_count,
            "likes": idea.likes_count,
            "created_at": idea.created_at.isoformat(),
        })
    return JsonResponse({"count": len(data), "results": data})


def api_idea_detail(request, pk):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return JsonResponse({"error": "Authorization required"}, status=401)
    try:
        idea = StartupIdea.objects.get(pk=pk)
    except StartupIdea.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    data = {
        "id": idea.id,
        "name": idea.startup_name,
        "founder": idea.founder_name,
        "industry": idea.get_industry_display(),
        "problem": idea.problem_statement,
        "solution": idea.proposed_solution,
        "target_customers": idea.target_customers,
        "business_model": idea.business_model,
        "usp": idea.unique_selling_proposition,
        "required_investment": float(idea.required_investment),
        "status": idea.status,
        "views": idea.views_count,
        "likes": idea.likes_count,
        "created_at": idea.created_at.isoformat(),
    }
    eval_obj = idea.evaluations.first()
    if eval_obj:
        data["evaluation"] = {
            "innovation": eval_obj.innovation_score,
            "feasibility": eval_obj.feasibility_score,
            "market_potential": eval_obj.market_potential,
            "scalability": eval_obj.scalability_score,
            "risk": eval_obj.risk_score,
            "overall": float(eval_obj.overall_rating),
        }
    return JsonResponse(data)


def api_investors(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return JsonResponse({"error": "Authorization required"}, status=401)
    investors = Investor.objects.filter(is_active=True)
    data = [{
        "id": inv.id,
        "name": inv.name,
        "type": inv.get_investor_type_display(),
        "min_investment": float(inv.min_investment),
        "max_investment": float(inv.max_investment),
        "location": inv.location,
    } for inv in investors]
    return JsonResponse({"count": len(data), "results": data})


@csrf_exempt
def api_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event = data.get("event", "unknown")
            payload = data.get("payload", {})
            return JsonResponse({"status": "received", "event": event})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "POST required"}, status=405)


def api_webhooks_docs(request):
    return render(request, "api/webhooks_docs.html")


def api_keys_page(request):
    return render(request, "api/api_keys.html")


@login_required
def api_integrations(request):
    return render(request, "api/integrations.html")
