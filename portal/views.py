from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect("crm_admin:dashboard")
        else:
            return super().get(request, *args, **kwargs)

    template_name = "portal/home.html"


class TermsConditionsView(LoginRequiredMixin, TemplateView):

    template_name = "portal/terms_conditions.html"
