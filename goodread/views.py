from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class LandingView(TemplateView):
    template_name = "index.html"



class NotFoundView(TemplateView):
    template_name = "404.html"
