from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'drones', views.DroneViewSet)
router.register(r'medication', views.MedicationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
