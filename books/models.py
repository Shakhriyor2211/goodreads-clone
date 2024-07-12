from django.utils import timezone

from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from books.utils import generate_unique_slug


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_picture = models.ImageField(default="default_book_cover.png")
    isbn = models.CharField(max_length=17, unique=True, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("books:book_detail", args=[
            self.created_time.year,
            self.created_time.month,
            self.created_time.day,
            self.slug,
        ])

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} by {self.author.first_name} {self.author.last_name}"


class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.stars_given} stars for {self.book} {self.user.username}"
