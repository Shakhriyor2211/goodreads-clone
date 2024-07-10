from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BookTestCase(TestCase):

    def test_no_books(self):
        res = self.client.get(reverse("books:books_list"))

        self.assertContains(res, "No books found.")

    def test_book_fields(self):
        Book.objects.create(title="Book1", description="Description1", isbn="122211")
        Book.objects.create(title="Book2", description="Description2", isbn="123121")
        Book.objects.create(title="Book3", description="Description3", isbn="123123")
        Book.objects.create(title="Book4", description="Description4", isbn="133311")

        res = self.client.get(reverse("books:books_list"))
        books = Book.objects.all()
        for book in books:
            self.assertContains(res, book.title)

    def test_detail(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="122211")

        res = self.client.get(reverse("books:book_detail", args=[
            book.created_time.year,
            book.created_time.month,
            book.created_time.day,
            book.slug,
        ]))

        # res = self.client.get(reverse("books:book_detail", kwargs={
        #     "slug": book.slug,
        #     "year": book.created_time.year,
        #     "month": book.created_time.month,
        #     "day": book.created_time.day
        # }))

        self.assertContains(res, book.title)
        self.assertContains(res, book.description)


