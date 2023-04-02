from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from apps.authentication.forms import LoginForm, SignUpForm


def login_view(request):
    msg = None
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                try:
                    user_temp = User.objects.get(username=username)
                except ObjectDoesNotExist:
                    user_temp = None

                if user_temp is None:
                    msg = "This account doesn't exist."
                elif not user_temp.is_active:
                    msg = "Inactive account - Please confirm your email or contact support"
                else:
                    msg = "Invalid credentials"
    else:
        form = LoginForm()
    return render(request, "authentication/login.html", {"form": form, "msg": msg})


def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
    else:
        form = SignUpForm()
    return render(request, "authentication/register.html", {"form": form})
