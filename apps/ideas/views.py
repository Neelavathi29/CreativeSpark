from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import StartupIdea, Category, IdeaLike, IdeaBookmark, IdeaComment
from .forms import StartupIdeaForm
from apps.evaluation.ai_evaluator import evaluate_idea


@login_required
def idea_list(request):
    query = request.GET.get("q", "")
    category_slug = request.GET.get("category", "")
    status_filter = request.GET.get("status", "")
    rating_filter = request.GET.get("rating", "")
    sort_by = request.GET.get("sort", "-created_at")

    ideas = StartupIdea.objects.all()

    if query:
        q = Q(startup_name__icontains=query)
        q = q | Q(problem_statement__icontains=query)
        q = q | Q(industry__icontains=query)
        q = q | Q(founder_name__icontains=query)
        ideas = ideas.filter(q)

    if category_slug:
        ideas = ideas.filter(category__slug=category_slug)

    if status_filter:
        ideas = ideas.filter(status=status_filter)

    if rating_filter:
        ideas = ideas.filter(
            evaluations__overall_rating__gte=float(rating_filter)
        )

    ideas = (
        ideas.select_related("user", "category")
        .prefetch_related("evaluations")
        .order_by(sort_by)
    )

    paginator = Paginator(ideas, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.annotate(idea_count=Count("ideas"))
    status_choices = StartupIdea.STATUS_CHOICES

    context = {
        "ideas": page_obj,
        "categories": categories,
        "status_choices": status_choices,
        "query": query,
        "current_category": category_slug,
        "current_status": status_filter,
        "current_rating": rating_filter,
        "page_obj": page_obj,
    }
    return render(request, "ideas/idea_list.html", context)


@login_required
def idea_detail(request, pk):
    idea = get_object_or_404(
        StartupIdea.objects.select_related("user", "category").prefetch_related(
            "evaluations", "comments__user"
        ),
        pk=pk,
    )
    session_key = f"viewed_idea_{pk}"
    if not request.session.get(session_key):
        idea.views_count += 1
        idea.save()
        request.session[session_key] = True
        request.session.set_expiry(86400)

    is_liked = IdeaLike.objects.filter(user=request.user, idea=idea).exists()
    is_bookmarked = IdeaBookmark.objects.filter(
        user=request.user, idea=idea
    ).exists()
    evaluation = idea.evaluations.first()
    comments = idea.comments.all()

    context = {
        "idea": idea,
        "is_liked": is_liked,
        "is_bookmarked": is_bookmarked,
        "evaluation": evaluation,
        "comments": comments,
    }
    return render(request, "ideas/idea_detail.html", context)


@login_required
def idea_create(request):
    if request.method == "POST":
        form = StartupIdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.save()

            evaluate_idea(idea)

            messages.success(
                request,
                "Your startup idea has been submitted!"
                " AI evaluation is complete.",
            )
            return redirect("idea_detail", pk=idea.pk)
    else:
        form = StartupIdeaForm()
    return render(
        request,
        "ideas/idea_form.html",
        {"form": form, "title": "Submit New Idea"},
    )


@login_required
def idea_edit(request, pk):
    idea = get_object_or_404(StartupIdea, pk=pk)
    if idea.user != request.user and not request.user.is_superuser:
        messages.error(request, "You can only edit your own ideas.")
        return redirect("idea_detail", pk=pk)

    if request.method == "POST":
        form = StartupIdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            messages.success(request, "Your idea has been updated!")
            return redirect("idea_detail", pk=pk)
    else:
        form = StartupIdeaForm(instance=idea)
    return render(
        request, "ideas/idea_form.html", {"form": form, "title": "Edit Idea"}
    )


@login_required
def my_ideas(request):
    ideas = StartupIdea.objects.filter(user=request.user)
    return render(request, "ideas/my_ideas.html", {"ideas": ideas})


@login_required
def like_idea(request, pk):
    idea = get_object_or_404(StartupIdea, pk=pk)
    like, created = IdeaLike.objects.get_or_create(
        user=request.user, idea=idea
    )
    if not created:
        like.delete()
        idea.likes_count = max(0, idea.likes_count - 1)
    else:
        idea.likes_count += 1
    idea.save()
    return redirect("idea_detail", pk=pk)


@login_required
def bookmark_idea(request, pk):
    idea = get_object_or_404(StartupIdea, pk=pk)
    bookmark, created = IdeaBookmark.objects.get_or_create(
        user=request.user, idea=idea
    )
    if not created:
        bookmark.delete()
        idea.bookmarks_count = max(0, idea.bookmarks_count - 1)
    else:
        idea.bookmarks_count += 1
    idea.save()
    return redirect("idea_detail", pk=pk)


@login_required
def add_comment(request, pk):
    idea = get_object_or_404(StartupIdea, pk=pk)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            IdeaComment.objects.create(
                user=request.user, idea=idea, content=content
            )
            messages.success(request, "Comment added!")
    return redirect("idea_detail", pk=pk)
