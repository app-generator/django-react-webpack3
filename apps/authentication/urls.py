from django.contrib.auth import views
from django.urls import path

from .views import login_view, register_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]