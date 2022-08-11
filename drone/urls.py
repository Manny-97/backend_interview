from django.urls import path, include
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'drones', views.DroneViewSet)
router.register(r'medication', views.MedicationViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
