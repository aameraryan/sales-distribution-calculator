from django.db import models
import random
import string


def ticket_id_generator():
    random_id = "TK-" + ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6))
    if not Ticket.objects.filter(ticket_id=random_id).exists():
        return random_id
    return ticket_id_generator()


class Ticket(models.Model):

    TICKET_STATUS_CHOICES = (("IN", "Initiated"), ("PR", "Processing"), ("SL", "Solved"), ("CN", "Cancelled"), ("EX", "Expired"))
    QUERY_TYPE_CHOICES = (("PR", "Price"), ("PM", "Payment"), ("OT", "Other"))

    ticket_id = models.CharField(max_length=32, default=ticket_id_generator)

    sale = models.ForeignKey("sales.Sale", on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=TICKET_STATUS_CHOICES, default="IN")
    query_type = models.CharField(max_length=2, choices=QUERY_TYPE_CHOICES, default="OT")

    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="tickets/photos/", blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    solved_on = models.DateTimeField(blank=True, null=True)
    executive_description = models.TextField(blank=True)

    def __str__(self):
        return "{} {} ({})".format(self.sale.user.get_full_name, self.sale.sale_id, self.get_query_type_display())
