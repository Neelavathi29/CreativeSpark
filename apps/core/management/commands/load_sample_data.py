from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.ideas.models import Category, StartupIdea
from apps.evaluation.models import FundingTip, Evaluation
from apps.market.models import IndustryTrend
from apps.core.models import Testimonial, StartupQuote
from apps.gamification.models import Badge, UserXP
from apps.funding.models import Investor

User = get_user_model()


class Command(BaseCommand):
    help = "Load sample data for Creative Spark platform"

    def handle(self, *args, **kwargs):
        self.stdout.write("Loading sample data...")

        if User.objects.filter(username="admin").exists():
            self.stdout.write("Data already loaded, skipping.")
            return

        admin = User.objects.create_superuser(
            "admin", "admin@creativespark.io", "admin123"
        )
        admin.role = "admin"
        admin.first_name = "Admin"
        admin.last_name = "User"
        admin.save()

        student = User.objects.create_user(
            "student1", "student1@test.com", "student123"
        )
        student.role = "student"
        student.first_name = "John"
        student.last_name = "Doe"
        student.bio = (
            "Aspiring entrepreneur passionate about technology and innovation."
        )
        student.skills = "Python, JavaScript, UI/UX Design, Business Strategy"
        student.education = "B.Tech in Computer Science"
        student.save()

        student2 = User.objects.create_user(
            "student2", "student2@test.com", "student123"
        )
        student2.role = "student"
        student2.first_name = "Sarah"
        student2.last_name = "Johnson"
        student2.bio = (
            "Serial entrepreneur with a passion for sustainable solutions."
        )
        student2.skills = "Marketing, Finance, Operations, Leadership"
        student2.save()

        mentor_user = User.objects.create_user(
            "mentor1", "mentor1@test.com", "mentor123"
        )
        mentor_user.role = "mentor"
        mentor_user.first_name = "Mike"
        mentor_user.last_name = "Chen"
        mentor_user.bio = "Experienced startup advisor and angel investor."
        mentor_user.skills = "Venture Capital, Product Strategy, Leadership"
        mentor_user.save()

        from apps.mentors.models import MentorProfile

        MentorProfile.objects.create(
            user=mentor_user,
            expertise=(
                "Product Strategy, Fundraising,"
                " Business Model Design, Go-to-Market"
            ),
            experience_years=15, company="Spark Ventures",
            designation="Managing Partner", available=True, hourly_rate=150,
            bio=(
                "Helped 50+ startups raise over $100M in funding."
                " Passionate about nurturing early-stage companies."
            ),
            total_sessions=120, rating=4.8,
        )

        categories = [
            {
                "name": "Artificial Intelligence",
                "slug": "ai",
                "icon": "bi-cpu",
            },
            {
                "name": "HealthTech",
                "slug": "healthtech",
                "icon": "bi-heart-pulse",
            },
            {"name": "EdTech", "slug": "edtech", "icon": "bi-book"},
            {
                "name": "FinTech",
                "slug": "fintech",
                "icon": "bi-currency-dollar",
            },
            {"name": "GreenTech", "slug": "greentech", "icon": "bi-tree"},
            {"name": "E-Commerce", "slug": "ecommerce", "icon": "bi-cart"},
            {
                "name": "Social Impact",
                "slug": "social-impact",
                "icon": "bi-heart",
            },
            {"name": "SaaS", "slug": "saas", "icon": "bi-cloud"},
        ]

        for cat in categories:
            Category.objects.create(**cat)

        idea1 = StartupIdea.objects.create(
            user=student, category=Category.objects.get(slug="ai"),
            startup_name="SmartLearn AI", founder_name="John Doe",
            industry="education",
            problem_statement=(
                "Students struggle with personalized learning paths"
                " and adaptive content delivery. Traditional education"
                " systems fail to cater to individual learning paces"
                " and styles, leading to disengagement and poor outcomes."
            ),
            proposed_solution=(
                "An AI-powered adaptive learning platform that creates"
                " personalized learning paths, identifies knowledge gaps,"
                " and delivers customized content in real-time based on"
                " student performance and learning style."
            ),
            target_customers=(
                "K-12 students, college students, lifelong learners,"
                " educational institutions"
            ),
            business_model=(
                "Freemium + B2B SaaS subscriptions for institutions."
                " Premium features for individual learners."
            ),
            revenue_model=(
                "Monthly/Annual subscriptions ($9.99-$49.99),"
                " Institutional licensing ($5000+/year),"
                " Premium tutoring marketplace commission (20%)"
            ),
            competitor_analysis=(
                "Competitors include Khan Academy (free, limited AI),"
                " Coursera (course-based, not adaptive), Duolingo"
                " (gamified but limited subjects), and Byju's"
                " (video-based). None offer true AI-powered adaptive"
                " learning across multiple subjects."
            ),
            unique_selling_proposition=(
                "Real-time adaptive learning using proprietary AI"
                " that analyzes learning patterns, predicts knowledge"
                " gaps, and creates dynamic learning paths unique to"
                " each student."
            ),
            required_investment=500000,
            team_members=(
                "John Doe (CEO), Jane Smith (CTO),"
                " Alex Brown (AI Lead), Lisa Wang (Education Specialist)"
            ),
            expected_timeline="18 months to full launch", status="approved",
            is_trending=True,
        )

        Evaluation.objects.create(
            idea=idea1, innovation_score=88, feasibility_score=75,
            market_potential=85, scalability_score=82, risk_score=70,
            overall_rating=4.2,
            strengths=(
                "Highly innovative AI solution\n"
                "Strong market demand\n"
                "Clear revenue model\nExperienced team"
            ),
            weaknesses=(
                "High initial development cost\n"
                "Dependency on quality training data\n"
                "Competitive market"
            ),
            opportunities=(
                "Growing EdTech market\n"
                "Remote learning trends\n"
                "International expansion potential"
            ),
            threats=(
                "Established competitors\n"
                "Data privacy regulations\nTechnology changes"
            ),
            improvement_suggestions=(
                "Start with MVP focused on one subject\n"
                "Partner with schools for pilot programs\n"
                "Develop offline learning capabilities"
            ),
            incubation_recommendation="Strongly Recommend for Incubation",
        )

        idea2 = StartupIdea.objects.create(
            user=student2, category=Category.objects.get(slug="greentech"),
            startup_name="EcoTrack Solutions", founder_name="Sarah Johnson",
            industry="environment",
            problem_statement=(
                "Businesses lack effective tools to measure, track,"
                " and reduce their carbon footprint. Current solutions"
                " are either too expensive for SMEs or lack"
                " comprehensive features."
            ),
            proposed_solution=(
                "An affordable SaaS platform that helps businesses"
                " track their carbon emissions, set reduction targets,"
                " and generate sustainability reports using IoT sensors"
                " and AI analytics."
            ),
            target_customers=(
                "SMEs, manufacturing companies, logistics firms,"
                " corporate sustainability teams"
            ),
            business_model=(
                "SaaS subscription tiers based on company size"
                " and features required."
            ),
            revenue_model=(
                "Monthly subscriptions ($199-$999),"
                " Implementation consulting ($5000+),"
                " Carbon credit marketplace commission (15%)"
            ),
            competitor_analysis=(
                "Major competitors include Salesforce Sustainability"
                " Cloud (expensive), Plan A (limited features),"
                " and Carbon Trust (consulting heavy). None offer"
                " affordable end-to-end solution for SMEs."
            ),
            unique_selling_proposition=(
                "Affordable, all-in-one carbon management platform"
                " with AI-powered insights and automated reporting,"
                " specifically designed for SMEs."
            ),
            required_investment=350000,
            team_members=(
                "Sarah Johnson (CEO), Tom Green (CTO),"
                " Emma Wilson (Sustainability Lead)"
            ),
            expected_timeline="12 months to MVP", status="under_review",
            is_trending=True,
        )

        Evaluation.objects.create(
            idea=idea2, innovation_score=78, feasibility_score=82,
            market_potential=90, scalability_score=85, risk_score=75,
            overall_rating=4.1,
            strengths=(
                "Strong market need\n"
                "Excellent timing with ESG trends\n"
                "Scalable SaaS model\nClear revenue streams"
            ),
            weaknesses=(
                "Requires hardware integration\n"
                "Customer education needed\n"
                "Regulatory compliance complexity"
            ),
            opportunities=(
                "Net-zero regulations driving demand\n"
                "Growing ESG investing\nEnterprise partnerships"
            ),
            threats=(
                "Tech giants entering space\n"
                "Changing regulations\n"
                "Competition from free tools"
            ),
            improvement_suggestions=(
                "Start with software-only solution\n"
                "Build partnerships with sensor manufacturers\n"
                "Focus on one industry vertical first"
            ),
            incubation_recommendation="Strongly Recommend for Incubation",
        )

        StartupIdea.objects.create(
            user=student, category=Category.objects.get(slug="healthtech"),
            startup_name="MediConnect", founder_name="John Doe",
            industry="healthcare",
            problem_statement=(
                "Patients struggle to access their medical records"
                " across different healthcare providers, leading to"
                " fragmented care and repeated tests."
            ),
            proposed_solution=(
                "A blockchain-based platform that creates a unified"
                " health record system accessible by patients and"
                " authorized providers."
            ),
            target_customers=(
                "Patients, hospitals, clinics, insurance companies"
            ),
            business_model=(
                "Per-transaction fee for record access"
                " + subscription for healthcare providers."
            ),
            revenue_model=(
                "Provider subscriptions ($299/month),"
                " Per-transaction fees ($0.50),"
                " Insurance data access fees"
            ),
            competitor_analysis=(
                "Epic Systems (expensive, enterprise-focused),"
                " PatientBank (limited scope). Our solution is"
                " more accessible and interoperable."
            ),
            unique_selling_proposition=(
                "Blockchain-based interoperability with"
                " patient-controlled access and AI-powered"
                " health insights."
            ),
            required_investment=750000,
            team_members="John Doe, Dr. Sarah Medical, Mike Security",
            expected_timeline="24 months", status="submitted",
        )

        tips = [
            {
                "title": "Bootstrapping Your Startup",
                "content": (
                    "Start with your own savings or revenue from"
                    " early customers. Focus on building a minimum"
                    " viable product (MVP) and validating your idea"
                    " before seeking external funding."
                ),
                "source": "Y Combinator",
            },
            {
                "title": "Angel Investment Tips",
                "content": (
                    "Build relationships with angel investors through"
                    " networking events and platforms like AngelList."
                    " Have a clear pitch deck and demonstrate traction."
                ),
                "source": "Angel Capital Association",
            },
            {
                "title": "Venture Capital Guide",
                "content": (
                    "VCs look for scalable businesses with large"
                    " addressable markets. Prepare detailed financial"
                    " projections and show strong unit economics."
                ),
                "source": "Harvard Business Review",
            },
            {
                "title": "Government Grants",
                "content": (
                    "Explore SBIR/STTR grants for R&D funding."
                    " Many governments offer innovation grants"
                    " and tax incentives for startups."
                ),
                "source": "SBA.gov",
            },
            {
                "title": "Crowdfunding Strategies",
                "content": (
                    "Platforms like Kickstarter and Indiegogo are"
                    " great for consumer products. Build a compelling"
                    " story and offer attractive rewards."
                ),
                "source": "Forbes",
            },
        ]
        for tip in tips:
            FundingTip.objects.create(**tip)

        trends = [
            {
                "name": "Artificial Intelligence",
                "description": (
                    "AI and ML continue to transform industries with"
                    " automation, predictive analytics, and personalized"
                    " experiences."
                ),
                "growth_rate": 38.5,
                "market_size": 150000000000,
                "icon": "bi-cpu",
            },
            {
                "name": "Remote Work Technology",
                "description": (
                    "The shift to remote work drives demand for"
                    " collaboration tools, virtual offices, and"
                    " productivity software."
                ),
                "growth_rate": 25.3,
                "market_size": 80000000000,
                "icon": "bi-laptop",
            },
            {
                "name": "Clean Energy",
                "description": (
                    "Renewable energy, electric vehicles, and sustainable"
                    " technologies are experiencing rapid growth."
                ),
                "growth_rate": 22.8,
                "market_size": 120000000000,
                "icon": "bi-sun",
            },
            {
                "name": "Digital Health",
                "description": (
                    "Telemedicine, digital therapeutics, and health"
                    " monitoring apps are reshaping healthcare delivery."
                ),
                "growth_rate": 28.4,
                "market_size": 95000000000,
                "icon": "bi-heart-pulse",
            },
            {
                "name": "FinTech Innovation",
                "description": (
                    "Digital payments, blockchain, and decentralized"
                    " finance are transforming the financial sector."
                ),
                "growth_rate": 32.1,
                "market_size": 180000000000,
                "icon": "bi-currency-bitcoin",
            },
            {
                "name": "EdTech Revolution",
                "description": (
                    "Online learning platforms, AI tutoring, and skill"
                    " development tools are growing rapidly."
                ),
                "growth_rate": 20.5,
                "market_size": 60000000000,
                "icon": "bi-book",
            },
        ]
        for trend in trends:
            IndustryTrend.objects.create(**trend)

        testimonials = [
            {
                "name": "Sarah Johnson",
                "role": "Founder, TechFlow",
                "content": (
                    "Creative Spark helped me refine my startup idea"
                    " with their AI evaluation. The mentorship program"
                    " connected me with industry experts who guided me"
                    " through the entire process."
                ),
                "rating": 5,
            },
            {
                "name": "Mike Chen",
                "role": "CEO, GreenTech Solutions",
                "content": (
                    "The market analysis and competitive insights I got"
                    " from this platform were invaluable. I was able to"
                    " pivot my business model based on the data-driven"
                    " recommendations."
                ),
                "rating": 5,
            },
            {
                "name": "Emily Rodriguez",
                "role": "Founder, EduInnovate",
                "content": (
                    "As a first-time entrepreneur, the incubation"
                    " roadmap and funding tips were game-changers."
                    " I successfully raised my seed round using the"
                    " reports generated by the platform."
                ),
                "rating": 4,
            },
        ]
        for t in testimonials:
            Testimonial.objects.create(**t)

        quotes = [
            {
                "quote": "The best way to predict the future is to create it.",
                "author": "Peter Drucker",
            },
            {
                "quote": (
                    "Innovation distinguishes between"
                    " a leader and a follower."
                ),
                "author": "Steve Jobs",
            },
            {
                "quote": (
                    "The only way to do great work"
                    " is to love what you do."
                ),
                "author": "Steve Jobs",
            },
            {
                "quote": (
                    "Your most unhappy customers are"
                    " your greatest source of learning."
                ),
                "author": "Bill Gates",
            },
            {
                "quote": "The biggest risk is not taking any risk.",
                "author": "Mark Zuckerberg",
            },
        ]
        for q in quotes:
            StartupQuote.objects.create(**q)

        badges_data = [
            {
                "name": "First Idea",
                "slug": "first-idea",
                "description": "Submitted your first startup idea",
                "icon": "bi-lightbulb",
                "xp_required": 10,
                "badge_type": "idea",
            },
            {
                "name": "Idea Machine",
                "slug": "idea-machine",
                "description": "Submitted 5 startup ideas",
                "icon": "bi-stars",
                "xp_required": 50,
                "badge_type": "idea",
            },
            {
                "name": "Top Rated",
                "slug": "top-rated",
                "description": "Received an evaluation score of 4.0+",
                "icon": "bi-trophy",
                "xp_required": 75,
                "badge_type": "evaluation",
            },
            {
                "name": "Mentorship Seeker",
                "slug": "mentorship-seeker",
                "description": "Completed first mentorship session",
                "icon": "bi-people",
                "xp_required": 30,
                "badge_type": "mentor",
            },
            {
                "name": "Community Star",
                "slug": "community-star",
                "description": "Active contributor to discussions",
                "icon": "bi-chat-dots",
                "xp_required": 40,
                "badge_type": "community",
            },
            {
                "name": "Rising Star",
                "slug": "rising-star",
                "description": "Reached level 5",
                "icon": "bi-star",
                "xp_required": 100,
                "badge_type": "milestone",
            },
        ]
        for badge in badges_data:
            Badge.objects.create(**badge)

        for user in User.objects.all():
            UserXP.objects.get_or_create(
                user=user, defaults={"total_xp": 50, "level": 1}
            )

        investors_data = [
            {
                "name": "TechStars Ventures",
                "investor_type": "vc",
                "description": (
                    "Leading early-stage VC funding disruptive"
                    " technology startups."
                ),
                "min_investment": 500000,
                "max_investment": 5000000,
                "preferred_stages": "Seed, Series A",
                "preferred_industries": "Technology, AI, SaaS",
                "location": "San Francisco, CA",
                "website": "https://techstars.com",
            },
            {
                "name": "Angel Fund Alpha",
                "investor_type": "angel",
                "description": (
                    "Angel investor network focused on healthtech"
                    " and edtech."
                ),
                "min_investment": 100000,
                "max_investment": 1000000,
                "preferred_stages": "Pre-seed, Seed",
                "preferred_industries": "Healthcare, Education, Technology",
                "location": "New York, NY",
                "website": "https://alphafund.com",
            },
            {
                "name": "GreenFuture Capital",
                "investor_type": "corporate",
                "description": (
                    "Corporate VC investing in sustainable"
                    " and green technology."
                ),
                "min_investment": 200000,
                "max_investment": 3000000,
                "preferred_stages": "Seed, Series A",
                "preferred_industries": "Environment, CleanTech, Agriculture",
                "location": "Austin, TX",
                "website": "https://greenfuture.vc",
            },
            {
                "name": "SeedSpark Accelerator",
                "investor_type": "accelerator",
                "description": (
                    "3-month accelerator program with $150K seed funding."
                ),
                "min_investment": 150000,
                "max_investment": 150000,
                "preferred_stages": "Pre-seed",
                "preferred_industries": "Technology, FinTech, E-Commerce",
                "location": "Miami, FL",
                "website": "https://seedspark.com",
            },
            {
                "name": "GovTech Innovation Grant",
                "investor_type": "grant",
                "description": (
                    "Government grant for innovative technology solutions."
                ),
                "min_investment": 50000,
                "max_investment": 500000,
                "preferred_stages": "Seed",
                "preferred_industries": "Technology, Education, Healthcare",
                "location": "Washington, DC",
            },
        ]
        for inv in investors_data:
            Investor.objects.create(**inv)

        self.stdout.write(
            self.style.SUCCESS(
                "Sample data loaded successfully!\n"
                "  - Admin user: admin / admin123\n"
                "  - Student 1: student1 / student123\n"
                "  - Student 2: student2 / student123\n"
                "  - Mentor: mentor1 / mentor123"
            )
        )
