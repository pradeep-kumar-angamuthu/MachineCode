from rest_framework import serializers
from .models import Machine

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'

# serializers.py
class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['machine_id', 'axis_id', 'tool_offset', 'feedrate','tool_in_use','timestamp']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['request'].user.role in ['SUPERVISOR', 'OPERATOR']:
            if self.context['request'].user.role == 'OPERATOR':
                del representation['tool_offset']  # restrict access
        return representation