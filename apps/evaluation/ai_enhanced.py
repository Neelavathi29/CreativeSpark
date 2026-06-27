import random


def generate_startup_name(industry, keywords=None):
    prefixes = [
        "Smart",
        "Neo",
        "Next",
        "Cloud",
        "Data",
        "Swift",
        "Bright",
        "Nova",
        "Apex",
        "Core",
        "Zen",
        "Flux",
        "Prime",
        "Vibe",
        "Pulse",
        "Spark",
    ]
    suffixes = [
        "Lab",
        "Hub",
        "Sync",
        "Mind",
        "Flow",
        "Wave",
        "Link",
        "Nest",
        "Core",
        "Wise",
        "Forge",
        "Bridge",
        "Space",
        "Up",
        "io",
        "AI",
    ]

    industry_prefixes = {
        "technology": ["Tech", "Cyber", "Digital", "Code", "Quantum"],
        "healthcare": ["Health", "Med", "Vital", "Care", "Life"],
        "education": ["Edu", "Learn", "Skill", "Mind", "Class"],
        "finance": ["Fin", "Pay", "Wealth", "Capital", "Ledger"],
        "ecommerce": ["Shop", "Cart", "Buy", "Trade", "Market"],
        "agriculture": ["Agri", "Farm", "Green", "Grow", "Harvest"],
        "environment": ["Eco", "Green", "Clean", "Sustain", "Nature"],
        "entertainment": ["Play", "Fun", "Media", "Story", "Game"],
        "social": ["Connect", "Together", "Unite", "Socia", "Tribe"],
        "other": ["New", "Future", "Global", "Vision", "First"],
    }

    ind_prefs = industry_prefixes.get(industry, ["New", "Future", "Global"])

    name_style = random.randint(1, 3)
    name_suffixes = ["ly", "ify", "ize", "able", "ico", "io", "ai"]
    if name_style == 1:
        name = f"{random.choice(ind_prefs)}{random.choice(suffixes)}"
    elif name_style == 2:
        name = f"{random.choice(prefixes)}{random.choice(ind_prefs)}"
    else:
        word = random.choice(ind_prefs)
        name = f"{word}{random.choice(name_suffixes)}"

    return name


def generate_business_plan(idea):
    sections = []

    industry = idea.get_industry_display()
    executive_summary = (
        f"{idea.startup_name} is a pioneering {industry} startup that "
        f"addresses {idea.problem_statement[:100].lower()}... "
        f"Through {idea.proposed_solution[:100].lower()}, "
        f"we aim to capture significant market share in the {industry} sector."
    )
    sections.append(("Executive Summary", executive_summary))

    market_opp = (
        f"The target market for {idea.startup_name} consists of "
        f"{idea.target_customers[:100]}. "
        f"With the growing demand in the {industry} industry, "
        f"we project strong adoption rates and market penetration."
    )
    sections.append(("Market Opportunity", market_opp))

    product = (
        f"Our core offering {idea.proposed_solution[:150].lower()} "
        f"Differentiated by {idea.unique_selling_proposition[:100]}, "
        f"our solution provides unique value to customers."
    )
    sections.append(("Product/Service Description", product))

    business_model = (
        f"{idea.business_model[:200]} "
        f"Our revenue streams include {idea.revenue_model[:150]}."
    )
    sections.append(("Business Model", business_model))

    competitors_summary = (
        f"Key competitors include {idea.competitor_analysis[:150]}. "
        "Our competitive advantage lies in our unique"
        " approach and technology."
    )
    sections.append(("Competitive Analysis", competitors_summary))

    financials = generate_financial_projection(idea.required_investment)

    return sections, financials


def generate_financial_projection(investment):
    base = float(investment)
    projections = []
    for year in range(1, 6):
        revenue = base * (0.5 + 0.5 * year) * random.uniform(0.8, 1.2)
        costs = base * 0.3 * (1 + 0.1 * year)
        profit = revenue - costs
        projections.append(
            {
                "year": year,
                "revenue": round(revenue, 2),
                "costs": round(costs, 2),
                "profit": round(profit, 2),
            }
        )
    return projections


