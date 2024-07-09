from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):

    def test_user_is_created(self):

        self.client.post(reverse("users:register"), data={
            "username": "shakhriyor",
            "email": "shakhriyormamadaliev@gmail.com",
            "first_name": "Shakhriyor",
            "last_name": "Mamadaliev",
            "password": "somepassword",
        })
        user = User.objects.get(username="shakhriyor")
        self.assertEqual(user.first_name, "Shakhriyor")
        self.assertEqual(user.last_name, "Mamadaliev")
        self.assertEqual(user.email, "shakhriyormamadaliev@gmail.com")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):

        res = self.client.post(reverse("users:register"), data={
            # "username": "shakhriyor",
            "email": "shakhriyormamadaliev@gmail.com",
            "first_name": "Shakhriyor",
            "last_name": "Mamadaliev",
            # "password": "somepassword",
        })

        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(res.context["form"], "username", "This field is required.")
        self.assertFormError(res.context["form"], "password", "This field is required.")

    def test_invalid_email(self):
        res = self.client.post(reverse("users:register"), data={
            "username": "shakhriyor",
            "email": "shakhriyormamadaliev",
            "first_name": "Shakhriyor",
            "last_name": "Mamadaliev",
            "password": "somepassword",
        })

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(res.context["form"], "email", "Enter a valid email address.")
    def test_unique_username(self):


        user = User.objects.create(username="shakhriyor", first_name="Shakhriyor")
        user.set_password("somepassword")
        user.save()

        res = self.client.post(reverse("users:register"), data={
            "username": "shakhriyor",
            "email": "shakhriyormamadaliev@gmail.com",
            "first_name": "Shakhriyor",
            "last_name": "Mamadaliev",
            "password": "somepassword",
        })

        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(res.context["form"], "username", "A user with that username already exists.")


class LoginTestCase(TestCase):

    def test_successful_login(self):

        test_user = User.objects.create(username="shakhriyor", first_name="Shakhriyor")
        test_user.set_password("somepassword")
        test_user.save()

        self.client.post(reverse("users:login"), data={
            "username": "shakhriyor",
            "password": "somepassword"
        })

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_invalid_credentials(self):
        test_user = User.objects.create(username="shakhriyor", first_name="Shakhriyor")
        test_user.set_password("somepassword")
        test_user.save()

        self.client.post(reverse("users:login"), data={
            "username": "wrong-username",
            "password": "somepassword"
        })

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(reverse("users:login"), data={
            "username": "shakhriyor",
            "password": "wrong-username"
        })

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


