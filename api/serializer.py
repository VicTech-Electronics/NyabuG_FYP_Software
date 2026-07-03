from rest_framework import serializers
from management.models import Device

# Create your models serializers here.
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["device_id", "vibration", "noise"]