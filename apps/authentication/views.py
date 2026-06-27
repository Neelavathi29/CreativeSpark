from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (
    login,
    logout,
    authenticate,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistrationForm, UserProfileForm
from .models import User
from .security_models import LoginActivity
from apps.core.models import AccountActivityLog


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Welcome {user.username}! Your account has been created.",
            )
            return redirect("dashboard:home")
    else:
        form = UserRegistrationForm()
    return render(request, "authentication/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            from .security_models import TwoFactorAuth
            try:
                tfa = TwoFactorAuth.objects.get(user=user, is_enabled=True)
                request.session["2fa_user_id"] = user.id
                request.session["2fa_next"] = request.GET.get(
                    "next", "dashboard:home"
                )
                return redirect("verify_2fa")
            except TwoFactorAuth.DoesNotExist:
                pass
            login(request, user)
            LoginActivity.objects.create(
                user=user,
                ip_address=request.META.get("REMOTE_ADDR", "0.0.0.0"),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
                is_successful=True,
            )
            AccountActivityLog.objects.create(
                user=user,
                action="Login",
                details="User logged in successfully",
                ip_address=request.META.get("REMOTE_ADDR", "0.0.0.0"),
            )
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get("next", "dashboard:home")
            return redirect(next_url)
        else:
            if User.objects.filter(username=username).exists():
                failed_user = User.objects.get(username=username)
                LoginActivity.objects.create(
                    user=failed_user,
                    ip_address=request.META.get("REMOTE_ADDR", "0.0.0.0"),
                    is_successful=False,
                )
            messages.error(request, "Invalid username or password.")
    return render(request, "authentication/login.html")


def verify_2fa(request):
    user_id = request.session.get("2fa_user_id")
    if not user_id:
        return redirect("login")

    if request.method == "POST":
        from .security_models import TwoFactorAuth
        import pyotp

        code = request.POST.get("code", "")
        tfa = get_object_or_404(TwoFactorAuth, user_id=user_id)
        totp = pyotp.TOTP(tfa.secret_key)
        if totp.verify(code) or code in (tfa.backup_codes or "").split("\n"):
            user = tfa.user
            login(request, user)
            LoginActivity.objects.create(
                user=user,
                ip_address=request.META.get("REMOTE_ADDR", "0.0.0.0"),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
                is_successful=True,
            )
            AccountActivityLog.objects.create(
                user=user,
                action="Login",
                details="User logged in successfully (2FA)",
                ip_address=request.META.get("REMOTE_ADDR", "0.0.0.0"),
            )
            # Remove used backup code
            if code in (tfa.backup_codes or "").split("\n"):
                codes = tfa.backup_codes.split("\n")
                codes.remove(code)
                tfa.backup_codes = "\n".join(codes)
                tfa.save()

            del request.session["2fa_user_id"]
            del request.session["2fa_next"]
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.session.pop("2fa_next", "dashboard:home")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid verification code. Try again.")

    return render(request, "authentication/verify_2fa.html")


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


@login_required
def profile(request):
    ideas = request.user.ideas.all()[:5]
    return render(request, "authentication/profile.html", {"ideas": ideas})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "authentication/edit_profile.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request, "authentication/change_password.html", {"form": form}
    )
