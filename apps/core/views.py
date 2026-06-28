from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from .models import ContactMessage, VisitorCounter, AccountActivityLog, Testimonial, StartupQuote, Notification, EmailTemplate, SiteConfiguration, AuditLog, SystemHealth, BackupRecord
from apps.ideas.models import StartupIdea
from apps.funding.models import FundingApplication
from apps.evaluation.models import Evaluation
from datetime import date


def home(request):
    visitor_date = date.today()
    counter, _ = VisitorCounter.objects.get_or_create(date=visitor_date)
    counter.count += 1
    counter.save()
    ideas = StartupIdea.objects.filter(status="approved")[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:5]
    return render(request, "core/home.html", {"ideas": ideas, "testimonials": testimonials})


def about(request):
    return render(request, "core/about.html")


def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )
        messages.success(request, "Message sent! We'll get back to you soon.")
        return redirect("contact")
    return render(request, "core/contact.html")


def faq(request):
    return render(request, "core/faq.html")


@login_required
def activity_log(request):
    logs = AccountActivityLog.objects.filter(user=request.user)[:50]
    return render(request, "core/activity_log.html", {"logs": logs})


def set_language(request):
    if request.method == "POST":
        from django.conf import settings
        lang = request.POST.get("language")
        if lang and lang in dict(settings.LANGUAGES):
            from django.utils.translation import activate
            activate(lang)
            request.session["django_language"] = lang
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect("dashboard:home")


@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect(request.META.get("HTTP_REFERER", "dashboard:home"))


@staff_member_required
def admin_dashboard(request):
    total_ideas = StartupIdea.objects.count()
    total_users = get_user_model().objects.count()
    total_evaluations = Evaluation.objects.count()
    total_applications = FundingApplication.objects.count()
    recent_ideas = StartupIdea.objects.order_by("-created_at")[:10]
    recent_logs = AuditLog.objects.order_by("-created_at")[:20]
    health_checks = SystemHealth.objects.all()
    context = {
        "total_ideas": total_ideas,
        "total_users": total_users,
        "total_evaluations": total_evaluations,
        "total_applications": total_applications,
        "recent_ideas": recent_ideas,
        "recent_logs": recent_logs,
        "health_checks": health_checks,
    }
    return render(request, "core/admin_dashboard.html", context)


@staff_member_required
def system_health(request):
    checks = SystemHealth.objects.all()
    return render(request, "core/system_health.html", {"checks": checks})


@staff_member_required
def email_templates(request):
    templates = EmailTemplate.objects.all()
    return render(request, "core/email_templates.html", {"templates": templates})


@staff_member_required
def site_config(request):
    config, _ = SiteConfiguration.objects.get_or_create(pk=1)
    if request.method == "POST":
        config.site_name = request.POST.get("site_name", config.site_name)
        config.tagline = request.POST.get("tagline", "")
        config.contact_email = request.POST.get("contact_email", "")
        config.enable_registration = request.POST.get("enable_registration") == "on"
        config.enable_ai_features = request.POST.get("enable_ai_features") == "on"
        config.maintenance_mode = request.POST.get("maintenance_mode") == "on"
        config.save()
        AuditLog.objects.create(user=request.user, action="Updated site configuration")
        messages.success(request, "Site configuration updated!")
        return redirect("site_config")
    return render(request, "core/site_config.html", {"config": config})


@staff_member_required
def audit_logs(request):
    logs = AuditLog.objects.order_by("-created_at")[:100]
    return render(request, "core/audit_logs.html", {"logs": logs})


@staff_member_required
def backup_list(request):
    backups = BackupRecord.objects.order_by("-created_at")
    return render(request, "core/backup_list.html", {"backups": backups})


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
