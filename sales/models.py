from django.db import models
from accounts.models import User
import random
import string
from django.db.models.signals import post_save
from django.urls import reverse_lazy
from django.core.validators import MinValueValidator, MaxValueValidator
from calcons.models import Bonus, CarDealerBonus, Duration, Multiplier, Payout, PaymentTermINTZ
from django.db.models import Q, Sum
from calcons.calc_constants import MIN_CV_FOR_SETUP_FEE_PAYOUT, FEE_PERCENT_SETUP_FEE_PAYOUT
from payouts.models import Payout


def sale_id_generator():
    random_id = "SL-" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    if not Sale.objects.filter(sale_id=random_id).exists():
        return random_id
    return sale_id_generator()


class Sale(models.Model):

    SALE_STATUS_CHOICES = (("PA", "Pending"), ("AP", "Approved"), ("CP", "Completed"), ("DC", "Declined"))

    agent = models.ForeignKey(User, on_delete=models.CASCADE)

    #   AGENT INPUTS
    campaign_name = models.CharField(max_length=128)
    sale_date = models.DateField()
    setup_fee = models.PositiveIntegerField()
    contract_volume = models.PositiveIntegerField()
    monthly_budget = models.PositiveIntegerField()
    # duration = models.PositiveIntegerField(validators=[MinValueValidator(limit_value=1), ])
    duration = models.ForeignKey(Duration, on_delete=models.PROTECT)
    management_fee = models.PositiveIntegerField()
    car_dealer_amount = models.PositiveIntegerField()
    payment_terms = models.PositiveIntegerField()
    agent_comment = models.TextField(verbose_name="Comment", blank=True)

    #   FINANCE INPUTS
    finance_comment = models.TextField(blank=True)

    #   CALCULATION FIELDS
    commission_applicable = models.FloatField(blank=True, null=True)
    payment_term_intz = models.PositiveIntegerField(blank=True, null=True)
    car_dealer_bonus = models.PositiveIntegerField(blank=True, null=True)
    multiplier_applicable = models.FloatField(blank=True, null=True)

    #   OUTPUT FIELDS
    setup_fee_payout = models.PositiveIntegerField(blank=True, null=True)
    first_payout = models.PositiveIntegerField(blank=True, null=True)
    last_payout = models.PositiveIntegerField(blank=True, null=True)
    bonus_payout = models.PositiveIntegerField(blank=True, null=True)
    total_payout = models.PositiveIntegerField(blank=True, null=True)

    #   IMPORTANT FIELDS
    sale_id = models.CharField(max_length=32, default=sale_id_generator)
    status = models.CharField(max_length=2, choices=SALE_STATUS_CHOICES, default="PA")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} by {} - {}".format(self.campaign_name, self.agent.get_full_name, self.total_payout)

    @property
    def get_absolute_url(self):
        return reverse_lazy("sales:detail", kwargs={"id": self.id})

    @property
    def get_admin_absolute_url(self):
        return reverse_lazy("crm_admin:sales_admin_detail", kwargs={"id": self.id})

    @property
    def get_admin_update_url(self):
        return reverse_lazy("crm_admin:sales_admin_update", kwargs={"id": self.id})

    @property
    def get_raise_ticket_url(self):
        return str(reverse_lazy("tickets:add")) + "?sid={}".format(self.id)

    @property
    def calculate_commission_applicable(self):
        return self.duration.commission_applicable

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

    @property
    def calculate_setup_fee_payout(self):
        if self.contract_volume >= MIN_CV_FOR_SETUP_FEE_PAYOUT:
            return self.setup_fee * (FEE_PERCENT_SETUP_FEE_PAYOUT/100)
        else:
            return 0

    @property
    def calculate_payout(self):
        return (self.monthly_budget or 0.00) * (self.multiplier_applicable or 0.00) * (self.commission_applicable or 0.00)/100

    @property
    def calculate_first_payout(self):
        payout = self.duration.payout
        return self.calculate_payout * payout.fp_percent/100

    @property
    def calculate_last_payout(self):
        payout = self.duration.payout
        return self.calculate_payout * payout.lp_percent/100

    @property
    def get_first_payout_month(self):
        try:
            return self.first_commission_pay_on.strftime("%B %Y")
        except:
            if self.id % 2 == 0:
                return "March 2019"
            else:
                return "June 2019"

    @property
    def get_last_payout_month(self):
        try:
            return self.first_commission_pay_on.strftime("%B %Y")
        except:
            if self.id % 2 == 0:
                return "October 2019"
            else:
                return "May 2019"

    @property
    def calculate_bonus_payout(self):
        bonuses = Bonus.objects.filter(min_contract_volume__lte=self.contract_volume, is_active=True).order_by("min_contract_volume")
        if bonuses.exists():
            return self.contract_volume * bonuses.last().bonus_percent/100
        else:
            return 0

    @property
    def calculate_total_payout(self):
        total_payout = (self.setup_fee_payout or 0) + (self.first_payout or 0) + (self.last_payout or 0) + (self.bonus_payout or 0)
        return total_payout


