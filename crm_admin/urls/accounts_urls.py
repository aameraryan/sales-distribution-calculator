from django.conf.urls import url
from crm_admin.views import accounts_views as views


urlpatterns = [
    url(r"^users/list/$", views.UserListView.as_view(), name="ac_admin_user_list"),
    url(r"^users/add/$", views.UserAddView.as_view(), name="ac_admin_user_add"),
    # url(r"^detail/(?P<id>[0-9]+)/$", views.TicketDetailView.as_view(), name="tickets_admin_detail"),
    # url(r"^update/(?P<id>[0-9]+)/$", views.SaleUpdateView.as_view(), name="sales_admin_update"),
]
