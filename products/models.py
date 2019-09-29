from django.db import models
import decimal
import random
import string
from django.urls import reverse_lazy


def product_id_generator():
    random_id = "PR-" + ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6))
    if not Product.objects.filter(product_id=random_id).exists():
        return random_id
    return product_id_generator()


class Product(models.Model):

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    product_id = models.CharField(max_length=32, default=product_id_generator)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    commission_margin = models.FloatField(default=30)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_display_text(self):
        return self.name

    @property
    def get_commission_percent(self):
        return self.commission_margin / 100

    @property
    def calculate_commission_amount(self):
        return round(self.price * decimal.Decimal(round(self.get_commission_percent, 2)), 2)

    @property
    def get_absolute_url(self):
        return reverse_lazy("products:detail", kwargs={"id": self.id})