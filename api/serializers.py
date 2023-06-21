from django.contrib.auth.models import User
from rest_framework import  serializers
from api import models
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_staff', 'is_active']

class USRSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Usr
        fields = '__all__'

class LaunchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Launch
        fields = '__all__'


class VesselSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Vessel
        fields = ['url','date','captain','captainNumber',
                  'owner','ownerNumber','sourcePort','sourceDestination',
                  'status','agenty','file','launch', 'getBalance']