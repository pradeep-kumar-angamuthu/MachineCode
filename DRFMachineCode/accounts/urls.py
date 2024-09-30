# accounts/urls.py
from django.urls import path
from .views import MachineViewSet

machine_list = MachineViewSet.as_view({'get': 'list'})  # if you want to access the list of machines

urlpatterns = [
    path('machines/', machine_list, name='machine-list'),
    path('machines/historical-data/', MachineViewSet.as_view({'get': 'historical_data'}), name='machine-historical-data'),
]
