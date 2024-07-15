from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.views.generic import ListView, DetailView

from books.forms import AddReviewForm
from books.models import Book, BookReview


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
        book = get_object_or_404(Book, slug=kwargs["slug"], created_time__year=kwargs["year"],
                                 created_time__month=kwargs["month"], created_time__day=kwargs["day"])
        review_form = AddReviewForm()
        return render(request, "books/details.html", {"book": book, "review_form": review_form})

    def post(self, request, **kwargs):
        review_form = AddReviewForm(data=request.POST)
        book = Book.objects.get(slug=kwargs["slug"])
        if review_form.is_valid():
            BookReview.objects.create(user=request.user, book=book, comment=review_form.cleaned_data["comment"],
                                stars_given=review_form.cleaned_data["stars_given"])

            return redirect(book.get_absolute_url())
            # return redirect(reverse("books:book_detail", kwargs={
            #     "slug": book.slug,
            #     "year": book.created_time.year,
            #     "month": book.created_time.month,
            #     "day": book.created_time.day
            # }))
        return render(request, "books/details.html", {"book": book, "review_form": review_form})
