from rest_framework import viewsets
from .models import Drone, Medication
from .serializers import DroneSerializer, MedicationSerializer

# Create your views here.


class DroneViewSet(viewsets.ModelViewSet):
    """API endpoint for the drone"""
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    # permission_classes = [permissions.IsAuthenticated]


class MedicationViewSet(viewsets.ModelViewSet):
    """API endpoint for the medication"""
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    # permission_classes = [permissions.IsAuthenticated]
