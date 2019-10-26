from django.conf.urls import url
from crm_admin.views import tickets_views as views


urlpatterns = [
    url(r"^list/$", views.TicketListView.as_view(), name="tickets_admin_list"),
    url(r"^detail/(?P<id>[0-9]+)/$", views.TicketDetailView.as_view(), name="tickets_admin_detail"),
    url(r"^update/(?P<id>[0-9]+)/$", views.TicketUpdateView.as_view(), name="tickets_admin_update"),
]
