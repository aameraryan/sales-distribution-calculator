from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Payout
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib import messages


class PayoutListView(LoginRequiredMixin, TemplateView):

    template_name = "payouts/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        sales = self.request.user.sale_set.all()
        context['sales'] = sales
        return context

    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     context['pending_sales'] = context['sales'].filter(status="PA")
    #     context['approved_sales'] = context['sales'].filter(status="AP")
    #     context['completed_sales'] = context['sales'].filter(status="CP")
    #     print(context)
    #     return context
