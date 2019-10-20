from django.conf.urls import url
from crm_admin.views import sales_views as views


# app_name = "sales_admin"

urlpatterns = [
    url(r"^list/$", views.SaleListView.as_view(), name="sales_admin_list"),
    url(r"^detail/(?P<id>[0-9]+)/$", views.SaleDetailView.as_view(), name="sales_admin_detail"),
    url(r"^update/(?P<id>[0-9]+)/$", views.SaleUpdateView.as_view(), name="sales_admin_update"),
]
