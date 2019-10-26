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


class TicketUpdateView(LoginRequiredMixin, UpdateView):

    model = Ticket
    template_name = "tickets_admin/update.html"
    fields = ("description", )
    slug_field = "id"
    slug_url_kwarg = "id"
    success_url = reverse_lazy("crm_admin:tickets_admin_list")

    def form_valid(self, form):
        messages.success(self.request, "Ticket Updated Successfully")
        return super().form_valid(form)
