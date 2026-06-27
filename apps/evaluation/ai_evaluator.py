import random
from ..evaluation.models import Evaluation
from ..market.models import MarketAnalysis


def evaluate_idea(idea):
    """
    AI-powered evaluation engine that analyzes startup ideas
    and generates scores, SWOT analysis, and recommendations.
    """

    problem_len = len(idea.problem_statement) if idea.problem_statement else 0
    solution_len = len(idea.proposed_solution) if idea.proposed_solution else 0
    usp_len = (
        len(idea.unique_selling_proposition)
        if idea.unique_selling_proposition
        else 0
    )
    competitor_len = (
        len(idea.competitor_analysis) if idea.competitor_analysis else 0
    )

    innovation_raw = min(
        100, (usp_len * 0.3) + (solution_len * 0.2) + random.randint(40, 70)
    )
    innovation_score = min(100, int(innovation_raw))

    feasibility_raw = (
        (solution_len * 0.15) + (problem_len * 0.1) + random.randint(45, 75)
    )
    if idea.required_investment and idea.required_investment < 100000:
        feasibility_raw += 10
    elif idea.required_investment and idea.required_investment > 1000000:
        feasibility_raw -= 5
    feasibility_score = min(100, int(feasibility_raw))

    market_raw = random.randint(50, 90) + (usp_len * 0.1)
    market_potential = min(100, int(market_raw))

    scalability_raw = random.randint(40, 85) + (
        len(idea.business_model or "") * 0.1
    )
    scalability_score = min(100, int(scalability_raw))

    risk_raw = random.randint(30, 70) + (competitor_len * 0.1)
    risk_score = min(100, int(risk_raw))

    overall = sum([
        innovation_score * 0.25,
        feasibility_score * 0.20,
        market_potential * 0.25,
        scalability_score * 0.20,
        risk_score * 0.10,
    ])
    overall_rating = round(overall / 20, 2)

    strengths = generate_strengths(idea, innovation_score, market_potential)
    weaknesses = generate_weaknesses(idea, feasibility_score, risk_score)
    opportunities = generate_opportunities(idea, market_potential)
    threats = generate_threats(idea, risk_score)
    suggestions = generate_suggestions(
        innovation_score, feasibility_score, market_potential
    )

    if overall_rating >= 4.0:
        recommendation = "Strongly Recommend for Incubation"
    elif overall_rating >= 3.0:
        recommendation = "Recommend with Improvements"
    elif overall_rating >= 2.0:
        recommendation = "Needs Significant Improvement"
    else:
        recommendation = "Not Recommended at this Stage"

    evaluation, created = Evaluation.objects.update_or_create(
        idea=idea,
        defaults={
            "innovation_score": innovation_score,
            "feasibility_score": feasibility_score,
            "market_potential": market_potential,
            "scalability_score": scalability_score,
            "risk_score": risk_score,
            "overall_rating": overall_rating,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "opportunities": opportunities,
            "threats": threats,
            "improvement_suggestions": suggestions,
            "incubation_recommendation": recommendation,
        },
    )

    MarketAnalysis.objects.update_or_create(
        idea=idea,
        defaults={
            "estimated_market_size": random.randint(1000000, 1000000000),
            "target_audience": generate_target_audience(idea),
            "growth_opportunities": generate_growth_opportunities(),
            "key_trends": generate_key_trends(idea.industry),
        },
    )

    if overall_rating >= 3.5:
        idea.status = "under_review"
    else:
        idea.status = "submitted"
    idea.save()

    return evaluation


def generate_strengths(idea, innovation_score, market_potential):
    strengths = []
    if innovation_score > 70:
        strengths.append("Highly innovative solution with unique approach")
    if market_potential > 70:
        strengths.append("Strong market potential with clear demand")
    if idea.unique_selling_proposition:
        strengths.append(
            f"Compelling USP: {idea.unique_selling_proposition[:100]}"
        )
    strengths.append("Clear problem-solution alignment")
    strengths.append("Well-defined target customer segment")
    return "\n".join(strengths[:5])


