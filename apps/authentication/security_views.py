import secrets
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .security_models import LoginActivity, TwoFactorAuth
import pyotp


@login_required
def security_settings(request):
    activities = LoginActivity.objects.filter(user=request.user)[:20]
    two_factor, _ = TwoFactorAuth.objects.get_or_create(user=request.user)
    totp_uri = ""
    if two_factor.is_enabled and two_factor.secret_key:
        totp = pyotp.TOTP(two_factor.secret_key)
        totp_uri = totp.provisioning_uri(
            request.user.email,
            issuer_name="Creative Spark",
        )

    return render(
        request,
        "authentication/security.html",
        {
            "activities": activities,
            "two_factor": two_factor,
            "totp_uri": totp_uri,
        },
    )


@login_required
def toggle_two_factor(request):
    two_factor, _ = TwoFactorAuth.objects.get_or_create(user=request.user)
    if two_factor.is_enabled:
        two_factor.is_enabled = False
        messages.success(request, "Two-factor authentication disabled.")
    else:
        two_factor.is_enabled = True
        two_factor.secret_key = pyotp.random_base32()
        codes = "\n".join([secrets.token_hex(4) for _ in range(8)])
        two_factor.backup_codes = codes
        messages.success(
            request,
            "Two-factor authentication enabled. "
            "Scan the QR code or enter the secret in your authenticator app.",
        )
    two_factor.save()
    return redirect("security_settings")
