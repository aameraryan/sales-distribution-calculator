from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin2/', admin.site.urls),
    url(r'^admin/', include('crm_admin.urls', namespace='crm_admin')),
    url(r'^', include('portal.urls', namespace='portal')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^sales/', include('sales.urls', namespace='sales')),
    url(r'^tickets/', include('tickets.urls', namespace='tickets')),
    url(r'^payouts/', include('payouts.urls', namespace='payouts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
