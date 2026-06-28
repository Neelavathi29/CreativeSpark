from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("apps.core.urls")),
    path("auth/", include("apps.authentication.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("ideas/", include("apps.ideas.urls")),
    path("evaluation/", include("apps.evaluation.urls")),
    path("market/", include("apps.market.urls")),
    path("mentors/", include("apps.mentors.urls")),
    path("reports/", include("apps.reports.urls")),
    path("community/", include("apps.community.urls")),
    path("gamification/", include("apps.gamification.urls")),
    path("productivity/", include("apps.productivity.urls")),
    path("funding/", include("apps.funding.urls")),
    path("collaboration/", include("apps.collaboration.urls")),
    path("canvas/", include("apps.canvas.urls")),
    path("analytics/", include("apps.analytics.urls")),
    path("api/", include("apps.api.urls")),
    path("accessibility/", include("apps.accessibility.urls")),
    path("blockchain/", include("apps.blockchain.urls")),
]

handler404 = "CreativeSpark.views.handler404"
handler500 = "CreativeSpark.views.handler500"
handler403 = "CreativeSpark.views.handler403"
handler400 = "CreativeSpark.views.handler400"

if settings.DEBUG:
    media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += media
    static_files = static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static_files
