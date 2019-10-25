from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


MONTH_CHOICES = ((1, "January"), (2, "February"), (3, "March"), (4, "April"), (5, "May"), (6, "June"),
                 (7, "July"), (8, "August"), (9, "September"), (10, "October"), (11, "November"), (12, "December"))


class Payout(models.Model):

    PAYOUT_TYPE_CHOCIES = (("FP", "First Payout"), ("LP", "Last Payout"))
    STATUS_CHOICES = (("PN", "Pending"), ("PD", "Paid"))

    sale = models.ForeignKey("sales.Sale", on_delete=models.CASCADE)
    payout_type = models.CharField(max_length=2, choices=PAYOUT_TYPE_CHOCIES)
    status = models.CharField(max_length=2, default="PN", choices=STATUS_CHOICES)
    amount = models.PositiveIntegerField(default=0.0)

    month = models.PositiveIntegerField(choices=MONTH_CHOICES, validators=[MinValueValidator(limit_value=1), MaxValueValidator(limit_value=12)], blank=True, null=True)
    year = models.PositiveIntegerField(validators=[MinValueValidator(limit_value=1990), MaxValueValidator(2050)], default=timezone.datetime.now().year)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.sale.agent.get_short_name, self.sale.sale_id, self.get_payout_type_display(), self.amount, self.get_status_display())

    @property
    def get_month_year_display(self):
        return "{} {}".format(self.get_month_display(), self.year)
