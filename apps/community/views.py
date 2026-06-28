from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserFollow, ChatRoom, ChatMessage, SuccessStory, StartupShowcase, Podcast, Webinar, WebinarRegistration, ForumQuestion, ForumAnswer
from apps.ideas.models import StartupIdea


def showcase(request):
    showcases = StartupShowcase.objects.filter(is_published=True)
    return render(request, "community/showcase.html", {"showcases": showcases})


def success_stories(request):
    stories = SuccessStory.objects.filter(is_approved=True)
    return render(request, "community/success_stories.html", {"stories": stories})


@login_required
def add_success_story(request):
    if request.method == "POST":
        SuccessStory.objects.create(
            user=request.user,
            idea_id=request.POST.get("idea") or None,
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            achievement=request.POST.get("achievement", ""),
        )
        messages.success(request, "Story submitted for approval!")
        return redirect("success_stories")
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "community/add_story.html", {"ideas": ideas})


@login_required
def follow_user(request, user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        messages.error(request, "Cannot follow yourself.")
        return redirect("public_profile", user_id=user_id)
    follow, created = UserFollow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
    return redirect("public_profile", user_id=user_id)


def public_profile(request, user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    profile_user = get_object_or_404(User, pk=user_id)
    ideas = StartupIdea.objects.filter(user=profile_user)
    followers_count = UserFollow.objects.filter(following=profile_user).count()
    following_count = UserFollow.objects.filter(follower=profile_user).count()
    is_following = False
    if request.user.is_authenticated:
        is_following = UserFollow.objects.filter(follower=request.user, following=profile_user).exists()
    return render(request, "community/public_profile.html", {
        "profile_user": profile_user,
        "ideas": ideas,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    })


@login_required
def chat_rooms(request):
    rooms = ChatRoom.objects.filter(participants=request.user)
    return render(request, "community/chat_rooms.html", {"rooms": rooms})


@login_required
def chat_room_detail(request, pk):
    room = get_object_or_404(ChatRoom, pk=pk, participants=request.user)
    if request.method == "POST":
        ChatMessage.objects.create(room=room, sender=request.user, content=request.POST.get("message"))
        return redirect("chat_room_detail", pk=room.pk)
    return render(request, "community/chat_room.html", {"room": room})


@login_required
def start_chat(request, user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    other_user = get_object_or_404(User, pk=user_id)
    existing = ChatRoom.objects.filter(participants=request.user).filter(participants=other_user, is_group=False)
    if existing.exists():
        return redirect("chat_room_detail", pk=existing.first().pk)
    room = ChatRoom.objects.create(is_group=False)
    room.participants.add(request.user, other_user)
    return redirect("chat_room_detail", pk=room.pk)


def podcast_list(request):
    podcasts = Podcast.objects.filter(is_published=True)
    return render(request, "community/podcast_list.html", {"podcasts": podcasts})


def webinar_list(request):
    webinars = Webinar.objects.filter(is_active=True)
    return render(request, "community/webinar_list.html", {"webinars": webinars})


@login_required
def webinar_register(request, webinar_id):
    webinar = get_object_or_404(Webinar, pk=webinar_id, is_active=True)
    reg, created = WebinarRegistration.objects.get_or_create(webinar=webinar, user=request.user)
    if created:
        messages.success(request, "Registered for webinar!")
    else:
        messages.info(request, "Already registered.")
    return redirect("webinar_list")


def forum_list(request):
    questions = ForumQuestion.objects.all()
    return render(request, "community/forum_list.html", {"questions": questions})


@login_required
def forum_ask(request):
    if request.method == "POST":
        ForumQuestion.objects.create(
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            user=request.user,
            tags=request.POST.get("tags", ""),
        )
        messages.success(request, "Question posted!")
        return redirect("forum_list")
    return render(request, "community/forum_ask.html")


def forum_detail(request, pk):
    question = get_object_or_404(ForumQuestion, pk=pk)
    question.views_count += 1
    question.save(update_fields=["views_count"])
    if request.method == "POST" and request.user.is_authenticated:
        ForumAnswer.objects.create(question=question, content=request.POST.get("content"), user=request.user)
        messages.success(request, "Answer posted!")
        return redirect("forum_detail", pk=question.pk)
    return render(request, "community/forum_detail.html", {"question": question})
