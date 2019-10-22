from calcons.models import Bonus, CarDealerBonus, Multiplier, Duration, PaymentTermINTZ, Payout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy


class CalconsView(LoginRequiredMixin, TemplateView):

    template_name = "calcons_admin/view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['bonuses'] = Bonus.objects.all()
        context['cd_bonuses'] = CarDealerBonus.objects.all()
        context['multipliers'] = Multiplier.objects.all()
        context['durations'] = Duration.objects.all()
        context['pt_intz'] = PaymentTermINTZ.objects.all()
        context['payouts'] = Payout.objects.all()
        return context

