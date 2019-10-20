from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin_def/', admin.site.urls),
    url(r'^crm_admin/', include('crm_admin.urls', namespace='crm_admin')),
    url(r'^', include('portal.urls', namespace='portal')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^sales/', include('sales.urls', namespace='sales')),
    url(r'^tickets/', include('tickets.urls', namespace='tickets')),

]
