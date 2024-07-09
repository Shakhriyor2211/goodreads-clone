from django.urls import path

from books.views import BooksView, BookDetailView

urlpatterns = [
    path("", BooksView.as_view(), name="books"),
    path("detils/<slug:slug>", BookDetailView.as_view(), name="book_detail")
]
