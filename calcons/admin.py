from django.contrib import admin
from .models import Bonus, CarDealerBonus, Duration, Multiplier, PaymentTermINTZ

admin.site.register(Bonus)
admin.site.register(CarDealerBonus)
admin.site.register(Duration)
admin.site.register(Multiplier)
admin.site.register(PaymentTermINTZ)
