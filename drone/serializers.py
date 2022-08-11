from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Drone, Medication

class DroneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'group']
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
        model = Group
        fields = ['url', 'name']
        model = Medication
        fields = [
            'id',
            'name',
            'weight',
            'code',
            'image'
        ]