from django.conf.urls import url
from crm_admin.views import calcons_views as views


urlpatterns = [
    url(r"^view/$", views.CalconsView.as_view(), name="calcons_admin_view"),
    # url(r"^detail/(?P<id>[0-9]+)/$", views.TicketDetailView.as_view(), name="tickets_admin_detail"),
    # url(r"^update/(?P<id>[0-9]+)/$", views.SaleUpdateView.as_view(), name="sales_admin_update"),
]
