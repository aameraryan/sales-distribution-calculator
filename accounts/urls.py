from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, logout_then_login

app_name = "accounts"

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name="accounts/login.html"), name="login"),
    url(r'^logout/$', logout_then_login, name="logout"),
    url(r'^profile_update/$', views.ProfileUpdateView.as_view(), name="profile_update"),
    url(r'^password/change/$', views.password_change, name="password_change"),
]