def calculate_investor_readiness(idea):
    score = 0
    max_score = 100

    if idea.problem_statement and len(idea.problem_statement) > 50:
        score += 10
    if idea.proposed_solution and len(idea.proposed_solution) > 50:
        score += 10
    usp = idea.unique_selling_proposition
    if usp and len(usp) > 30:
        score += 10
    if idea.competitor_analysis and len(idea.competitor_analysis) > 50:
        score += 10
    if idea.business_model and len(idea.business_model) > 50:
        score += 10
    if idea.revenue_model and len(idea.revenue_model) > 30:
        score += 10
    if idea.target_customers and len(idea.target_customers) > 30:
        score += 10
    if idea.team_members and len(idea.team_members) > 20:
        score += 10
    if idea.pitch_deck:
        score += 10
    if idea.logo:
        score += 5
    if idea.required_investment > 0:
        score += 5

    score = min(score, max_score)

    level = (
        "Seed"
        if score < 40
        else "Early" if score < 60 else "Growth" if score < 80 else "Scale"
    )

    return {
        "score": score,
        "level": level,
        "max_score": max_score,
        "gaps": get_readiness_gaps(score, idea),
    }


def get_readiness_gaps(score, idea):
    gaps = []
    if not idea.pitch_deck:
        gaps.append("Upload a pitch deck presentation")
    if not idea.logo:
        gaps.append("Add a company logo")
    if not idea.team_members or len(idea.team_members) < 20:
        gaps.append("Provide detailed team member information")
    if score < 50:
        gaps.append(
            "Strengthen your problem statement and" " solution description"
        )
        gaps.append("Develop a more detailed business model")
    if score < 70:
        gaps.append("Include financial projections")
        gaps.append("Add more detail to competitor analysis")
    return gaps


def calculate_valuation(idea):
    investment = (
        float(idea.required_investment)
        if idea.required_investment > 0
        else 50000
    )
    eval_score = 0
    evaluation = idea.evaluations.first()
    if evaluation:
        eval_score = float(evaluation.overall_rating) * 20

    base_value = investment * (3 + eval_score / 100 * 10)
    industry_multiplier = {
        "technology": 8,
        "healthcare": 7,
        "education": 5,
        "finance": 9,
        "ecommerce": 6,
        "agriculture": 4,
        "entertainment": 7,
        "environment": 6,
        "social": 4,
        "other": 5,
    }
    mult = industry_multiplier.get(idea.industry, 5)
    valuation = base_value * mult / 5
    return round(valuation, 2)


def generate_executive_summary(idea):
    summary = (
        f"Executive Summary\n\n"
        f"{idea.startup_name} is an innovative"
        f" {idea.get_industry_display()} startup "
        f"founded by {idea.founder_name}. The venture addresses"
        f" a critical problem: "
        f"{idea.problem_statement[:200]}.\n\n"
        f"Solution\n"
        f"{idea.startup_name} proposes {idea.proposed_solution[:200]}, "
        f"targeting {idea.target_customers[:150]}. "
        f"The unique selling proposition is"
        f" {idea.unique_selling_proposition[:150]}.\n\n"
        f"Market Opportunity\n"
        f"Operating in the {idea.get_industry_display()} sector, "
        f"{idea.startup_name} has identified a substantial"
        f" market opportunity. "
        f"The business model relies on {idea.business_model[:150]}, "
        f"with revenue generated through {idea.revenue_model[:100]}.\n\n"
        f"Competitive Advantage\n"
        f"Analysis of the competitive landscape reveals:"
        f" {idea.competitor_analysis[:200]}. "
        f"{idea.startup_name} differentiates itself through"
        f" its unique approach.\n\n"
        f"Financial Projection\n"
        f"The venture requires an initial investment of"
        f" ${idea.required_investment:,}. "
        f"The expected timeline to market is"
        f" {idea.expected_timeline}."
    )
    evaluation = idea.evaluations.first()
    if evaluation:
        rec = evaluation.incubation_recommendation
        if not rec:
            rec = "Proceed with development"
        summary += (
            f"\n\nAI Evaluation Summary\n"
            f"Innovation Score: {evaluation.innovation_score}/100\n"
            f"Market Potential: {evaluation.market_potential}/100\n"
            f"Overall Rating: {evaluation.overall_rating}/5\n"
            f"Recommendation: {rec}"
        )
    return summary