def assign_commission_applicable(sender, instance, *args, **kwargs):
    if instance.status != "CP":
        cm_ap = instance.calculate_commission_applicable
        if instance.commission_applicable != cm_ap:
            instance.commission_applicable = cm_ap
            instance.save()


def assign_pt_intz(sender, instance, *args, **kwargs):
    if instance.status != "CP":
        pt_intz = instance.calculate_pt_intz
        if instance.payment_term_intz != pt_intz:
            instance.payment_term_intz = pt_intz
            instance.save()


def assign_car_dealer_bonus(sender, instance, *args, **kwargs):
    if instance.status != "CP":
        cd_bonus = instance.calculate_car_dealer_bonus
        if instance.car_dealer_bonus != cd_bonus:
            instance.car_dealer_bonus = cd_bonus
            instance.save()


def assign_multiplier_applicable(sender, instance, *args, **kwargs):
    if instance.status != "CP":
        ml_ap = instance.calculate_multiplier_applicable
        if instance.multiplier_applicable != ml_ap:
            instance.multiplier_applicable = ml_ap
            instance.save()


def assign_setup_fee_payout(sender, instance, *args, **kwargs):
    if instance.status != "CP":
        setup_fee_payout = instance.calculate_setup_fee_payout
        if instance.setup_fee_payout != setup_fee_payout:
            instance.setup_fee_payout = setup_fee_payout
            instance.save()


def assign_payouts(sender, instance, *args, **kwargs):
    if instance.status != "CP":
        first_payout = instance.calculate_first_payout
        last_payout = instance.calculate_last_payout
        if instance.first_payout != first_payout or instance.last_payout != last_payout:
            instance.first_payout = first_payout
            instance.last_payout = last_payout
            instance.save()


def assign_bonus_payout(sender, instance, *args, **kwargs):
    if instance.status != "CP":
        bonus_payout = instance.calculate_bonus_payout
        if instance.bonus_payout != bonus_payout:
            instance.bonus_payout = bonus_payout
            instance.save()


def assign_total_payout(sender, instance, *args, **kwargs):
    if instance.status != "CP":
        total_payout = instance.calculate_total_payout
        if instance.total_payout != total_payout:
            instance.total_payout = total_payout
            instance.save()


def create_payouts(sender, instance, *args, **kwargs):
    if instance.first_payout:
        fp = Payout.objects.get_or_create(sale=instance, payout_type="FP")[0]
        if fp.amount != instance.first_payout:
            fp.amount = instance.first_payout
            fp.save()
    if instance.last_payout:
        lp = Payout.objects.get_or_create(sale=instance, payout_type="LP")[0]
        if lp.amount != instance.last_payout:
            lp.amount = instance.last_payout
            lp.save()


post_save.connect(assign_commission_applicable, sender=Sale)
post_save.connect(assign_pt_intz, sender=Sale)
post_save.connect(assign_car_dealer_bonus, sender=Sale)
post_save.connect(assign_multiplier_applicable, sender=Sale)
post_save.connect(assign_setup_fee_payout, sender=Sale)
post_save.connect(assign_payouts, sender=Sale)
post_save.connect(assign_bonus_payout, sender=Sale)
post_save.connect(assign_total_payout, sender=Sale)
post_save.connect(create_payouts, sender=Sale)
