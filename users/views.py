from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from django.views import View

from users.forms import UserCreateForm, UserUpdateForm


class RegisterView(View):

    def get(self, request):
        create_form = UserCreateForm()
        context = {
            "form": create_form
        }

        return render(request, 'users/register.html', context)

    def post(self, request):
        create_user = UserCreateForm(data=request.POST)

        if create_user.is_valid():
            create_user.save()
            return redirect("users:login")

        else:
            context = {
                "form": create_user
            }
            return render(request, "users/register.html", context)


class LoginView(View):

    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, "users/login.html", {"login_form": login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You logged in successfully!")
            return redirect("books:books_list")

        else:
            return render(request, "users/login.html", {"login_form": login_form})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "users/profile.html", {"user": request.user})



class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.info(request, "You logged out!")
        return redirect("landing")



class UpdateProfileView(View):

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        return render(request, "users/update_profile.html", {"form": user_form})

    def post(self, request):
        user_form = UserUpdateForm(instance=request.user, data=request.POST, files=request.FILES)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile updated successfully")
            return redirect("users:profile")

        else:
            return render(request, "users/update_profile.html", {"form": user_form})







