from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from books.models import BookReview


class LandingView(TemplateView):
    template_name = "index.html"



class HomeView(View):
    def get(self, request):

        book_reviews = BookReview.objects.all().order_by("-created_time")

        size = request.GET.get("page_size", 2)
        paginator = Paginator(book_reviews, size)

        page = request.GET.get("page", 1)
        page_obj = paginator.get_page(page)

        return render(request, "home.html", {"page_obj": page_obj})





class NotFoundView(TemplateView):
    template_name = "404.html"


