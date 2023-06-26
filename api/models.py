from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Usr(models.Model):
    type = models.CharField(max_length=30,null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

class Launch(models.Model):
    number = models.CharField(max_length=30)
    owner = models.CharField(max_length=30, null=True,blank=True)
    ownerNumber = models.CharField(max_length=15, null=True,blank=True)
    def __str__(self):
        return self.number


def generate_file_path(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    launch_number = instance.launch.number
    filename = f"{timestamp}-{launch_number}"
    return f"vessels/{filename}/{filename}"
    

class Vessel(models.Model):
    launch = models.ForeignKey(Launch,on_delete=models.CASCADE)
    captain = models.CharField(max_length=30)
    captainNumber = models.CharField(max_length=15)
    owner = models.CharField(max_length=30,null=True,blank=True)
    ownerNumber = models.CharField(max_length=15,null=True,blank=True)
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    sourcePort = models.CharField(max_length=30, null=True,blank=True)
    DestinationPort = models.CharField(max_length=30, null=True,blank=True)
    status = models.CharField(max_length=30, null=True,blank=True)
    agenty = models.DecimalField(max_digits=8, decimal_places=2, null=True,blank=True)
    file = models.FileField(upload_to=generate_file_path, null=True,blank=True)

    def __str__(self):
        return self.launch.number
    
    def save(self, *args, **kwargs):
        launch = self.launch  # Get the associated Launch instance
        self.owner = launch.owner  # Set owner from Launch owner
        self.ownerNumber = launch.ownerNumber  # Set ownerNumber from Launch ownerNumber
        super().save(*args, **kwargs)  # Call the original save method


    # get the balance
    def getBalance(self, *args, **kwargs):
        return self.agenty
    def getLaunchNumber(self, *args, **kwargs):
        return self.launch.number
    

def generate_file_path(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    launch_number = instance.vessel
    filename = f"{timestamp}-{launch_number}"
    return f"vessels/{filename}/parking"

class VesselParking(models.Model):
    vessel = models.ForeignKey(Vessel,on_delete=models.CASCADE)
    days = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=generate_file_path, null=True,blank=True)
    note = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.vessel.launch.number
    

    # get the balance
    def getExtraParking(self, *args, **kwargs): 
        # amount / days = one day and one day * (days-3)
        if self.days <= 3:
            return 0
        return int((self.amount / self.days) * ( self.days - 3))
    
    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
