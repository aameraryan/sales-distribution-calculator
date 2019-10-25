from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Payout
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib import messages


class PayoutListView(LoginRequiredMixin, ListView):

    model = Payout
    context_object_name = "payouts"
    template_name = "payouts/list.html"
    ordering = "-id"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(sale__agent=self.request.user)
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     context['pending_sales'] = context['sales'].filter(status="PA")
    #     context['approved_sales'] = context['sales'].filter(status="AP")
    #     context['completed_sales'] = context['sales'].filter(status="CP")
    #     print(context)
    #     return context
