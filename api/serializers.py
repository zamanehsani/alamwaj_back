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
        fields = ['pk', 'url', 'number', 'owner', 'ownerNumber']


class VesselSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.Vessel
        fields = ['pk','url','date','captain','captainNumber',
                  'owner','ownerNumber','sourcePort','DestinationPort',
                  'status','agenty','file','launch', 'getBalance','getLaunchNumber']

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        vessel = super().create(validated_data)
        if file:
            vessel.file = file
            vessel.save()

        return vessel
    
    
class VesselParkingSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselParking
        fields = ['pk','url','days','amount',
                  'vessel','done_by','note','file', 'getExtraParking','date', 'getDoneByName']

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        parking = super().create(validated_data)

        if file:
            parking.file = file
            parking.save()

        return parking