import random
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from apps.ideas.models import StartupIdea, Category
from apps.evaluation.models import Evaluation
from apps.core.models import StartupQuote, Testimonial
from apps.funding.models import Investor, Incubator
from apps.mentors.models import MentorProfile
from apps.community.models import SuccessStory, Podcast, Webinar
from apps.market.models import IndustryTrend, NewsArticle, LearningResource, JobPosting, Event


def seed_market_data():
    IndustryTrend.objects.get_or_create(name="Artificial Intelligence", defaults={"description": "AI is transforming every industry", "growth_rate": 35.5, "market_size": 150000})
    IndustryTrend.objects.get_or_create(name="FinTech", defaults={"description": "Digital payments and blockchain", "growth_rate": 25.3, "market_size": 300000})
    IndustryTrend.objects.get_or_create(name="HealthTech", defaults={"description": "Telemedicine and digital health", "growth_rate": 28.7, "market_size": 250000})
    IndustryTrend.objects.get_or_create(name="CleanTech", defaults={"description": "Renewable energy and sustainability", "growth_rate": 22.4, "market_size": 180000})
    IndustryTrend.objects.get_or_create(name="EdTech", defaults={"description": "Online learning platforms", "growth_rate": 18.9, "market_size": 120000})
    IndustryTrend.objects.get_or_create(name="E-Commerce", defaults={"description": "Online retail and D2C brands", "growth_rate": 15.2, "market_size": 500000})


