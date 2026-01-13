from django.contrib import admin
from .models import Admin, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Admin)
