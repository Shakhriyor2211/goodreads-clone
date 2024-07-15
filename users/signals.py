from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # send_mail("Welcome to Goodreads", f"Hi {instance.username} to world of books. Enjoy the books and reviews.",
        #           "shakhriyormamadaliev221199@gmail.com", [instance.email])
        print("Welcome to Goodreads", f"Hi {instance.username} to world of books. Enjoy the books and reviews.",
                          "shakhriyormamadaliev221199@gmail.com", [instance.email])