def create_demo_data():
    seed_market_data()
    User = get_user_model()
    if User.objects.filter(username="demo_founder").exists():
        return False
    demo_user = User.objects.create(
        username="demo_founder",
        email="demo@creativespark.io",
        password=make_password("Demo@12345"),
        role="student",
        bio="Demo founder exploring Creative Spark features.",
    )
    mentor_user = User.objects.create(
        username="demo_mentor",
        email="mentor@creativespark.io",
        password=make_password("Demo@12345"),
        role="mentor",
        bio="Experienced startup mentor with 10+ years in tech.",
    )
    mentor, _ = MentorProfile.objects.get_or_create(user=mentor_user, defaults={
        "expertise": "Technology, AI, SaaS",
        "experience_years": 10,
        "company": "TechVentures Inc.",
        "designation": "Startup Advisor",
        "available": True,
        "bio": "I help early-stage startups find product-market fit and raise funding.",
    })
    cat, _ = Category.objects.get_or_create(name="Technology", slug="technology")
    idea_data = [
        {"name": "EcoTrack", "industry": "environment", "problem": "Businesses struggle to track and reduce their carbon footprint effectively", "solution": "An AI-powered platform that automatically tracks, reports, and suggests carbon reduction strategies", "customers": "Mid-to-large enterprises", "business_model": "SaaS subscription with tiered pricing", "revenue": "Monthly subscription fees + consulting", "usp": "Real-time AI-driven carbon tracking with automated compliance reporting", "competitors": "Manual carbon tracking tools", "investment": 500000, "team": "5 co-founders with experience in sustainability and AI", "timeline": "12 months"},
        {"name": "HealthSync", "industry": "healthcare", "problem": "Patients struggle to manage appointments, records, and prescriptions across different providers", "solution": "A unified health management platform integrating with existing healthcare systems", "customers": "Patients and healthcare providers", "business_model": "B2B SaaS for hospitals + B2C app", "revenue": "Hospital licensing + patient subscriptions", "usp": "Seamless integration with 100+ healthcare systems", "competitors": "MyChart, HealthTap", "investment": 1000000, "team": "8 members with healthcare and tech background", "timeline": "18 months"},
        {"name": "LearnFlow", "industry": "education", "problem": "Traditional online learning platforms lack personalized learning paths", "solution": "AI-driven adaptive learning platform that personalizes content for each student", "customers": "Students and educational institutions", "business_model": "Freemium + institutional licensing", "revenue": "Premium subscriptions + B2B licensing", "usp": "Dynamic learning paths that adapt in real-time", "competitors": "Coursera, Udemy", "investment": 300000, "team": "4 education technology experts", "timeline": "9 months"},
        {"name": "PayBridge", "industry": "finance", "problem": "Cross-border payments are slow, expensive, and opaque", "solution": "Blockchain-based cross-border payment platform with real-time settlement", "customers": "SMEs and freelancers", "business_model": "Transaction fee based", "revenue": "0.5% per transaction", "usp": "Real-time settlement at 10x lower cost", "competitors": "Wise, PayPal", "investment": 2000000, "team": "6 fintech veterans", "timeline": "24 months"},
        {"name": "GreenCart", "industry": "ecommerce", "problem": "Consumers want to shop sustainably but lack options and transparency", "solution": "Eco-friendly marketplace with verified sustainability ratings for every product", "customers": "Eco-conscious consumers", "business_model": "Commission-based marketplace", "revenue": "15% commission on sales", "usp": "Blockchain-verified sustainability scores", "competitors": "Amazon, Etsy", "investment": 750000, "team": "3 e-commerce specialists", "timeline": "15 months"},
    ]
    for i, data in enumerate(idea_data):
        idea = StartupIdea.objects.create(
            user=demo_user,
            category=cat,
            startup_name=data["name"],
            founder_name=f"Demo Founder {i+1}",
            industry=data["industry"],
            problem_statement=data["problem"],
            proposed_solution=data["solution"],
            target_customers=data["customers"],
            business_model=data["business_model"],
            revenue_model=data["revenue"],
            unique_selling_proposition=data["usp"],
            competitor_analysis=data["competitors"],
            required_investment=data["investment"],
            team_members=data["team"],
            expected_timeline=data["timeline"],
            status="approved",
            views_count=random.randint(50, 500),
            likes_count=random.randint(5, 50),
            is_trending=i < 2,
        )
        Evaluation.objects.create(
            idea=idea,
            innovation_score=random.randint(60, 95),
            feasibility_score=random.randint(55, 90),
            market_potential=random.randint(60, 95),
            scalability_score=random.randint(50, 90),
            risk_score=random.randint(50, 85),
            overall_rating=round(random.uniform(3.0, 5.0), 2),
            funding_probability=random.randint(40, 85),
        )
    StartupQuote.objects.get_or_create(quote="The best way to predict the future is to create it.", author="Peter Drucker", is_active=True)
    StartupQuote.objects.get_or_create(quote="Innovation distinguishes between a leader and a follower.", author="Steve Jobs", is_active=True)
    StartupQuote.objects.get_or_create(quote="Don't worry about failure; you only have to be right once.", author="Drew Houston", is_active=True)
    Testimonial.objects.get_or_create(name="Sarah Johnson", role="Startup Founder", content="Creative Spark helped me validate my idea and connect with the right mentors! I went from concept to MVP in just 3 months.", rating=5, is_active=True)
    Testimonial.objects.get_or_create(name="Michael Chen", role="Angel Investor", content="The AI evaluation tools are incredibly accurate. I've found some of my best investments through this platform.", rating=5, is_active=True)
    Investor.objects.get_or_create(name="Acme Ventures", investor_type="vc", description="Early-stage VC focusing on disruptive tech startups.", min_investment=500000, max_investment=5000000, preferred_stages="Seed, Series A", preferred_industries="Technology, Healthcare", is_active=True)
    Investor.objects.get_or_create(name="SeedFund Capital", investor_type="seed", description="Seed-stage fund supporting innovative ideas.", min_investment=50000, max_investment=500000, preferred_stages="Pre-seed, Seed", preferred_industries="Technology, Education, Healthcare", is_active=True)
    Investor.objects.get_or_create(name="Green Angels", investor_type="angel", description="Angel network focused on sustainable and eco-friendly startups.", min_investment=25000, max_investment=250000, preferred_stages="Seed", preferred_industries="Environment, Agriculture, CleanTech", is_active=True)
    Incubator.objects.get_or_create(name="TechStars Accelerator", incubator_type="accelerator", description="World-renowned startup accelerator program.", is_active=True)
    Incubator.objects.get_or_create(name="Y Combinator", incubator_type="accelerator", description="Leading startup accelerator providing seed funding and mentorship.", is_active=True)
    SuccessStory.objects.get_or_create(user=demo_user, title="From Idea to Launch in 6 Months", content="When I started my journey with Creative Spark, I had nothing but an idea. The AI evaluation helped me refine my concept...", achievement="Raised $2M in seed funding", is_approved=True, is_featured=True)
    Podcast.objects.get_or_create(title="Startup Stories: From Zero to Hero", description="Weekly podcast featuring founders who built successful startups from scratch.", audio_url="https://example.com/podcast1", is_published=True)
    Podcast.objects.get_or_create(title="The AI Entrepreneur", description="Exploring how AI is transforming entrepreneurship and startup building.", audio_url="https://example.com/podcast2", is_published=True)
    from django.utils import timezone
    from datetime import timedelta
    Webinar.objects.get_or_create(title="How to Build a Successful MVP", description="Learn the art of building minimum viable products that investors love.", presenter="John Smith", scheduled_date=timezone.now() + timedelta(days=7), is_active=True)
    Webinar.objects.get_or_create(title="Fundraising Masterclass", description="Everything you need to know about raising your first round of funding.", presenter="Jane Doe", scheduled_date=timezone.now() + timedelta(days=14), is_active=True)
    return True
