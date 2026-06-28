from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .security_models import LoginActivity, TwoFactorAuth, Device, SuspiciousLogin
import pyotp
import secrets


@login_required
def security_settings(request):
    tfa, _ = TwoFactorAuth.objects.get_or_create(user=request.user)
    devices = Device.objects.filter(user=request.user)
    login_history = LoginActivity.objects.filter(user=request.user)[:20]
    suspicious = SuspiciousLogin.objects.filter(user=request.user)[:10]
    return render(request, "authentication/security.html", {
        "tfa": tfa,
        "devices": devices,
        "login_history": login_history,
        "suspicious_logins": suspicious,
    })


@login_required
def toggle_two_factor(request):
    tfa, _ = TwoFactorAuth.objects.get_or_create(user=request.user)
    if not tfa.is_enabled:
        tfa.secret_key = pyotp.random_base32()
        codes = [secrets.token_hex(4) for _ in range(5)]
        tfa.backup_codes = ",".join(codes)
        tfa.is_enabled = True
        tfa.save()
        totp = pyotp.TOTP(tfa.secret_key)
        provisioning_uri = totp.provisioning_uri(request.user.email, issuer_name="Creative Spark")
        messages.success(request, "Two-factor authentication enabled! Scan the QR code with your authenticator app.")
        return render(request, "authentication/verify_2fa.html", {
            "secret": tfa.secret_key,
            "provisioning_uri": provisioning_uri,
            "backup_codes": codes,
        })
    else:
        tfa.is_enabled = False
        tfa.secret_key = ""
        tfa.backup_codes = ""
        tfa.save()
        messages.success(request, "Two-factor authentication disabled.")
    return redirect("security_settings")


@login_required
def device_list(request):
    devices = Device.objects.filter(user=request.user)
    return render(request, "authentication/device_list.html", {"devices": devices})


@login_required
def remove_device(request, pk):
    device = get_object_or_404(Device, pk=pk, user=request.user)
    device.delete()
    messages.success(request, "Device removed.")
    return redirect("security_settings")


@login_required
def login_history(request):
    history = LoginActivity.objects.filter(user=request.user)[:50]
    return render(request, "authentication/login_history.html", {"history": history})
