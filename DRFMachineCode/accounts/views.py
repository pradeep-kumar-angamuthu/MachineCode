from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Machine
from .serializers import MachineSerializer
from .permissions import IsSuperAdmin, IsManager, IsSupervisor, IsOperator, IsAnyRole

from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Get role from request and assign it to the user
            role = request.data.get('role', 'OPERATOR')  # Default role is OPERATOR
            if role not in [choice[0] for choice in User.ROLE_CHOICES]:
                return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
            user.role = role
            user.save()

            return Response({"message": "User created successfully", "role": user.role}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [IsSuperAdmin , IsManager , IsSupervisor , IsOperator]
    lookup_field = 'machine_id'

    def get_permissions(self):
        if self.request.method == 'POST':
            if self.request.user.role == 'SUPERADMIN':
                return [IsSuperAdmin()]
            elif self.request.user.role == 'MANAGER':
                return [IsManager()]
            elif self.request.user.role == 'SUPERVISOR':
                return [IsSupervisor()]
            else:
                return []  # Return an empty list instead of False
        elif self.request.method in ['PUT', 'PATCH']:
            if self.request.user.role == 'SUPERADMIN':
                return [IsSuperAdmin()]
            elif self.request.user.role == 'MANAGER':
                return [IsManager()]
            else:
                return []  # Return an empty list instead of False
        elif self.request.method == 'DELETE':
            if self.request.user.role == 'SUPERADMIN':
                return [IsSuperAdmin()]
            elif self.request.user.role == 'SUPERVISOR':
                return [IsSupervisor()]
            else:
                return []  # Return an empty list instead of False
        else:
            return [IsAnyRole()]  # Default permission for other methods
        

    def create(self, request, *args, **kwargs):
        """
        Handle machine creation based on user role.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if self.request.user.role == 'SUPERADMIN':
                # SUPERADMIN can create the machine as-is
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif self.request.user.role in ['MANAGER', 'SUPERVISOR']:
                # MANAGER and SUPERVISOR can create machines, but tool_in_use is set to 0
                serializer.validated_data['tool_in_use'] = 0
                serializer.save()  # Save the machine with modified data
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Any other role does not have permission to create machines
                return Response({"error": "You do not have permission to create machines."}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        # Role-based field-level access control for update
        user_role = request.user.role
        machine = request.data.get('machine_id')
        data = request.data

        if user_role == 'SUPERADMIN' or (user_role == 'MANAGER' and 'tool_in_use' not in data):
            return super().update(request, *args, **kwargs)
        elif user_role == 'MANAGER' and 'tool_in_use' in data:
            return Response({"error": "Managers cannot update 'tool_in_use'."}, status=status.HTTP_403_FORBIDDEN)
        elif user_role == 'SUPERVISOR' and ('tool_in_use' in data and data['tool_in_use'] != machine.tool_in_use):
            return Response({"error": "Supervisors cannot update 'tool_in_use'."}, status=status.HTTP_403_FORBIDDEN)
        elif user_role == 'OPERATOR' and 'tool_in_use' not in data:
            return Response({"error": "Operators can only update 'tool_in_use'."}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Only SUPERADMIN can delete a machine
        if request.user.role != 'SUPERADMIN':
            return Response({"error": "You do not have permission to delete machines."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)    
    
    @action(detail=False, methods=['get'],permission_classes=[IsOperator])
    def historical_data(self, request, *args, **kwargs):
        time_threshold = timezone.now() - timedelta(minutes=300)
        axis = request.query_params.get('axis_id', None)
        print(type(axis))
        if axis:
            try:
                # Convert the axis parameter to a list of integers
                axis_ids = [int(a) for a in axis.split(',')]
                data = Machine.objects.filter( axis_id__in=axis_ids)  #timestamp__gte=time_threshold,
                print(data)
            except ValueError:
                return Response({"error": "Invalid axis id format"}, status=400)  # Handle conversion error
        else:
            data = Machine.objects.filter(timestamp__gte=time_threshold)

        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

