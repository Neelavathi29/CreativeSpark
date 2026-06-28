from django.urls import path
from . import views
from . import demo_views
from . import showcase_views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("activity-log/", views.activity_log, name="activity_log"),
    path("set-language/", views.set_language, name="set_language"),
    path("notifications/<int:pk>/read/", views.mark_notification_read, name="mark_notification_read"),
    path("notifications/read-all/", views.mark_all_notifications_read, name="mark_all_notifications_read"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/system-health/", views.system_health, name="system_health"),
    path("admin/email-templates/", views.email_templates, name="email_templates"),
    path("admin/site-config/", views.site_config, name="site_config"),
    path("admin/audit-logs/", views.audit_logs, name="audit_logs"),
    path("admin/backups/", views.backup_list, name="backup_list"),
    path("demo/load/", demo_views.demo_mode, name="demo_mode"),
    path("demo/info/", demo_views.demo_login_info, name="demo_info"),
    path("qr-portfolio/", demo_views.qr_portfolio, name="qr_portfolio"),
    path("qr-portfolio/<int:idea_id>/", demo_views.qr_portfolio, name="qr_portfolio_idea"),
    path("world-map/", showcase_views.world_startup_map, name="world_startup_map"),
    path("funding-tracker/", showcase_views.live_funding_tracker, name="live_funding_tracker"),
]
