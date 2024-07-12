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
        Book.objects.create(title="Book5", description="Description5", isbn="123113")

        res = self.client.get(reverse("books:books_list") + "?page_size=3")
        books = Book.objects.all()
        for book in books[:2]:
            self.assertContains(res, book.title)

        res = self.client.get(reverse("books:books_list") + "?page_size=3&page=2")

        for book in books[3:]:
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

    def test_book_search(self):
        Book.objects.create(title="Sport", description="Description1", isbn="122211")
        Book.objects.create(title="Business", description="Description2", isbn="123121")
        Book.objects.create(title="Politics", description="Description3", isbn="123123")

        books = Book.objects.all()

        res = self.client.get(reverse("books:books_list")+"?q=sport")
        self.assertContains(res, books[0].title)
        self.assertNotContains(res, books[1].title)
        self.assertNotContains(res, books[2].title)

        res = self.client.get(reverse("books:books_list") + "?q=business")
        self.assertContains(res, books[1].title)
        self.assertNotContains(res, books[0].title)
        self.assertNotContains(res, books[2].title)

        res = self.client.get(reverse("books:books_list") + "?q=politics")
        self.assertContains(res, books[2].title)
        self.assertNotContains(res, books[0].title)
        self.assertNotContains(res, books[1].title)


