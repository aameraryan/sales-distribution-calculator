from sales.models import Sale
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy


class SaleListView(LoginRequiredMixin, ListView):

    model = Sale
    context_object_name = "sales"
    template_name = "sales_admin/list.html"


class SaleDetailView(LoginRequiredMixin, DetailView):

    model = Sale
    context_object_name = "sale"
    template_name = "sales_admin/detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"


class SaleUpdateView(LoginRequiredMixin, UpdateView):

    model = Sale
    template_name = "sales_admin/update.html"
    fields = ("first_commission_paid", "last_commission_paid", "first_commission_pay_on", "last_commission_pay_on", "finance_comment", "status")
    slug_field = "id"
    slug_url_kwarg = "id"
    success_url = reverse_lazy("crm_admin:sales_admin_list")

    def form_valid(self, form):
        messages.success(self.request, "Sale Updated Successfully")
        return super().form_valid(form)


class PayoutListView(LoginRequiredMixin, TemplateView):

    template_name = "sales_admin/payouts_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        sales = Sale.objects.all()
        context['sales'] = sales
        return context
