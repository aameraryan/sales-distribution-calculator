from django.conf.urls import url
from . import views

app_name = "sales"

urlpatterns = [
    url(r'^list/$', views.SaleListView.as_view(), name="list"),
    url(r'^add/$', views.SaleAddView.as_view(), name="add"),
    url(r'^detail/(?P<id>[0-9]+)/$', views.SaleDetailView.as_view(), name="detail"),


]
