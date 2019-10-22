from django.conf.urls import url, include
from crm_admin.views import views
from crm_admin.urls import sales_url, tickets_urls, calcons_urls

app_name = "crm_admin"

urlpatterns = [
    # url("^sales/", include(sales_url, namespace="sales_admin")),
    url("^sales/", include(sales_url)),
    url("^tickets/", include(tickets_urls)),
    url("^calcons/", include(calcons_urls)),
    url("^$", views.DashboardView.as_view(), name="dashboard"),
]
