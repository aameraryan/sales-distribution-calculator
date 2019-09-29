from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('portal.urls', namespace='portal')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^sales/', include('sales.urls', namespace='sales')),
    url(r'^tickets/', include('tickets.urls', namespace='tickets')),

]
