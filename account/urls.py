from django.urls import path
from account.views import login_view, signup_view, logout_view

app_name = "account"


urlpatterns = [
    path("signup", signup_view, name="signup"),
    path("logout", logout_view, name="logout"),
    path("login", login_view, name="login"),
]