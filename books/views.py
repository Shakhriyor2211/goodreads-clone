from django.shortcuts import render
from django.views import View

from books.models import Book


class BooksView(View):
    def get(self, request):
        return render(request, "books/index.html", {"books": Book.objects.all()})


class BookDetailView(View):
    def get(self, request, slug):
        return render(request, "books/details.html", {"book": Book.objects.get(slug=slug)})