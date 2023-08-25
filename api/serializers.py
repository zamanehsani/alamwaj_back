from django.contrib.auth.models import User
from rest_framework import  serializers
from api import models
from datetime import datetime
# Serializers define the API representation.

class UsrSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usr
        fields = ('type',)
class UserSerializer(serializers.HyperlinkedModelSerializer):
    usr = UsrSerializer()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','url', 'is_staff', 'is_active','usr']

class UserDetailsSerializer(serializers.ModelSerializer):
    usr = UsrSerializer()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','pk', 'usr']

class USRSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Usr
        fields = ['pk', 'type', 'url', 'getUsername', 'user', 'getEmail', 'getUserPK']

class LaunchSerializer(serializers.HyperlinkedModelSerializer):
    vessel_count = serializers.SerializerMethodField()
    class Meta:
        model = models.Launch
        fields = ['pk', 'url', 'number', 'owner', 'ownerNumber', 'note', 'warning','vessel_count']
    
    def get_vessel_count(self, launch):
        return models.Vessel.objects.filter(launch=launch).count()

class VesselSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.Vessel
        fields = ['pk','url','date','captain','captainNumber', 'get_balance','total_discount',
                  'total_manifestation', 'total_expenses','get_extra_parking','get_profit',
                  'total_hamal_fees','get_total_trans_fees','get_total_trans_sell','get_profit',
                  'owner','ownerNumber','sourcePort','DestinationPort', 'total_receivees',
                  'status','agenty','file','launch', 'getTotalBalance','getLaunchNumber','mathrahani','exitReport']

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
        fields = ['pk','url','days','amount','getVessel',
                  'vessel','done_by','note','file', 'getExtraParking','date', 'getDoneByName']

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        parking = super().create(validated_data)

        if file:
            parking.file = file
            parking.save()

        return parking


class VesselExitSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselExit
        fields = ['pk','url','amount', 'getVessel',
                  'vessel','done_by','note','file','date', 'getDoneByName']
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        exit = super().create(validated_data)

        if file:
            exit.file = file
            exit.save()

        return exit
    

class VesselTrueCopySerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselTrueCopy
        fields = ['pk','url','amount', 'getVessel',
                  'vessel','done_by','note','file','date', 'getDoneByName']
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        truecopy = super().create(validated_data)

        if file:
            truecopy.file = file
            truecopy.save()
        return truecopy
    
    
class VesselAttestationSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselAttestation
        fields = ['pk','url','amount', 'getVessel',
                  'vessel','done_by','note','file','date', 'getDoneByName']
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        attest = super().create(validated_data)

        if file:
            attest.file = file
            attest.save()
        return attest
    
class VesselAmendSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselAmend
        fields = ['pk','url','amount', 'getVessel',
                  'vessel','done_by','note','file','date', 'getDoneByName']
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        amend = super().create(validated_data)

        if file:
            amend.file = file
            amend.save()
        return amend
    
class VesselManifestSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselManifest
        fields = ['pk','url','amount', 'getVessel',
                  'vessel','done_by','note','file','date', 'getDoneByName']
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        manifest = super().create(validated_data)

        if file:
            manifest.file = file
            manifest.save()
        return manifest
    
    
class VesselHamaliSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselHamali
        fields = ['pk','url','hamal','hamal_loaded','container','ctn_fees','extra_expense',
                  'getHamalFees', 'getHamalName', 'is_paid', 'paid_amount',
                  'vessel','done_by','note','file','date', 'getDoneByName', 'getVesselNumber']
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        hamal = super().create(validated_data)
        
        if file:
            hamal.file = file
            hamal.save()
        return hamal
    
class VesselAccountSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselAccount
        fields = ['pk','url','note','file','date', 'amount',
                  'vessel','done_by', 'getDoneByName', 'getVesselNumber']
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        acc = super().create(validated_data)
        if file:
            acc.file = file
            acc.save()
        return acc

class VesselExpenseSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselExpenses
        fields = ['pk','url','note','file','date', 'amount',
                  'vessel','done_by', 'getDoneByName', 'getVesselNumber']
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        hamal = super().create(validated_data)
        
        if file:
            hamal.file = file
            hamal.save()
        return hamal
    
class UserExpenseSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.UserExpenseAccount
        fields = ['pk','url','note','file','date', 'amount','done_by', 'getDoneByName', ]
        
    def create(self, validated_data):
        file = validated_data.pop('file', None)
        hamal = super().create(validated_data)
        
        if file:
            hamal.file = file
            hamal.save()
        return hamal
    
class UserReceiveSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.UserReceiveAccount
        fields = ['pk','url','note','file','date', 'amount','done_by', 'getDoneByName', ]

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        hamal = super().create(validated_data)
        
        if file:
            hamal.file = file
            hamal.save()
        return hamal
    
class VesselDiscountSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselDiscount
        fields = ['pk','url','note','file','date', 'amount','done_by', 'getVessel','getDoneByName', 'vessel',]

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        disc = super().create(validated_data)
        
        if file:
            disc.file = file
            disc.save()
        return disc
    
class VesselBookingSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = models.VesselBooking
        fields = ['pk','url','note','file','date', 'paid', 'amount_paid', 
                  'pay_date', 'final_stamp', 'received_by', 'getReceivedByName',
                  'company', 'amount','done_by', 'getVessel','getDoneByName', 'vessel','type']

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        disc = super().create(validated_data)
        if file:
            disc.file = file
            disc.save()
        return disc
    
    def update(self, instance, validated_data):
        amount_paid = validated_data.pop('amount_paid', None)
        instance = super().update(instance, validated_data)
        if amount_paid:
            print("amount paid: ")
            instance.amount_paid = amount_paid
            instance.pay_date = datetime.now()  # Set pay_date to current date and time
            instance.save()
            print("amount paid saved: ", instance.amount_paid)
        return instance

class HSCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.HS_codes
        fields = ['pk','url','code','description','category']

    
class CompanySerializer(serializers.HyperlinkedModelSerializer):
    logo = serializers.FileField(required=False)
    class Meta:
        model = models.Company
        fields = ['pk','url','name','address','logo','trn', 'tel','mob', 
                  'pob','email']

    def create(self, validated_data):
        logo = validated_data.pop('logo', None)
        instance = super().create(validated_data)
        if logo:
            instance.logo = logo
            instance.save()
        return instance
    
