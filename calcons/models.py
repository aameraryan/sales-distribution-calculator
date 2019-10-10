from django.db import models
from django.core.validators import MinValueValidator


class Duration(models.Model):

    min_value = models.PositiveIntegerField()
    max_value = models.PositiveIntegerField(blank=True, null=True)
    commission_applicable = models.FloatField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.get_duration_display_text)

    @property
    def get_duration_display_text(self):
        if self.min_value and self.max_value:
            return "{}-{}".format(self.min_value, self.max_value)
        elif self.min_value and not self.max_value:
            return "{}+".format(self.min_value)


class Bonus(models.Model):

    min_contract_volume = models.PositiveIntegerField()
    max_contract_volume = models.PositiveIntegerField(blank=True, null=True)
    bonus_percent = models.FloatField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}-{} = {}%".format(self.min_contract_volume, self.max_contract_volume, self.bonus_percent)

    class Meta:
        verbose_name = "Bonus"
        verbose_name_plural = "Bonuses"


class Multiplier(models.Model):

    fee_percent = models.FloatField()
    multiplier_applicable = models.FloatField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}% - {}".format(self.fee_percent, self.multiplier_applicable)

    class Meta:
        verbose_name = "Multiplier"
        verbose_name_plural = "Multipliers"


class CarDealerBonus(models.Model):

    car_dealer_amount = models.PositiveIntegerField()
    bonus_amount = models.FloatField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} = {}".format(self.car_dealer_amount, self.bonus_amount)

    class Meta:
        verbose_name = "Car Dealer Bonus"
        verbose_name_plural = "Car Dealer Bonuses"


class PaymentTermINTZ(models.Model):

    VARIABLE_CHOICES = (("PR", "Pre Payment"), ("PS", "Post Payment"))

    variable = models.CharField(max_length=2, choices=VARIABLE_CHOICES)
    max_payment_terms = models.PositiveIntegerField()
    commission = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "max {} ({}) = {}".format(self.max_payment_terms, self.get_variable_display(), self.commission)

    class Meta:
        verbose_name = "Payment Term Incentivization"
        verbose_name_plural = "Payment Term Incentivizations"


class Payout(models.Model):

    duration = models.OneToOneField(Duration, on_delete=models.PROTECT)
    fp_percent = models.FloatField(verbose_name="First Payout Percent",)
    lp_percent = models.FloatField(verbose_name="Last Payout Percent",)

    def __str__(self):
        return "{} | fp:{}, lp:{}".format(self.duration.get_duration_display_text, self.fp_percent, self.lp_percent)
