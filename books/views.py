from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from books.models import Book


# class BooksView(ListView):
#     model = Book
#     template_name = "books/index.html"
#     context_object_name = "books"


class BooksView(View):
    def get(self, request):
        book = Book.objects.all().order_by("id")

        search_query = request.GET.get("q", "")
        if search_query:
            book = book.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        page_size = request.GET.get("page_size", 3)
        paginator = Paginator(book, page_size)

        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)

        return render(request, "books/index.html", {"books": page_obj, "search_query": search_query})


# class BookDetailView(DetailView):
#     model = Book
#     template_name = "books/details.html"
#     context_object_name = "book"
#     slug_url_kwarg = 'slug'
#     query_pk_and_slug = True

class BookDetailView(View):
    def get(self, request, **kwargs):
        return render(request, "books/details.html", {"book": get_object_or_404(Book, slug=kwargs["slug"], created_time__year=kwargs["year"], created_time__month=kwargs["month"], created_time__day=kwargs["day"])})
