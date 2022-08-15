from rest_framework import viewsets
from django.http.response import Http404
from .models import Drone, Medication, LoadInformation
from .serializers import DroneSerializer, MedicationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from drone import serializers

# Create your views here.


class DroneViewSet(viewsets.ModelViewSet):
    """API endpoint for the drone"""
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    allowed_methods = ['get', 'post', 'patch', 'put']
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False, url_name='available')
    def available(self, request, *args, **kwargs):
        """ """
        filtered = Drone.objects.filter(
            battery_capacity__gt=25, state__exact='IDLE'
        )
        serializer = self.get_serializer(filtered, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_name='battery')
    def battery(self, requst, *args, **kwargs):
        """ """
        drone: Drone = self.get_object()
        if not drone:
            raise Http404
        serializer = self.get_serializer(drone)
        response_data = {
            'battery_capacity': f"{serializer.data['battery_capacity']}%"
        }
        return Response(response_data)



class MedicationViewSet(viewsets.ModelViewSet):
    """API endpoint for the medication"""
    allowed_methods = ['get', 'post']
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    # permission_classes = [permissions.IsAuthenticated]
