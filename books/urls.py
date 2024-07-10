from django.urls import path

from books.views import BooksView, BookDetailView

app_name = "books"

urlpatterns = [
    path("", BooksView.as_view(), name="books_list"),
    path("detils/<int:year>/<int:month>/<int:day>/<slug:slug>/", BookDetailView.as_view(), name="book_detail")
]
