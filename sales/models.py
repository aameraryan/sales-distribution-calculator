from django.db import models
from accounts.models import User
import random
import string


def sale_id_generator():
    random_id = "SL" + ''.join(random.choice(string.ascii_uppercase) for i in range(8))
    if not Sale.objects.filter(sale_id=random_id).exists():
        return random_id
    return sale_id_generator()


class Sale(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)

    sale_id = models.CharField(max_length=32, default=sale_id_generator)

    commission_amount = models.DecimalField(max_digits=8, decimal_places=2)
    sale_date = models.DateField()

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} by {} - {}".format(self.product.name, self.user.get_full_name, self.commission_amount)
