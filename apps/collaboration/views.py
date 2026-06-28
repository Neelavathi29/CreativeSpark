import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import models as db_models
from .models import Whiteboard, SharedNote, NoteVersion, Poll, PollOption, TeamVote, TeamVoteOption, TeamVoteResponse, FileVersion, ActivityTimeline
from apps.ideas.models import StartupIdea


@login_required
def whiteboard_list(request):
    whiteboards = Whiteboard.objects.filter(
        db_models.Q(created_by=request.user) | db_models.Q(collaborators=request.user)
    ).distinct()
    return render(request, "collaboration/whiteboard_list.html", {"whiteboards": whiteboards})


@login_required
def whiteboard_detail(request, pk):
    whiteboard = get_object_or_404(Whiteboard, pk=pk)
    if request.user != whiteboard.created_by and request.user not in whiteboard.collaborators.all():
        messages.error(request, "Access denied.")
        return redirect("whiteboard_list")
    if request.method == "POST":
        whiteboard.content = json.loads(request.POST.get("content", "{}"))
        whiteboard.save()
        ActivityTimeline.objects.create(user=request.user, action_type="updated", description=f"Updated whiteboard: {whiteboard.title}", idea=whiteboard.idea)
        return JsonResponse({"status": "ok"})
    return render(request, "collaboration/whiteboard_detail.html", {"whiteboard": whiteboard})


@login_required
def whiteboard_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        idea_id = request.POST.get("idea")
        idea = get_object_or_404(StartupIdea, pk=idea_id) if idea_id else None
        wb = Whiteboard.objects.create(title=title, created_by=request.user, idea=idea)
        ActivityTimeline.objects.create(user=request.user, action_type="created", description=f"Created whiteboard: {wb.title}", idea=idea)
        messages.success(request, "Whiteboard created!")
        return redirect("whiteboard_detail", pk=wb.pk)
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "collaboration/whiteboard_form.html", {"ideas": ideas})


@login_required
def shared_notes_list(request):
    notes = SharedNote.objects.filter(
        db_models.Q(created_by=request.user) | db_models.Q(collaborators=request.user) | db_models.Q(is_public=True)
    ).distinct()
    return render(request, "collaboration/shared_notes_list.html", {"notes": notes})


@login_required
def shared_note_detail(request, pk):
    note = get_object_or_404(SharedNote, pk=pk)
    if not note.is_public and request.user != note.created_by and request.user not in note.collaborators.all():
        messages.error(request, "Access denied.")
        return redirect("shared_notes_list")
    if request.method == "POST":
        content = request.POST.get("content")
        old_content = note.content
        note.content = content
        note.save()
        latest = note.versions.first()
        vnum = (latest.version_number + 1) if latest else 1
        NoteVersion.objects.create(note=note, content=old_content, version_number=vnum, edited_by=request.user)
        ActivityTimeline.objects.create(user=request.user, action_type="updated", description=f"Updated note: {note.title}")
        messages.success(request, "Note updated!")
        return redirect("shared_note_detail", pk=note.pk)
    return render(request, "collaboration/shared_note_detail.html", {"note": note})


@login_required
def shared_note_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        idea_id = request.POST.get("idea")
        idea = get_object_or_404(StartupIdea, pk=idea_id) if idea_id else None
        note = SharedNote.objects.create(title=title, content=content, created_by=request.user, idea=idea)
        NoteVersion.objects.create(note=note, content=content, version_number=1, edited_by=request.user)
        ActivityTimeline.objects.create(user=request.user, action_type="created", description=f"Created note: {note.title}", idea=idea)
        messages.success(request, "Note created!")
        return redirect("shared_note_detail", pk=note.pk)
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "collaboration/shared_note_form.html", {"ideas": ideas})


@login_required
def poll_list(request):
    polls = Poll.objects.filter(
        db_models.Q(created_by=request.user) | db_models.Q(idea__user=request.user)
    ).distinct()
    return render(request, "collaboration/poll_list.html", {"polls": polls})


@login_required
def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == "POST":
        selected = request.POST.getlist("option")
        for opt_id in selected:
            opt = get_object_or_404(PollOption, pk=opt_id)
            opt.votes.add(request.user)
        messages.success(request, "Vote recorded!")
        return redirect("poll_detail", pk=poll.pk)
    return render(request, "collaboration/poll_detail.html", {"poll": poll})


@login_required
def poll_create(request):
    if request.method == "POST":
        question = request.POST.get("question")
        options = request.POST.getlist("options")
        idea_id = request.POST.get("idea")
        idea = get_object_or_404(StartupIdea, pk=idea_id) if idea_id else None
        poll = Poll.objects.create(question=question, created_by=request.user, idea=idea)
        for opt_text in options:
            if opt_text.strip():
                PollOption.objects.create(poll=poll, text=opt_text.strip())
        ActivityTimeline.objects.create(user=request.user, action_type="created", description=f"Created poll: {poll.question}", idea=idea)
        messages.success(request, "Poll created!")
        return redirect("poll_list")
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "collaboration/poll_form.html", {"ideas": ideas})


@login_required
def team_vote_list(request):
    votes = TeamVote.objects.filter(
        db_models.Q(created_by=request.user) | db_models.Q(idea__user=request.user)
    ).distinct()
    return render(request, "collaboration/team_vote_list.html", {"votes": votes})


@login_required
def team_vote_detail(request, pk):
    vote = get_object_or_404(TeamVote, pk=pk)
    if request.method == "POST":
        option_id = request.POST.get("option")
        option = get_object_or_404(TeamVoteOption, pk=option_id)
        TeamVoteResponse.objects.get_or_create(vote=vote, option=option, voter=request.user)
        messages.success(request, "Vote recorded!")
        return redirect("team_vote_detail", pk=vote.pk)
    return render(request, "collaboration/team_vote_detail.html", {"vote": vote})


@login_required
def timeline(request):
    activities = ActivityTimeline.objects.filter(user=request.user)[:50]
    return render(request, "collaboration/timeline.html", {"activities": activities})
