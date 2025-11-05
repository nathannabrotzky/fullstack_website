from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", views.login_signup_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("redeem/", views.redeem_code, name="redeem_code"),
    path("profile/", views.profile_view, name="profile"),
]
