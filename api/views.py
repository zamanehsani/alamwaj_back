
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from api import serializers, models
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class USRViewSet(viewsets.ModelViewSet):
    queryset = models.Usr.objects.all()
    serializer_class = serializers.USRSerializer


class LaunchViewSet(viewsets.ModelViewSet):
    queryset = models.Launch.objects.all()
    serializer_class = serializers.LaunchSerializer

class VesselViewSet(viewsets.ModelViewSet):
    queryset = models.Vessel.objects.all()
    serializer_class = serializers.VesselSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class ParkingViewSet(viewsets.ModelViewSet):
    queryset = models.VesselParking.objects.all()
    serializer_class = serializers.VesselParkingSerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VesselParkingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselParkingSerializer
    queryset = models.VesselParking.objects.all()

    def get_queryset(self):
        queryset = models.VesselParking.objects.all()
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    