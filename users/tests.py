from django.contrib.auth import get_user
from users.models import CustomUser
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
        user = CustomUser.objects.get(username="shakhriyor")
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

        user_count = CustomUser.objects.count()
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

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(res.context["form"], "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username="shakhriyor", first_name="Shakhriyor")
        user.set_password("somepassword")
        user.save()

        res = self.client.post(reverse("users:register"), data={
            "username": "shakhriyor",
            "email": "shakhriyormamadaliev@gmail.com",
            "first_name": "Shakhriyor",
            "last_name": "Mamadaliev",
            "password": "somepassword",
        })

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(res.context["form"], "username", "A user with that username already exists.")


class LoginTestCase(TestCase):

    def setUp(self):
        test_user = CustomUser.objects.create(username="shakhriyor", first_name="Shakhriyor", last_name="Mamadaliev",
                                        email="shakhriyormamadaliev@gmail.com")
        test_user.set_password("somepassword")
        test_user.save()


    def test_successful_login(self):
        self.client.post(reverse("users:login"), data={
            "username": "shakhriyor",
            "password": "somepassword"
        })

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_invalid_credentials(self):
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

    def test_logout(self):
        self.client.login(username="shakhriyor", password="somepassword")
        self.client.logout()
        # self.client.get(reverse("users:logout"))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):

    def test_login_required(self):
        res = self.client.get(reverse("users:profile"))

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        test_user = CustomUser.objects.create(username="shakhriyor", first_name="Shakhriyor", last_name="Mamadaliev",
                                        email="shakhriyormamadaliev@gmail.com")
        test_user.set_password("somepassword")
        test_user.save()

        self.client.login(username="shakhriyor", password="somepassword")

        res = self.client.get(reverse("users:profile"))


        self.assertEqual(res.status_code, 200)
        self.assertContains(res, test_user.username)
        self.assertContains(res, test_user.first_name)
        self.assertContains(res, test_user.last_name)
        self.assertContains(res, test_user.email)


    def test_update_profile(self):
        test_user = CustomUser.objects.create(username="shakhriyor", first_name="Shakhriyor", last_name="Mamadaliev",
                                        email="shakhriyormamadaliev@gmail.com")
        test_user.set_password("somepassword")

        test_user.save()

        self.client.login(username="shakhriyor", password="somepassword")

        res = self.client.post(reverse("users:update_profile"), data={
            "username": "John123",
            "email": "example@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
        })

        test_user.refresh_from_db()

        self.assertEqual(test_user.username, "John123")
        self.assertEqual(test_user.email, "example@gmail.com")
        self.assertEqual(test_user.first_name, "John")
        self.assertEqual(test_user.last_name, "Doe")
        self.assertEqual(res.url, reverse("users:profile"))





