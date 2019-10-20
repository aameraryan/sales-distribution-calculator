from django.contrib import admin
from .models import Bonus, CarDealerBonus, Duration, Multiplier, PaymentTermINTZ, Payout

admin.site.site_title = "Hero Leads Administration"
admin.site.site_header = "Hero Leads Administration"


admin.site.register(Bonus)
admin.site.register(CarDealerBonus)
admin.site.register(Duration)
admin.site.register(Multiplier)
admin.site.register(Payout)
admin.site.register(PaymentTermINTZ)
