import random
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .ai_enhanced import calculate_investor_readiness, calculate_funding_probability
from .ai_features import generate_tags
from apps.ideas.models import StartupIdea
from apps.analytics.models import StartupHealthScore
from apps.evaluation.models import Evaluation


def calculate_readiness_meter(idea):
    evaluation = idea.evaluations.first()
    if not evaluation:
        return {"score": 0, "level": "Not Evaluated", "color": "#6c757d"}
    scores = {
        "innovation": evaluation.innovation_score,
        "feasibility": evaluation.feasibility_score,
        "market": evaluation.market_potential,
        "scalability": evaluation.scalability_score,
        "risk": evaluation.risk_score,
    }
    weighted = scores["innovation"] * 0.25 + scores["feasibility"] * 0.20 + scores["market"] * 0.25 + scores["scalability"] * 0.20 + scores["risk"] * 0.10
    score = min(100, int(weighted))
    if score >= 80:
        level = "Investment Ready"
        color = "#198754"
    elif score >= 60:
        level = "Growth Stage"
        color = "#0d6efd"
    elif score >= 40:
        level = "Early Stage"
        color = "#ffc107"
    else:
        level = "Idea Stage"
        color = "#dc3545"
    return {"score": score, "level": level, "color": color, "scores": scores}


def calculate_dna_score(idea):
    evaluation = idea.evaluations.first()
    health = StartupHealthScore.objects.filter(idea=idea).first()
    dna = {
        "founder_match": random.randint(60, 95),
        "problem_fit": random.randint(55, 95),
        "solution_fit": random.randint(50, 95),
        "market_fit": (evaluation.market_potential if evaluation else 50),
        "team_capability": (evaluation.feasibility_score if evaluation else 50),
        "execution_ability": (evaluation.scalability_score if evaluation else 50),
    }
    if health:
        dna["financial_health"] = health.financial_score
    else:
        dna["financial_health"] = 50
    overall = int(sum(dna.values()) / len(dna))
    return {"dimensions": dna, "overall": overall}


def calculate_unicorn_potential(idea):
    evaluation = idea.evaluations.first()
    if not evaluation:
        return {"score": 0, "potential": "Unknown", "factors": []}
    innovation_weight = evaluation.innovation_score * 0.30
    market_weight = evaluation.market_potential * 0.30
    scalability_weight = evaluation.scalability_score * 0.25
    risk_weight = (100 - evaluation.risk_score) * 0.15
    score = int(innovation_weight + market_weight + scalability_weight + risk_weight)
    if score >= 85:
        potential = "Unicorn Potential"
    elif score >= 70:
        potential = "High Growth"
    elif score >= 50:
        potential = "Promising"
    else:
        potential = "Early Stage"
    factors = []
    if evaluation.innovation_score >= 75:
        factors.append("High innovation")
    if evaluation.market_potential >= 75:
        factors.append("Large market opportunity")
    if evaluation.scalability_score >= 75:
        factors.append("Strong scalability")
    return {"score": score, "potential": potential, "factors": factors}


