from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from apps.authentication.forms import LoginForm, SignUpForm


def login_view(request):
    msg = None
    form = LoginForm(request.POST or None)

    if request.method == "POST":
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
            msg = "Error validating the form"

    else:
        form = LoginForm()
    return render(request, "authentication/login.html", {"form": form, "msg": msg})


def register_view(request):
    msg = None
    form = SignUpForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()

            msg = 'User created - please <a href="/login">login</a>.'
        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()
    return render(request, "authentication/register.html", {"form": form, "msg": msg})


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))
