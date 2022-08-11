from rest_framework import serializers
from .models import Drone, Medication
from .utils import validate_size

class DroneSerializer(serializers.ModelSerializer):

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
    medications = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all(), required=False, many=True)
    def validate(self, data):
        validate_size(Drone, serializers.ValidationError)
        return data

    def update(self, instance, valid_data):
        """Prevent the drone from being loaded with more weights than it can carry"""
        if 'medications' in valid_data:
            sum_weight_medications = sum([m.weight for m in valid_data['medications']])
            weight_limit = valid_data['weight_limit'] if 'weight_limit' in valid_data else instance.weight_limit
            if weight_limit < sum_weight_medications:
                raise serializers.ValidationError("Drone's capacity exceeded")
            
        battery_capacity = valid_data['battery_capacity'] if 'battery_capacity' in valid_data else instance.battery_capacity
        state = valid_data['state'] if 'state' in valid_data else instance.state

        if battery_capacity < 25 and state == 'LOADING':
            raise serializers.ValidationError("Drone cannot be in loading state if battery level is below 25%")
        
        super().update(instance=instance, validated_data=valid_data)
        return instance


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