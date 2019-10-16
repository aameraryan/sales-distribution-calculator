from django import forms
from .models import Ticket
from sales.models import Sale

#
# class TicketAddForm(forms.ModelForm):
#
#     class Meta:
#         fields = ("sale", "executive_description", "query_type", "photo")
#         model = Ticket
#
#     def __int__(self, instance=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if instance is not None:
#             self.fields['sale'].queryset = instance.sale_set.all()
