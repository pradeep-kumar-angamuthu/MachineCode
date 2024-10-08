from rest_framework import serializers
from .models import Machine



from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

    def create(self, validated_data):
        # Create the user with the hashed password
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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