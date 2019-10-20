from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "crm_admin/dashboard.html"
    # template_name = "crm_admin/dajngo_dsbrd.html"
