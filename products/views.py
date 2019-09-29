from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from django.http import Http404


class ProductListView(LoginRequiredMixin, ListView):

    model = Product
    context_object_name = "products"
    template_name = "products/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)


class ProductDetailView(LoginRequiredMixin, DetailView):

    model = Product
    context_object_name = "product"
    template_name = "products/detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_object(self, queryset=None):
        product = super().get_object()
        if product.is_active:
            return product
        raise Http404("Product not found!")