def calculate_funding_probability(idea):
    evaluation = idea.evaluations.first()
    if not evaluation:
        return {"probability": 50, "factors": ["No evaluation data available"]}

    base = float(evaluation.overall_rating) * 20
    innovation = evaluation.innovation_score * 0.25
    market = evaluation.market_potential * 0.25
    feasibility = evaluation.feasibility_score * 0.20
    scalability = evaluation.scalability_score * 0.15
    risk = evaluation.risk_score * 0.15

    score = (
        innovation + market + feasibility + scalability + risk
    ) * 0.8 + base * 0.2
    score = min(100, max(0, score))

    factors = []
    if evaluation.innovation_score > 70:
        factors.append("Strong innovation score")
    if evaluation.market_potential > 70:
        factors.append("Excellent market potential")
    if evaluation.feasibility_score < 50:
        factors.append("Feasibility needs improvement")
    if evaluation.risk_score < 50:
        factors.append("Risk factors need addressing")
    if idea.pitch_deck:
        factors.append("Professional pitch deck available")
    if float(idea.required_investment) < 100000:
        factors.append("Lower funding requirement reduces risk")

    return {
        "score": round(score, 1),
        "level": ("High" if score > 70 else "Medium" if score > 40 else "Low"),
        "factors": factors,
    }


def generate_investment_growth(
    initial_investment, annual_growth_rate=15, years=10
):
    projections = []
    for year in range(1, years + 1):
        value = initial_investment * ((1 + annual_growth_rate / 100) ** year)
        projections.append(
            {
                "year": year,
                "value": round(value, 2),
            }
        )
    return projections


def compare_competitors(idea):
    competitors_data = [
        {
            "name": "Market Leader A",
            "strength": 85,
            "market_share": 30,
            "strengths": "Strong brand, Large customer base,"
            " Extensive resources",
        },
        {
            "name": "Competitor B",
            "strength": 65,
            "market_share": 20,
            "strengths": "Innovative features, Good UX, Agile team",
        },
        {
            "name": "Competitor C",
            "strength": 45,
            "market_share": 10,
            "strengths": "Low pricing, Niche focus,"
            " Strong in specific segments",
        },
    ]
    our_strength = 0
    evaluation = idea.evaluations.first()
    if evaluation:
        s1 = evaluation.innovation_score + evaluation.market_potential
        our_strength = (s1 + evaluation.scalability_score) / 3
    else:
        our_strength = random.randint(50, 80)

    sorted_competitors = sorted(
        competitors_data, key=lambda c: c["strength"], reverse=True
    )
    our_rank = 1
    for c in sorted_competitors:
        if our_strength < c["strength"]:
            our_rank += 1
    return {
        "competitors": competitors_data,
        "our_strength": round(our_strength, 1),
        "our_ranking": our_rank,
    }


