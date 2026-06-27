from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import (
    Task,
    Milestone,
    CalendarEvent,
    Workspace,
    WorkspaceMember,
    WorkspaceDocument,
)
from apps.ideas.models import StartupIdea


@login_required
def task_board(request, idea_id=None):
    if idea_id:
        tasks = Task.objects.filter(user=request.user, idea_id=idea_id)
        idea = get_object_or_404(StartupIdea, pk=idea_id)
    else:
        tasks = Task.objects.filter(user=request.user)
        idea = None

    todo = tasks.filter(status="todo")
    in_progress = tasks.filter(status="in_progress")
    review = tasks.filter(status="review")
    done = tasks.filter(status="done")

    context = {
        "todo": todo,
        "in_progress": in_progress,
        "review": review,
        "done": done,
        "idea": idea,
        "tasks": tasks,
        "ideas": StartupIdea.objects.filter(user=request.user),
    }
    return render(request, "productivity/task_board.html", context)


@login_required
def add_task(request):
    if request.method == "POST":
        Task.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description", ""),
            priority=request.POST.get("priority", "medium"),
            idea_id=request.POST.get("idea") or None,
            due_date=request.POST.get("due_date") or None,
        )
        messages.success(request, "Task created!")
        return redirect("task_board")


@login_required
def update_task_status(request, task_id, status):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if status in dict(Task.STATUS_CHOICES):
        task.status = status
        task.save()
    return redirect("task_board")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.delete()
    return redirect("task_board")


@login_required
def milestones(request, idea_id):
    idea = get_object_or_404(StartupIdea, pk=idea_id)
    milestones_list = Milestone.objects.filter(idea=idea)

    if request.method == "POST":
        Milestone.objects.create(
            idea=idea,
            title=request.POST.get("title"),
            description=request.POST.get("description", ""),
            target_date=request.POST.get("target_date"),
        )
        messages.success(request, "Milestone added!")
        return redirect("milestones", idea_id=idea_id)

    return render(
        request,
        "productivity/milestones.html",
        {
            "idea": idea,
            "milestones": milestones_list,
        },
    )


@login_required
def update_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    new_status = request.POST.get("status")
    if new_status in dict(Milestone.STATUS_CHOICES):
        milestone.status = new_status
        if new_status == "completed" and not milestone.completed_date:
            from datetime import date

            milestone.completed_date = date.today()
        milestone.save()
    return redirect("milestones", idea_id=milestone.idea_id)


@login_required
def calendar_view(request):
    events = CalendarEvent.objects.filter(user=request.user)
    ideas = StartupIdea.objects.filter(user=request.user)

    if request.method == "POST":
        CalendarEvent.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description", ""),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date") or None,
            event_type=request.POST.get("event_type", "other"),
            related_idea_id=request.POST.get("idea") or None,
        )
        messages.success(request, "Event added!")
        return redirect("calendar_view")

    return render(
        request,
        "productivity/calendar.html",
        {
            "events": events,
            "ideas": ideas,
        },
    )


@login_required
def workspace_list(request):
    workspaces = Workspace.objects.filter(
        Q(created_by=request.user) | Q(members__user=request.user)
    ).distinct()
    return render(
        request, "productivity/workspace_list.html", {"workspaces": workspaces}
    )


@login_required
def workspace_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        idea_id = request.POST.get("idea")
        workspace = Workspace.objects.create(
            name=name,
            description=description,
            created_by=request.user,
            idea_id=idea_id or None,
        )
        WorkspaceMember.objects.create(
            workspace=workspace, user=request.user, role="admin"
        )
        member_ids = request.POST.getlist("members")
        for uid in member_ids:
            if uid and int(uid) != request.user.id:
                WorkspaceMember.objects.create(
                    workspace=workspace, user_id=int(uid), role="editor"
                )
        messages.success(request, "Workspace created!")
        return redirect("workspace_detail", pk=workspace.id)

    ideas = StartupIdea.objects.filter(user=request.user)
    return render(
        request,
        "productivity/workspace_form.html",
        {
            "ideas": ideas,
        },
    )


@login_required
def workspace_detail(request, pk):
    workspace = get_object_or_404(Workspace, pk=pk)
    is_member = workspace.members.filter(user=request.user).exists()
    if workspace.created_by != request.user and not is_member:
        messages.error(request, "You do not have access to this workspace.")
        return redirect("workspace_list")

    documents = WorkspaceDocument.objects.filter(workspace=workspace)
    tasks = Task.objects.filter(idea=workspace.idea) if workspace.idea else []

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_document":
            WorkspaceDocument.objects.create(
                workspace=workspace,
                title=request.POST.get("title"),
                content=request.POST.get("content", ""),
                uploaded_by=request.user,
            )
            messages.success(request, "Document added!")
        elif action == "remove_member":
            member_id = request.POST.get("member_id")
            WorkspaceMember.objects.filter(
                id=member_id, workspace=workspace
            ).delete()
            messages.success(request, "Member removed!")

    return render(
        request,
        "productivity/workspace_detail.html",
        {
            "workspace": workspace,
            "documents": documents,
            "tasks": tasks,
            "members": workspace.members.select_related("user").all(),
        },
    )
