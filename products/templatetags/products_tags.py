from django import template

register = template.Library()


@register.simple_tag
def get_user_product_sales_count(user, product):
    return product.sale_set.filter(user=user).count()
