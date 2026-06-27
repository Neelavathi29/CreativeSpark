from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
    MentorProfile,
    MentorshipSession,
    Discussion,
    DiscussionReply,
)
from .forms import MentorshipSessionForm, DiscussionForm


def mentor_list(request):
    mentors = MentorProfile.objects.filter(available=True).select_related("user")
    return render(request, "mentors/mentor_list.html", {"mentors": mentors})


def mentor_detail(request, pk):
    mentor = get_object_or_404(MentorProfile, pk=pk)
    discussions = Discussion.objects.filter(mentor=mentor)[:10]
    return render(
        request,
        "mentors/mentor_detail.html",
        {
            "mentor": mentor,
            "discussions": discussions,
        },
    )


@login_required
def book_session(request, pk):
    mentor = get_object_or_404(MentorProfile, pk=pk)
    if request.method == "POST":
        form = MentorshipSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.mentor = mentor
            session.student = request.user
            session.save()
            messages.success(
                request, "Mentorship session booked successfully!"
            )
            return redirect("mentor_detail", pk=pk)
    else:
        form = MentorshipSessionForm()
    return render(
        request,
        "mentors/book_session.html",
        {
            "form": form,
            "mentor": mentor,
        },
    )


@login_required
def my_sessions(request):
    if request.user.role == "mentor":
        sessions = MentorshipSession.objects.filter(
            mentor__user=request.user
        ).select_related("student", "mentor__user")
    else:
        sessions = MentorshipSession.objects.filter(
            student=request.user
        ).select_related("mentor__user", "student")
    return render(request, "mentors/my_sessions.html", {"sessions": sessions})


@login_required
def create_discussion(request, pk):
    mentor = get_object_or_404(MentorProfile, pk=pk)
    if request.method == "POST":
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.mentor = mentor
            discussion.user = request.user
            discussion.save()
            messages.success(request, "Discussion created!")
            return redirect("mentor_detail", pk=pk)
    else:
        form = DiscussionForm()
    return render(
        request,
        "mentors/create_discussion.html",
        {
            "form": form,
            "mentor": mentor,
        },
    )


@login_required
def discussion_detail(request, pk):
    discussion = get_object_or_404(
        Discussion.objects.select_related("user", "mentor__user"), pk=pk
    )
    replies = DiscussionReply.objects.filter(
        discussion=discussion
    ).select_related("user")

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            DiscussionReply.objects.create(
                discussion=discussion,
                user=request.user,
                content=content,
            )
            messages.success(request, "Reply added!")
        return redirect("discussion_detail", pk=pk)

    return render(
        request,
        "mentors/discussion_detail.html",
        {
            "discussion": discussion,
            "replies": replies,
        },
    )


@login_required
def submit_feedback(request, pk):
    session = get_object_or_404(
        MentorshipSession, pk=pk, student=request.user
    )
    if request.method == "POST":
        feedback = request.POST.get("feedback", "").strip()
        rating = request.POST.get("rating", 0)
        if feedback:
            session.feedback = feedback
            session.rating = int(rating) if rating.isdigit() else 0
            session.save()

            from apps.core.models import Notification
            Notification.objects.create(
                user=session.mentor.user,
                title="New Session Feedback",
                message=(
                    f"{request.user.username} left feedback"
                    f" for your session on '{session.topic}'"
                ),
                notification_type="info",
                link="/mentors/my-sessions/",
            )

            messages.success(request, "Feedback submitted! Thank you.")
            return redirect("my_sessions")
    return render(
        request,
        "mentors/submit_feedback.html",
        {"session": session},
    )
