from django.contrib import admin

# Register your models here.

from .models import Admin, Machine, User

admin.site.register(Admin)
admin.site.register(Machine)
admin.site.register(User)
