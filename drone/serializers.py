from rest_framework import serializers
from .models import Drone, Medication
from .utils import validate_size

class DroneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = Drone
        fields = [
            'id',
            'serial_number',
            'drone_model',
            'weight_limit',
            'battery_capacity',
            'state'
        ]
    def validate(self, data):
        validate_size(Drone, serializers.ValidationError)
        return data


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