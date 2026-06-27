from django.urls import path
from . import views

urlpatterns = [
    path("", views.report_dashboard, name="report_dashboard"),
    path("export/pdf/", views.export_pdf, name="export_pdf_all"),
    path("export/pdf/<int:pk>/", views.export_pdf, name="export_pdf"),
    path("export/excel/", views.export_excel, name="export_excel_all"),
    path("export/excel/<int:pk>/", views.export_excel, name="export_excel"),
    path("export/csv/", views.export_csv, name="export_csv_all"),
    path("export/csv/<int:pk>/", views.export_csv, name="export_csv"),
]
