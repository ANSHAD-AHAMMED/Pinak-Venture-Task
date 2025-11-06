# ibps_api/urls.py

from django.contrib import admin
from django.urls import path, include
from accounts.views import login_page   # ✅ import UI login view

urlpatterns = [
    path('', login_page, name="home"),  # ✅ Show UI on home page
    path('admin/', admin.site.urls),
    path("api/", include("accounts.urls")),
]
