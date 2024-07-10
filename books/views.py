from django.shortcuts import render, get_object_or_404
from django.views import View

from books.models import Book


class BooksView(View):
    def get(self, request):
        return render(request, "books/index.html", {"books": Book.objects.all()})


class BookDetailView(View):
    def get(self, request, **kwargs):
        return render(request, "books/details.html", {"book": get_object_or_404(Book, slug=kwargs["slug"], created_time__year=kwargs["year"], created_time__month=kwargs["month"], created_time__day=kwargs["day"])})
