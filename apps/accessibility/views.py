from django.shortcuts import render
from django.http import JsonResponse


def accessibility_settings(request):
    return render(request, "accessibility/settings.html")


def save_accessibility_prefs(request):
    if request.method == "POST":
        prefs = {
            "high_contrast": request.POST.get("high_contrast") == "on",
            "font_size": request.POST.get("font_size", "normal"),
            "reduce_motion": request.POST.get("reduce_motion") == "on",
            "screen_reader": request.POST.get("screen_reader") == "on",
            "keyboard_nav": request.POST.get("keyboard_nav") == "on",
        }
        if hasattr(request, "session"):
            request.session["accessibility"] = prefs
        return JsonResponse({"status": "ok", "prefs": prefs})
    return JsonResponse({"error": "POST required"}, status=405)


def keyboard_shortcuts(request):
    return render(request, "accessibility/keyboard_shortcuts.html")
