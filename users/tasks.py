from django.core.mail import send_mail

from goodreads.celery import app

@app.task()
def send_message_email(subject, message, recipient_list):
    print(
        subject,
        message,
        'shakhriyormamadaliev221199@gmail.com',
        recipient_list
    )
    send_mail(
        subject,
        message,
        'shakhriyormamadaliev221199@gmail.com',
        recipient_list
    )

