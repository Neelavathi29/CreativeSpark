from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import IdeaTimestamp, BlockchainCertificate
from apps.ideas.models import StartupIdea


@login_required
def timestamp_idea(request, idea_id):
    idea = get_object_or_404(StartupIdea, pk=idea_id, user=request.user)
    if hasattr(idea, "blockchain_timestamp"):
        messages.warning(request, "Idea already timestamped on blockchain.")
        return redirect("blockchain_certificate", pk=idea.blockchain_timestamp.pk)
    ts = IdeaTimestamp.objects.create(idea=idea)
    BlockchainCertificate.objects.create(
        idea_timestamp=ts,
        owner_name=request.user.get_full_name() or request.user.username,
        idea_name=idea.startup_name,
    )
    ActivityTimeline.objects.create(user=request.user, action_type="created", description=f"Timestamped idea on blockchain: {idea.startup_name}", idea=idea)
    messages.success(request, "Your idea has been timestamped on the blockchain!")
    return redirect("blockchain_certificate", pk=ts.pk)


@login_required
def blockchain_certificate(request, pk):
    ts = get_object_or_404(IdeaTimestamp, pk=pk, idea__user=request.user)
    cert = ts.certificate
    return render(request, "blockchain/certificate.html", {"timestamp": ts, "certificate": cert})


@login_required
def blockchain_dashboard(request):
    timestamps = IdeaTimestamp.objects.filter(idea__user=request.user).order_by("-block_number")
    return render(request, "blockchain/dashboard.html", {"timestamps": timestamps})


@login_required
def verify_certificate(request):
    cert_id = request.GET.get("certificate_id", "")
    cert = None
    if cert_id:
        try:
            cert = BlockchainCertificate.objects.get(certificate_id=cert_id, is_valid=True)
        except BlockchainCertificate.DoesNotExist:
            messages.error(request, "Certificate not found or has been revoked.")
    return render(request, "blockchain/verify.html", {"certificate": cert, "search_id": cert_id})


from apps.collaboration.models import ActivityTimeline
