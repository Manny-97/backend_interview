from rest_framework import serializers
from .models import Drone, Medication

class DroneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = Drone
        fields = [
            'id',
            'serial_number',
            'drone_model',
            'weight_limit',
            'battery_capacity',
            'state',
            'medications'
        ]


class MedicationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = Medication
        fields = [
            'id',
            'name',
            'weight',
            'code',
            'image'
        ]