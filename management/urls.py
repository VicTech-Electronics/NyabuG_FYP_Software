from django.urls import path
from . import views

urlpatterns = [
    path("", views.security, name="security"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("fault-history/", views.showFaults, name="fault_history"),
    path("delete-fault/", views.deleteFault, name="delete_fault"),
]