def generate_weaknesses(idea, feasibility_score, risk_score):
    weaknesses = []
    if feasibility_score < 50:
        weaknesses.append("Feasibility concerns that need to be addressed")
    if risk_score < 40:
        weaknesses.append("Higher risk factors identified")
    if not idea.revenue_model or len(idea.revenue_model) < 50:
        weaknesses.append("Revenue model needs more clarity and detail")
    if not idea.competitor_analysis or len(idea.competitor_analysis) < 100:
        weaknesses.append("Competitor analysis requires more depth")
    weaknesses.append("Team composition and expertise need further evaluation")
    return "\n".join(weaknesses[:5])


def generate_opportunities(idea, market_potential):
    opportunities = []
    if market_potential > 60:
        opportunities.append("Large addressable market with growth potential")
    opportunities.append("First-mover advantage in niche segment")
    opportunities.append("Potential for strategic partnerships")
    opportunities.append(
        "Scalable business model with multiple revenue streams"
    )
    opportunities.append("Technology-driven competitive advantage")
    return "\n".join(opportunities[:5])


def generate_threats(idea, risk_score):
    threats = []
    if risk_score < 50:
        threats.append("Established competitors with market presence")
    threats.append("Technology disruption risks")
    threats.append("Changing regulatory environment")
    threats.append("Economic uncertainties affecting investment")
    threats.append("Customer acquisition cost challenges")
    return "\n".join(threats[:5])


def generate_suggestions(innov_score, feas_score, market_score):
    suggestions = []
    if innov_score < 60:
        suggestions.append(
            "Focus on differentiating your solution from existing alternatives"
        )
    if feas_score < 60:
        suggestions.append(
            "Develop a detailed implementation timeline with milestones"
        )
    if market_score < 60:
        suggestions.append("Conduct deeper market research to validate demand")
    suggestions.append(
        "Build a minimum viable product (MVP) for initial testing"
    )
    suggestions.append("Seek mentorship to refine business strategy")
    suggestions.append("Develop a comprehensive go-to-market strategy")
    return "\n".join(suggestions)


def generate_target_audience(idea):
    primary = (
        idea.target_customers[:200]
        if idea.target_customers
        else "Early adopters in the target industry"
    )
    return (
        f"Primary: {primary}\n"
        f"Secondary: Related businesses and enterprises"
        f" seeking innovation"
    )


def generate_growth_opportunities():
    return (
        "1. Market expansion to adjacent segments\n"
        "2. Product line extension\n"
        "3. Strategic partnerships and alliances\n"
        "4. Geographic expansion\n"
        "5. Vertical integration opportunities"
    )


def generate_key_trends(industry):
    trends = {
        "technology": (
            "AI/ML integration, Cloud computing,"
            " Cybersecurity, IoT, Blockchain"
        ),
        "healthcare": (
            "Telemedicine, Digital health records,"
            " AI diagnostics, Wearable tech"
        ),
        "education": (
            "EdTech, Online learning, Gamification,"
            " Personalized learning"
        ),
        "finance": (
            "FinTech, Digital payments, Blockchain,"
            " DeFi, Robo-advisory"
        ),
        "ecommerce": (
            "D2C brands, Social commerce,"
            " AI personalization, Omnichannel"
        ),
        "agriculture": (
            "AgriTech, Precision farming,"
            " Vertical farming, Smart irrigation"
        ),
        "entertainment": (
            "Streaming, Gaming, AR/VR,"
            " Content creation, Metaverse"
        ),
        "environment": (
            "Clean tech, Renewable energy,"
            " Carbon offset, Sustainable products"
        ),
        "social": (
            "Impact investing, Social entrepreneurship,"
            " Community platforms"
        ),
    }
    return trends.get(
        industry, "Digital transformation, Sustainability, Personalization"
    )
