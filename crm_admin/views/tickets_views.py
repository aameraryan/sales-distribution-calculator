from tickets.models import Ticket
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy


class TicketListView(LoginRequiredMixin, ListView):

    model = Ticket
    context_object_name = "tickets"
    template_name = "tickets_admin/list.html"


class TicketDetailView(LoginRequiredMixin, DetailView):

    model = Ticket
    context_object_name = "ticket"
    template_name = "tickets_admin/detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"


# class SaleUpdateView(LoginRequiredMixin, UpdateView):
#
#     model = Sale
#     template_name = "sales_admin/update.html"
#     fields = ("first_commission_paid", "last_commission_paid", "first_commission_pay_on", "last_commission_pay_on", "finance_comment", "status")
#     slug_field = "id"
#     slug_url_kwarg = "id"
#     success_url = reverse_lazy("crm_admin:sales_admin_list")
#
#     def form_valid(self, form):
#         messages.success(self.request, "Sale Updated Successfully")
#         return super().form_valid(form)
