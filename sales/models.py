from django.db import models
from accounts.models import User
import random
import string
from django.db.models.signals import post_save
from django.urls import reverse_lazy


def sale_id_generator():
    random_id = "SL-" + ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6))
    if not Sale.objects.filter(sale_id=random_id).exists():
        return random_id
    return sale_id_generator()


class Sale(models.Model):

    SALE_STATUS_CHOICES = (("CR", "Created"), ("AP", "Approved"), ("CP", "Completed"), ("DC", "Declined"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)

    sale_id = models.CharField(max_length=32, default=sale_id_generator)
    status = models.CharField(max_length=2, choices=SALE_STATUS_CHOICES, default="CR")
    description = models.TextField(blank=True)

    commission_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sale_date = models.DateField()

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} by {} - {}".format(self.product.name, self.user.get_full_name, self.commission_amount)

    @property
    def get_absolute_url(self):
        return reverse_lazy("sales:detail", kwargs={"id": self.id})


def assign_commission_amount(sender, created, instance, *args, **kwargs):
    commission_amount = instance.product.calculate_commission_amount
    if instance.commission_amount != commission_amount:
        instance.commission_amount = commission_amount
        instance.save()


post_save.connect(assign_commission_amount, sender=Sale)
