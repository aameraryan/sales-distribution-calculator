from django.conf.urls import url
from . import views

app_name = "tickets"

urlpatterns = [
    url(r"^add/$", views.TicketAddView.as_view(), name="add"),
    url(r"^list/$", views.TicketListView.as_view(), name="list"),
    url(r'^detail/(?P<id>[0-9]+)/$', views.TicketDetailView.as_view(), name="detail"),
    # url(r'^update/(?P<id>[0-9]+)/$', views.TicketUpdateView.as_view(), name="update"),
]

