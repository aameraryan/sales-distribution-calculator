from django.conf.urls import url, include


urlpatterns = [
    url(r'^sales/', include("sales.admin_urls", namespace="sales_admin"))
]