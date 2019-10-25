from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy


class UserListView(LoginRequiredMixin, ListView):

    model = User
    context_object_name = "users"
    template_name = "accounts_admin/user_list.html"


class UserAddView(LoginRequiredMixin, CreateView):

    model = User
    template_name = "accounts_admin/user_add.html"
    fields = ("email", "phone", "first_name", "last_name", "account_type", "is_active", "password")
    success_url = reverse_lazy("crm_admin:ac_admin_user_list")

    def form_valid(self, form):
        messages.success(self.request, "User Created Successfully")
        return super().form_valid(form)

#
# class TicketDetailView(LoginRequiredMixin, DetailView):
#
#     model = Ticket
#     context_object_name = "ticket"
#     template_name = "tickets_admin/detail.html"
#     slug_field = "id"
#     slug_url_kwarg = "id"


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
