from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sale
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib import messages


class SaleListView(LoginRequiredMixin, ListView):

    model = Sale
    context_object_name = "sales"
    template_name = "sales/list.html"
    ordering = "-id"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(agent=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['pending_sales'] = context['sales'].filter(status="PA")
        context['approved_sales'] = context['sales'].filter(status="AP")
        context['completed_sales'] = context['sales'].filter(status="CP")
        print(context)
        return context


class SaleAddView(LoginRequiredMixin, CreateView):

    model = Sale
    template_name = "sales/add.html"
    success_url = reverse_lazy("sales:list")
    fields = ("campaign_name", "sale_date", "setup_fee", "contract_volume", "monthly_budget", "duration",
              "management_fee", "car_dealer_amount", "payment_terms", "agent_comment")

    def form_valid(self, form):
        form.instance.agent = self.request.user
        sale = form.save()
        self.success_url = sale.get_absolute_url
        messages.success(self.request, "Sale Created Successfully - {}".format(sale.sale_id))
        return super().form_valid(form)


class SaleDetailView(LoginRequiredMixin, DetailView):

    model = Sale
    context_object_name = "sale"
    template_name = "sales/detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_object(self, queryset=None):
        sale = super().get_object()
        if sale.agent == self.request.user:
            return sale
        raise Http404("Sale not found!")
