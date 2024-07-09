
from django.contrib import admin
from django.urls import path, include

from goodread.views import landing_page

urlpatterns = [
    path("", landing_page, name="landing"),
    path("users/", include("users.urls")),
    path("books/", include("books.urls")),


    path("admin/", admin.site.urls),
]
