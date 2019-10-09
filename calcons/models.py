from django.db import models
from django.core.validators import MinValueValidator


class Duration(models.Model):

    min_value = models.PositiveIntegerField()
    max_value = models.PositiveIntegerField(blank=True, null=True)
    commission_applicable = models.FloatField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}-{} = {}%".format(self.min_value, self.max_value, self.commission_applicable)


class Bonus(models.Model):

    contract_volume_from = models.PositiveIntegerField()
    contract_volume_to = models.PositiveIntegerField(blank=True, null=True)
    bonus_percent = models.FloatField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}-{} = {}%".format(self.contract_volume_from, self.contract_volume_to, self.bonus_percent)

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
