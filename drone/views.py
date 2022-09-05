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

    @action(methods=['get'], detail=False, url_path='available')
    def available(self, request, *args, **kwargs):
        """ """
        filtered = Drone.objects.filter(
            battery_capacity__gt=25, state__exact='IDLE'
        )
        serializer = self.get_serializer(filtered, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='battery')
    def battery(self, requst, *args, **kwargs):
        """ """
        drone = self.get_object()
        if not drone:
            raise Http404
        serializer = self.get_serializer(drone)
        response_data = {
            'battery_capacity': f"{serializer.data['battery_capacity']}%"
        }
        return Response(response_data)


    @action(detail=True, methods=['get', 'put'])
    def medications(self, request, *args, **kwargs):
        drone: Drone = self.get_object()
        if not drone:
            raise Http404
        if request.method == 'GET':
            load_info = LoadInformation.objects.filter(drone__pk=drone.pk)
            serializer = MedicationSerializer(
                [x.medication for x in load_info], many=True
            )
            quantities = [x.quantity for x in load_info]
            res = [{'quantity': x[0], 'medication': x[1]}
            for x in zip(quantities, serializer.data)]
            return Response(res)
        if request.method == 'PUT':
            med_ids = request.data
            medications = Medication.objects.filter(pk__id=med_ids)
            if len(set(med_ids)) != medications.count():
                stored_ids = [m.pk for m in medications]
                not_found_ids = [id for id in med_ids if id not in stored_ids]
                return Response(data={
                    'detail': f"The following medications ids were not found {not_found_ids}"
                }, status=404)
            # Check the drone weight limit
            weight_medications = sum(
                [sum(med.weight for med in medications if med.pk==_id) for _id in med_ids]
            )
            if drone.weight_limit < weight_medications:
                return Response(data={
                    'detail': "The list of medications cannot be loaded because it exceeds the drone's capacity"
                },status=406)

            # Remove previous rows of LoadInformation db related to the drone
            drone_rows = LoadInformation.objects.filter(drone__pk=drone.pk)
            drone_rows.delete()
            # Create the new relationship in LoadInformation db
            for m in medications:
                load_instance = LoadInformation(
                    drone=drone,
                    medication=m,
                    quantity=len([x for x in med_ids if x==m.pk])
                )
                load_instance.save()
            serializer = self.get_serializer(drone)
            return Response(serializer.data)


class MedicationViewSet(viewsets.ModelViewSet):
    """API endpoint for the medication"""
    allowed_methods = ['get', 'post']
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    # permission_classes = [permissions.IsAuthenticated]
