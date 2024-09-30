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

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    # permission_classes = [IsSuperAdmin , IsManager , IsSupervisor , IsOperator]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsSuperAdmin()]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return [IsManager() , IsSuperAdmin()]
        elif self.request.method == 'DELETE':
            return [IsSuperAdmin()]
        else:
            return [IsAnyRole()]
        
    # @action(detail=False, methods=['get'])
    # def historical_data(self, request, *args, **kwargs):
    #     time_threshold = timezone.now() - timedelta(minutes=15)
    #     axis = request.query_params.get('axis', None)
    #     if axis:
    #         data = Machine.objects.filter(timestamp__gte=time_threshold, axis__in=axis.split(','))
    #     else:
    #         data = Machine.objects.filter(timestamp__gte=time_threshold)
    #     serializer = self.get_serializer(data, many=True)
    #     return Response(serializer.data)

    # @action(detail=False, methods=['get'])
    # def historical_data(self, request, *args, **kwargs):
    #     time_threshold = timezone.now() - timedelta(minutes=15)
    #     axis = request.query_params.get('axis', None)
        
    #     if axis:
    #         # Assuming axis is a comma-separated string of integers
    #         axis_ids = list(map(int, axis.split(',')))  # Convert to integers
    #         data = Machine.objects.filter(timestamp__gte=time_threshold, axis_id__in=axis_ids)
    #     else:
    #         data = Machine.objects.filter(timestamp__gte=time_threshold)

    #     serializer = self.get_serializer(data, many=True)
    #     return Response(serializer.data)
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