def chat_with_ai(message, user, conversation=None):
    message_lower = message.lower()

    if "startup" in message_lower and "name" in message_lower:
        industries = [
            "technology",
            "healthcare",
            "education",
            "finance",
            "ecommerce",
        ]
        names = [
            generate_startup_name(random.choice(industries)) for _ in range(3)
        ]
        response = (
            f"Here are some startup name ideas:\n1. {names[0]}\n2."
            f" {names[1]}\n3. {names[2]}\n\n"
            f"Would you like more suggestions for a specific industry?"
        )
    elif "funding" in message_lower or "investor" in message_lower:
        response = (
            "Great question about funding! Here are some tips:\n\n"
            "1. **Angel Investors**: Ideal for early-stage"
            " startups ($10K-$100K)\n"
            "2. **Venture Capital**: For high-growth"
            " startups ($500K+)\n"
            "3. **Seed Funds**: Early-stage funding ($50K-$500K)\n"
            "4. **Government Grants**: Non-dilutive funding"
            " for innovation\n"
            "5. **Bootstrapping**: Self-funding"
            " to maintain control\n\n"
            "Would you like me to elaborate on any of these?"
        )
    elif "evaluation" in message_lower or "score" in message_lower:
        response = (
            "Our AI evaluation engine assesses startups"
            " across 5 dimensions:\n\n"
            "📊 **Innovation (25%)** - How novel is your solution?\n"
            "📊 **Feasibility (20%)** - Can it be built?\n"
            "📊 **Market Potential (25%)** - Is there demand?\n"
            "📊 **Scalability (20%)** - Can it grow?\n"
            "📊 **Risk Assessment (10%)** - What are the challenges?\n\n"
            "Submit your startup idea to get a comprehensive AI evaluation!"
        )
    elif "market" in message_lower or "industry" in message_lower:
        response = (
            "Market analysis is crucial for startup success."
            " Key areas to research:\n\n"
            "🔍 **Total Addressable Market (TAM)**\n"
            "🔍 **Serviceable Available Market (SAM)**\n"
            "🔍 **Serviceable Obtainable Market (SOM)**\n"
            "🔍 **Competitor Analysis**\n"
            "🔍 **Customer Segmentation**\n\n"
            "Use our Market Analysis tool to get industry insights!"
        )
    elif "idea" in message_lower or "submit" in message_lower:
        response = (
            "To submit a startup idea on Creative Spark:\n\n"
            "1. Click 'Submit Idea' in the sidebar\n"
            "2. Fill in your startup details (problem, solution, market)\n"
            "3. Upload your pitch deck (optional)\n"
            "4. Submit for AI evaluation\n\n"
            "Our AI will analyze your idea across multiple dimensions!"
        )
    elif "mentor" in message_lower:
        response = (
            "Our mentorship program connects you with"
            " experienced professionals.\n\n"
            "✨ Browse available mentors in the Mentors section\n"
            "✨ Book one-on-one sessions\n"
            "✨ Get feedback on your startup\n"
            "✨ Join discussions with industry experts\n\n"
            "Check out the Mentors page to find your perfect match!"
        )
    elif any(
        kw in message_lower for kw in ("badge", "achievement", "xp")
    ):
        response = (
            "🎮 **Gamification System**:\n\n"
            "Earn XP by:\n"
            "- Submitting startup ideas (+50 XP)\n"
            "- Getting ideas approved (+100 XP)\n"
            "- Booking mentorship sessions (+30 XP)\n"
            "- Commenting on ideas (+10 XP)\n"
            "- Completing challenges (+Varies)\n\n"
            "Unlock badges and climb the leaderboard!"
        )
    elif "pitch" in message_lower or "deck" in message_lower:
        response = (
            "Tips for a great pitch deck:\n\n"
            "1. **Problem Slide**: Clearly define the problem\n"
            "2. **Solution Slide**: Show your unique approach\n"
            "3. **Market Size**: Demonstrate the opportunity\n"
            "4. **Business Model**: How will you make money?\n"
            "5. **Traction**: Show progress and milestones\n"
            "6. **Team**: Why is your team the best?\n\n"
            "Keep it under 10-12 slides and practice your delivery!"
        )
    elif any(
        kw in message_lower for kw in ("help", "what", "hello", "hi")
    ):
        response = (
            "👋 Welcome to Creative Spark AI Assistant!"
            " I can help you with:\n\n"
            "💡 **Startup Names** - Generate creative startup name ideas\n"
            "💰 **Funding Advice** - Learn about funding options\n"
            "📊 **Evaluation Info** - How our AI evaluates ideas\n"
            "📈 **Market Analysis** - Understanding your market\n"
            "📝 **Idea Submission** - How to submit your startup\n"
            "👥 **Mentorship** - Finding and booking mentors\n"
            "🏆 **Gamification** - Badges, XP, and achievements\n"
            "🎯 **Pitch Decks** - Tips for great presentations\n\n"
            "What would you like to know about?"
        )
    else:
        response = (
            f"I understand you're asking about '{message[:50]}'. "
            f"I can help you with startup naming, funding advice,"
            f" market analysis, "
            f"idea evaluation, mentorship, and more."
            f" What specific area interests you?"
        )

    return response
