from django.urls import path
from . import views

urlpatterns = [
    path("settings/", views.accessibility_settings, name="accessibility_settings"),
    path("save/", views.save_accessibility_prefs, name="save_accessibility_prefs"),
    path("shortcuts/", views.keyboard_shortcuts, name="keyboard_shortcuts"),
]
