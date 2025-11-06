from django.urls import path
from .views import LoginView, login_page

urlpatterns = [
    path("login/", LoginView.as_view(), name="api-login"),
    path("ui/login/", login_page, name="login-ui"),  # ✅ UI route
]
