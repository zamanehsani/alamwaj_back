
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from api import serializers, models

# Create your views here.
# ViewSets define the view behavior.
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