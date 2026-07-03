from django.urls import path
from . import views

urlpatterns = [
    path("", views.documentation),
    path("device-data/", views.deviceData),
    path("deactivate-device/", views.deactivateDevice)
]