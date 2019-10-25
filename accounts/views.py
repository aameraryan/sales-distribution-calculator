from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("portal:home")
    fields = ("phone", "first_name", "last_name", "photo")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile Updated Successfully.")
        return super().form_valid(form)


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('portal:home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {
        'form': form
    })

