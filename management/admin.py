from django.contrib import admin
from .models import Device, Fault

# Register your models here.
admin.site.register(Device)
admin.site.register(Fault)