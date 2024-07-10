
from django.contrib import admin
from django.urls import path, include

from goodread.views import LandingView, NotFoundView

handler404 = NotFoundView.as_view()


urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("users/", include("users.urls")),
    path("books/", include("books.urls")),


    path("admin/", admin.site.urls),
]
