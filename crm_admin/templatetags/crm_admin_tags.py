from django import template
from sales.models import Sale
from tickets.models import Ticket


register = template.Library()


@register.simple_tag
def get_pending_sale_count():
    return Sale.objects.exclude(status="CP").count()


@register.simple_tag
def get_pending_ticket_count():
    return Ticket.objects.exclude(status__in=("EX", "CN", "SL")).count()
