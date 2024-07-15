from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from goodreads import settings
from goodreads.views import NotFoundView, HomeView, LandingView

handler404 = NotFoundView.as_view()


urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("home/", HomeView.as_view(), name="home"),
    path("users/", include("users.urls")),
    path("books/", include("books.urls")),


    path("admin/", admin.site.urls),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)