from turtle import title
from django.urls import path, include
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Backend')


router = routers.DefaultRouter()
router.register(r'drones', views.DroneViewSet)
router.register(r'medication', views.MedicationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
