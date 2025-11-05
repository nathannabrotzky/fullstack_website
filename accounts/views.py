from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm

def profile_view(request):
    return render(request, "accounts/profile.html")

from django.contrib.auth.forms import AuthenticationForm

def login_signup_view(request):
    login_form = AuthenticationForm()
    signup_form = SignUpForm()

    if request.method == "POST":
        if "login_submit" in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("home")

        elif "signup_submit" in request.POST:
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect("home")

    return render(request, "accounts/login.html", {
        "form": login_form,
        "signup_form": signup_form
    })

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AccessCode

@login_required
def redeem_code(request):
    if request.method == "POST":
        code_input = request.POST.get("code")
        try:
            code = AccessCode.objects.get(code=code_input, is_active=True)
            request.user.redeemed_codes.add(code)
            messages.success(request, f"Access code '{code.code}' redeemed!")
        except AccessCode.DoesNotExist:
            messages.error(request, "Invalid or expired access code.")
    return redirect("account:dashboard")
