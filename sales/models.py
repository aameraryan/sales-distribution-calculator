from django.db import models
from accounts.models import User
import random
import string
from django.db.models.signals import post_save
from django.urls import reverse_lazy
from django.core.validators import MinValueValidator, MaxValueValidator
from calcons.models import Bonus, CarDealerBonus, Duration, Multiplier, PaymentTermINTZ
from django.db.models import Q, Sum


def sale_id_generator():
    random_id = "SL-" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    if not Sale.objects.filter(sale_id=random_id).exists():
        return random_id
    return sale_id_generator()


class Sale(models.Model):

    SALE_STATUS_CHOICES = (("CR", "Created"), ("AP", "Approved"), ("CP", "Completed"), ("DC", "Declined"))

    agent = models.ForeignKey(User, on_delete=models.CASCADE)

    #   AGENT INPUTS
    product_name = models.CharField(max_length=128)
    sale_date = models.DateField()
    setup_fee = models.PositiveIntegerField()
    contract_volume = models.PositiveIntegerField()
    monthly_budget = models.PositiveIntegerField()
    duration = models.PositiveIntegerField(validators=[MinValueValidator(limit_value=1), ])
    management_fee = models.PositiveIntegerField()
    car_dealer_amount = models.PositiveIntegerField()
    payment_terms = models.PositiveIntegerField()
    agent_comment = models.TextField(blank=True)

    #   FINANCE INPUTS
    first_commission_paid = models.BooleanField(default=False)
    last_commission_paid = models.BooleanField(default=False)
    first_commission_pay_on = models.DateField(blank=True, null=True)
    last_commission_pay_on = models.DateField(blank=True, null=True)
    finance_comment = models.TextField(blank=True)

    #   CALCULATION FIELDS
    commission_applicable = models.FloatField(blank=True, null=True)
    payment_term_intz = models.PositiveIntegerField(blank=True, null=True)
    car_dealer_bonus = models.PositiveIntegerField(blank=True, null=True)
    multiplier_applicable = models.FloatField(blank=True, null=True)

    #   OUTPUT FIELDS
    setup_fee_payout = models.PositiveIntegerField(blank=True, null=True)
    first_payout = models.PositiveIntegerField(blank=True, null=True)
    second_payout = models.PositiveIntegerField(blank=True, null=True)
    bonus_payout = models.PositiveIntegerField(blank=True, null=True)
    total_commission = models.PositiveIntegerField(blank=True, null=True)

    #   IMPORTANT FIELDS
    sale_id = models.CharField(max_length=32, default=sale_id_generator)
    status = models.CharField(max_length=2, choices=SALE_STATUS_CHOICES, default="CR")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} by {} - {}".format(self.product_name, self.agent.get_full_name, self.total_commission)

    @property
    def get_absolute_url(self):
        return reverse_lazy("sales:detail", kwargs={"id": self.id})

    @property
    def calculate_commission_applicable(self):
        durations = Duration.objects.filter(min_value__lte=self.duration, is_active=True).order_by("min_value")
        if durations.exists():
            return durations.last().commission_applicable
        else:
            return 0

    @property
    def calculate_pt_intz(self):
        p_temr_intzs = PaymentTermINTZ.objects.filter(max_payment_terms__gte=self.payment_terms, is_active=True)
        if p_temr_intzs.exists():
            return p_temr_intzs.first().commission
        else:
            return 0

    @property
    def calculate_car_dealer_bonus(self):
        car_dealer_bonuses = CarDealerBonus.objects.filter(car_dealer_amount__lte=self.car_dealer_amount, is_active=True).order_by("car_dealer_amount")
        if car_dealer_bonuses.exists():
            return car_dealer_bonuses.last().bonus_amount
        else:
            return 0

    @property
    def calculate_multiplier_applicable(self):
        multipliers = Multiplier.objects.filter(fee_percent__lte=self.management_fee, is_active=True).order_by("fee_percent")
        if multipliers.exists():
            return multipliers.last().multiplier_applicable
        else:
            return 0


def assign_commission_applicable(sender, instance, *args, **kwargs):
    cm_ap = instance.calculate_commission_applicable
    if instance.commission_applicable != cm_ap:
        instance.commission_applicable = cm_ap
        instance.save()


def assign_pt_intz(sender, instance, *args, **kwargs):
    pt_intz = instance.calculate_pt_intz
    if instance.payment_term_intz != pt_intz:
        instance.payment_term_intz = pt_intz
        instance.save()


def assign_car_dealer_bonus(sender, instance, *args, **kwargs):
    cd_bonus = instance.calculate_car_dealer_bonus
    if instance.car_dealer_bonus != cd_bonus:
        instance.car_dealer_bonus = cd_bonus
        instance.save()


def assign_multiplier_applicable(sender, instance, *args, **kwargs):
    ml_ap = instance.calculate_multiplier_applicable
    if instance.multiplier_applicable != ml_ap:
        instance.multiplier_applicable = ml_ap
        instance.save()


post_save.connect(assign_commission_applicable, sender=Sale)
post_save.connect(assign_pt_intz, sender=Sale)
post_save.connect(assign_car_dealer_bonus, sender=Sale)
post_save.connect(assign_multiplier_applicable, sender=Sale)
