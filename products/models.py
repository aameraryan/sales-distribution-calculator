from django.db import models
import decimal


class Product(models.Model):

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    product_id = models.CharField(max_length=32)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    commission_margin = models.FloatField(default=30)

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
        return self.price * decimal.Decimal(self.get_commission_percent)