def calculate_maturity_index(idea):
    total = 0
    max_score = 100
    if idea.problem_statement and len(idea.problem_statement) > 100:
        total += 10
    if idea.proposed_solution and len(idea.proposed_solution) > 100:
        total += 10
    if idea.target_customers:
        total += 10
    if idea.business_model:
        total += 10
    if idea.revenue_model:
        total += 10
    if idea.competitor_analysis:
        total += 10
    if idea.unique_selling_proposition:
        total += 10
    if idea.pitch_deck:
        total += 10
    if idea.logo:
        total += 5
    if idea.required_investment > 0:
        total += 5
    evaluation = idea.evaluations.first()
    if evaluation:
        total += 5
        if evaluation.funding_probability and evaluation.funding_probability > 50:
            total += 5
    stages = ["Idea", "Validation", "Early Traction", "Growth", "Scale"]
    stage_idx = min(4, total // 20)
    return {"score": min(100, total), "stage": stages[stage_idx], "max": max_score}


def calculate_incubation_eligibility(idea):
    score = 0
    if idea.problem_statement and len(idea.problem_statement) > 50:
        score += 15
    if idea.proposed_solution and len(idea.proposed_solution) > 50:
        score += 15
    if idea.unique_selling_proposition:
        score += 10
    if idea.business_model:
        score += 10
    if idea.target_customers:
        score += 10
    if idea.competitor_analysis:
        score += 10
    if idea.team_members and len(idea.team_members) > 20:
        score += 10
    if idea.pitch_deck:
        score += 10
    if idea.logo:
        score += 5
    if idea.required_investment > 0:
        score += 5
    readiness = calculate_investor_readiness(idea)
    score = min(100, score + readiness["score"] // 5)
    if score >= 75:
        recommendation = "Highly Recommended"
    elif score >= 50:
        recommendation = "Eligible"
    else:
        recommendation = "Needs Improvement"
    return {"score": score, "recommendation": recommendation}


def calculate_sustainability_impact(idea):
    industry = idea.industry
    base_scores = {
        "technology": 50,
        "healthcare": 65,
        "education": 70,
        "finance": 40,
        "ecommerce": 45,
        "agriculture": 80,
        "environment": 90,
        "entertainment": 35,
        "social": 75,
        "other": 50,
    }
    base = base_scores.get(industry, 50)
    variance = random.randint(-10, 15)
    score = min(100, max(0, base + variance))
    badges = []
    if score >= 80:
        badges.append("Eco-Impact Leader")
    if score >= 60:
        badges.append("Sustainability Certified")
    if "green" in (idea.proposed_solution or "").lower() or "eco" in (idea.proposed_solution or "").lower():
        badges.append("Green Innovation")
        score = min(100, score + 10)
    return {"score": score, "badges": badges}


@login_required
def innovation_radar(request, idea_id):
    idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
    evaluation = idea.evaluations.first()
    if not evaluation:
        messages.error(request, "No evaluation data available.")
        return redirect("idea_detail", pk=idea_id)
    radar_data = {
        "innovation": evaluation.innovation_score,
        "feasibility": evaluation.feasibility_score,
        "market": evaluation.market_potential,
        "scalability": evaluation.scalability_score,
        "risk": evaluation.risk_score,
    }
    context = {
        "idea": idea,
        "radar_data": radar_data,
        "readiness": calculate_readiness_meter(idea),
        "dna": calculate_dna_score(idea),
        "unicorn": calculate_unicorn_potential(idea),
        "maturity": calculate_maturity_index(idea),
        "incubation": calculate_incubation_eligibility(idea),
        "sustainability": calculate_sustainability_impact(idea),
    }
    return render(request, "evaluation/innovation_radar.html", context)


def generate_ai_pitch_deck(idea):
    sections = [
        {"title": "Title Slide", "content": f"{idea.startup_name}\n{idea.get_industry_display()} Startup\nFounded by {idea.founder_name}"},
        {"title": "Problem", "content": idea.problem_statement[:300]},
        {"title": "Solution", "content": idea.proposed_solution[:300]},
        {"title": "Target Market", "content": f"Target Customers: {idea.target_customers[:200]}" if idea.target_customers else "Not specified"},
        {"title": "Unique Value Proposition", "content": idea.unique_selling_proposition[:300] if idea.unique_selling_proposition else "Not specified"},
        {"title": "Business Model", "content": f"{idea.business_model[:200]}\nRevenue: {idea.revenue_model[:200]}"},
        {"title": "Market Size & Opportunity", "content": f"Industry: {idea.get_industry_display()}\nCompetition: {idea.competitor_analysis[:200] if idea.competitor_analysis else 'Not specified'}"},
        {"title": "Financials", "content": f"Required Investment: ${idea.required_investment:,}\nTimeline: {idea.expected_timeline}"},
        {"title": "Team", "content": idea.team_members[:300] if idea.team_members else "Not specified"},
        {"title": "Contact", "content": f"Thank you!\n{idea.startup_name}\nContact: {idea.user.email if idea.user else 'Not specified'}"},
    ]
    evaluation = idea.evaluations.first()
    if evaluation:
        sections.append({"title": "AI Evaluation", "content": f"Innovation: {evaluation.innovation_score}/100\nMarket: {evaluation.market_potential}/100\nOverall: {evaluation.overall_rating}/5.0"})
    return sections


@login_required
def ai_pitch_deck_generator(request):
    result = None
    idea_id = request.GET.get("idea")
    selected_idea = None
    if idea_id:
        selected_idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
        result = generate_ai_pitch_deck(selected_idea)
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "evaluation/pitch_deck_generator.html", {
        "ideas": ideas,
        "selected_idea": selected_idea,
        "pitch_deck_sections": result,
    })


@login_required
def ai_business_plan_generator(request):
    result = None
    idea_id = request.GET.get("idea")
    selected_idea = None
    if idea_id:
        selected_idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
        from .ai_enhanced import generate_business_plan
        result, financials = generate_business_plan(selected_idea)
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "evaluation/business_plan_generator.html", {
        "ideas": ideas,
        "selected_idea": selected_idea,
        "business_plan": result,
    })
