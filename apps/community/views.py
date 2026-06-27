from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import (
    UserFollow,
    SuccessStory,
    StartupShowcase,
    ChatRoom,
    ChatMessage,
)
from apps.ideas.models import StartupIdea

UserModel = get_user_model()


def showcase(request):
    showcases = StartupShowcase.objects.filter(
        is_published=True
    ).select_related("idea")
    return render(request, "community/showcase.html", {"showcases": showcases})


def success_stories(request):
    stories = SuccessStory.objects.filter(is_approved=True)
    return render(
        request, "community/success_stories.html", {"stories": stories}
    )


@login_required
def add_success_story(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        achievement = request.POST.get("achievement")
        idea_id = request.POST.get("idea")

        story = SuccessStory(
            user=request.user,
            title=title,
            content=content,
            achievement=achievement,
        )
        if idea_id:
            story.idea_id = idea_id
        story.save()
        messages.success(
            request, "Your success story has been submitted for review!"
        )
        return redirect("success_stories")

    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "community/add_story.html", {"ideas": ideas})


@login_required
def follow_user(request, user_id):
    target = get_object_or_404(UserModel, pk=user_id)
    if target == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("public_profile", user_id=user_id)

    follow, created = UserFollow.objects.get_or_create(
        follower=request.user, following=target
    )
    if not created:
        follow.delete()
        messages.success(request, f"Unfollowed {target.username}")
    else:
        messages.success(request, f"Now following {target.username}")
    return redirect("public_profile", user_id=user_id)


def public_profile(request, user_id):
    profile_user = get_object_or_404(UserModel, pk=user_id)
    ideas = StartupIdea.objects.filter(user=profile_user, status="approved")
    followers_count = UserFollow.objects.filter(following=profile_user).count()
    following_count = UserFollow.objects.filter(follower=profile_user).count()
    is_following = False
    if request.user.is_authenticated:
        is_following = UserFollow.objects.filter(
            follower=request.user, following=profile_user
        ).exists()

    return render(
        request,
        "community/public_profile.html",
        {
            "profile_user": profile_user,
            "ideas": ideas,
            "followers_count": followers_count,
            "following_count": following_count,
            "is_following": is_following,
        },
    )


@login_required
def chat_rooms(request):
    rooms = ChatRoom.objects.filter(participants=request.user)
    return render(request, "community/chat_rooms.html", {"rooms": rooms})


@login_required
def chat_room_detail(request, pk):
    room = get_object_or_404(ChatRoom, pk=pk)
    if request.user not in room.participants.all():
        messages.error(request, "You are not a member of this chat room.")
        return redirect("chat_rooms")
    messages_list = ChatMessage.objects.filter(room=room)
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            ChatMessage.objects.create(
                room=room, sender=request.user, content=content
            )
            messages.success(request, "Message sent!")
        return redirect("chat_room_detail", pk=pk)
    return render(
        request,
        "community/chat_room.html",
        {
            "room": room,
            "messages": messages_list,
        },
    )


@login_required
def start_chat(request, user_id):
    target = get_object_or_404(UserModel, pk=user_id)
    if target == request.user:
        messages.error(request, "You cannot chat with yourself.")
        return redirect("public_profile", user_id=user_id)

    room = (
        ChatRoom.objects.filter(participants=request.user)
        .filter(participants=target)
        .first()
    )
    if not room:
        room = ChatRoom.objects.create(
            name=f"{request.user.username} & {target.username}"
        )
        room.participants.add(request.user, target)
    return redirect("chat_room_detail", pk=room.id)
