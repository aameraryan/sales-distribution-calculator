from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):

    template_name = "portal/home.html"
