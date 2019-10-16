from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .models import Ticket
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib import messages
from sales.models import Sale
from django.http import Http404


class TicketAddView(LoginRequiredMixin, CreateView):

    model = Ticket
    template_name = "tickets/add.html"
    success_url = reverse_lazy("tickets:list")
    fields = ("sale", "executive_description", "query_type", "photo")

    def form_valid(self, form):
        # sale = get_object_or_404(Sale, id=form.instance.sale.id, agent=self.request.user)
        if form.instance.sale.agent != self.request.user:
            raise Http404("Wrong Sale")
        messages.success(self.request, "Ticket Raised! We will inform you about its status soon")
        super().form_valid(form)


class TicketListView(LoginRequiredMixin, ListView):

    model = Ticket
    context_object_name = "tickets"
    template_name = "tickets/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(sale__agent=self.request.user)


class TicketDetailView(LoginRequiredMixin, DetailView):

    model = Ticket
    context_object_name = "ticket"
    template_name = "tickets/detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_object(self, queryset=None):
        ticket = super().get_object()
        if ticket.sale.agent == self.request.user:
            return ticket
        raise Http404("Ticket not found!")
