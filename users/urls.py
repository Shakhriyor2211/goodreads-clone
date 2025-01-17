from django.urls import path

from users.views import RegisterView, LoginView, ProfileView, LogoutView, UpdateProfileView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name='login'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("update_profile/", UpdateProfileView.as_view(), name="update_profile")
]
