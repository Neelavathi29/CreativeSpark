import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CanvasProject
from apps.ideas.models import StartupIdea


@login_required
def canvas_list(request):
    canvases = CanvasProject.objects.filter(idea__user=request.user)
    return render(request, "canvas/canvas_list.html", {"canvases": canvases})


@login_required
def canvas_detail(request, pk):
    canvas = get_object_or_404(CanvasProject, pk=pk, idea__user=request.user)
    if request.method == "POST":
        canvas.data = json.loads(request.POST.get("data", "{}"))
        canvas.save()
        messages.success(request, "Canvas saved!")
        return redirect("canvas_detail", pk=canvas.pk)
    return render(request, "canvas/canvas_detail.html", {"canvas": canvas})


@login_required
def canvas_create(request):
    if request.method == "POST":
        canvas_type = request.POST.get("canvas_type")
        idea_id = request.POST.get("idea")
        idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
        template_data = get_canvas_template(canvas_type)
        canvas = CanvasProject.objects.create(
            idea=idea, canvas_type=canvas_type, data=template_data, created_by=request.user
        )
        messages.success(request, "Canvas created!")
        return redirect("canvas_detail", pk=canvas.pk)
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "canvas/canvas_form.html", {
        "ideas": ideas,
        "canvas_types": CanvasProject.CANVAS_TYPES,
    })


def get_canvas_template(canvas_type):
    templates = {
        "business_model": {
            "key_partners": "",
            "key_activities": "",
            "key_resources": "",
            "value_propositions": "",
            "customer_relationships": "",
            "channels": "",
            "customer_segments": "",
            "cost_structure": "",
            "revenue_streams": "",
        },
        "lean": {
            "problem": "",
            "solution": "",
            "key_metrics": "",
            "unique_value_proposition": "",
            "unfair_advantage": "",
            "channels": "",
            "customer_segments": "",
            "cost_structure": "",
            "revenue_streams": "",
        },
        "swot": {
            "strengths": "",
            "weaknesses": "",
            "opportunities": "",
            "threats": "",
        },
        "value_proposition": {
            "customer_jobs": "",
            "customer_pains": "",
            "customer_gains": "",
            "products_services": "",
            "pain_relievers": "",
            "gain_creators": "",
        },
        "customer_persona": {
            "name": "",
            "demographics": "",
            "goals": "",
            "frustrations": "",
            "behaviors": "",
            "needs": "",
        },
        "user_journey": {
            "awareness": "",
            "consideration": "",
            "decision": "",
            "onboarding": "",
            "retention": "",
            "advocacy": "",
        },
        "risk_matrix": {
            "risks": [],
        },
        "okr": {
            "objective": "",
            "key_results": [],
        },
    }
    return templates.get(canvas_type, {})


@login_required
def canvas_delete(request, pk):
    canvas = get_object_or_404(CanvasProject, pk=pk, idea__user=request.user)
    canvas.delete()
    messages.success(request, "Canvas deleted!")
    return redirect("canvas_list")
