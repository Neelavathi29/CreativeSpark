from django.urls import path
from . import views

urlpatterns = [
    path("", views.canvas_list, name="canvas_list"),
    path("create/", views.canvas_create, name="canvas_create"),
    path("<int:pk>/", views.canvas_detail, name="canvas_detail"),
    path("<int:pk>/delete/", views.canvas_delete, name="canvas_delete"),
]
