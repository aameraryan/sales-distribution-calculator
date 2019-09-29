from django.contrib import admin
from django.contrib.auth.models import User as BaseUser
from accounts.models import User

admin.site.register(BaseUser)
admin.site.register(User)