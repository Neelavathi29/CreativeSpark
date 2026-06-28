from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .demo_mode import create_demo_data, seed_market_data
from apps.ideas.models import StartupIdea
from apps.funding.models import Investor
from apps.mentors.models import MentorProfile
from apps.community.models import SuccessStory
from apps.community.models import Podcast, Webinar


@staff_member_required
def demo_mode(request):
    created = create_demo_data()
    if created:
        messages.success(request, "Demo mode activated! Sample data has been loaded. Login with demo_founder / Demo@12345")
    else:
        messages.info(request, "Demo data already exists. You can login with demo_founder / Demo@12345")
    return redirect("admin_dashboard")


def qr_portfolio(request, idea_id=None):
    import hashlib, base64
    ideas = []
    if idea_id:
        ideas = StartupIdea.objects.filter(pk=idea_id)[:1]
    if not ideas:
        ideas = StartupIdea.objects.filter(status="approved")[:5]
    portfolio_data = []
    for idea in ideas:
        data_str = f"{idea.id}:{idea.startup_name}:{idea.founder_name}"
        qr_data = base64.b64encode(hashlib.md5(data_str.encode()).hexdigest().encode()).decode()[:20]
        portfolio_data.append({"idea": idea, "qr_code_id": qr_data})
    return render(request, "core/qr_portfolio.html", {"portfolio": portfolio_data})


def demo_login_info(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    demo_users = User.objects.filter(username__startswith="demo_")
    return render(request, "core/demo_info.html", {"demo_users": demo_users})
