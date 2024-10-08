# accounts/urls.py
from django.urls import path,include
from .views import MachineViewSet
from .views import RegisterUserView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'machines', MachineViewSet, basename='machine')


machine_list = MachineViewSet.as_view({'get': 'list'})  # if you want to access the list of machines

urlpatterns = [
    # path('machine/', machine_list, name='machine-list'),
    path('machines/historical-data/', MachineViewSet.as_view({'get': 'historical_data'}), name='machine-historical-data'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('', include(router.urls)),
]

