from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
import decimal

class Usr(models.Model):
    type = models.CharField(max_length=30,null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)
    def getUsername(self):
        return self.user.username
    def getEmail(self):
        return self.user.email
    def getUserPK(self):
        return self.user.pk

class Launch(models.Model):
    number      = models.CharField(max_length=6, unique=True)
    owner       = models.CharField(max_length=30, null=True,blank=True)
    ownerNumber = models.CharField(max_length=15, null=True,blank=True)
    note        = models.TextField(blank=True, null=True)
    warning     = models.BooleanField(default=False)

    def __str__(self):
        return self.number
    

def user_file_path(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    user = instance.done_by
    filename = f"{timestamp}-{user}"
    return f"{user}/{filename}"

def generate_file_path(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    launch_number = instance.launch.number
    filename = f"{timestamp}-{launch_number}"
    return f"vessels/{filename}/{filename}"

def exitReport_file_path(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    launch_number = instance.launch.number
    filename = f"{timestamp}-{launch_number}"
    return f"vessels/{filename}/exit-report-{filename}"

def mathrahani_file(instance, filename):
    timestamp = timezone.now().strftime('%d%m%Y')
    launch_number = instance.launch.number
    filename = f"{timestamp}-{launch_number}"
    return f"vessels/{filename}/mathrahani"
    

class Vessel(models.Model):
    launch = models.ForeignKey(Launch,on_delete=models.CASCADE,)
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
    mathrahani = models.FileField(upload_to=mathrahani_file, null=True,blank=True)
    exitReport = models.FileField(upload_to=exitReport_file_path, null=True,blank=True)
    
    def __str__(self):
        return self.launch.number
    
    def save(self, *args, **kwargs):
        launch = self.launch  # Get the associated Launch instance
        self.owner = launch.owner  # Set owner from Launch owner
        self.ownerNumber = launch.ownerNumber  # Set ownerNumber from Launch ownerNumber
        super().save(*args, **kwargs)  # Call the original save method


    # get the balance
    def getTotalBalance(self, *args, **kwargs):

        a = self.get_extra_parking()
        a+= self.total_expenses()
        a+= self.agenty
        return a
    
    def getLaunchNumber(self, *args, **kwargs):
        return self.launch.number
    
    def total_manifestation(self):
        true_copy = self.vesseltruecopy_set.all()  #VesselTrueCopy.objects.filter(vessel=self)
        total_tc = true_copy.aggregate(Sum('amount'))['amount__sum'] or 0

        manifest = self.vesselmanifest_set.all() # VesselManifest.objects.filter(vessel=self)
        total_manifest = manifest.aggregate(Sum('amount'))['amount__sum'] or 0
        
        parking =self.vesselparking_set.all() # VesselParking.objects.filter(vessel=self)
        total_parking = parking.aggregate(Sum('amount'))['amount__sum'] or 0
        
        exit = self.vesselexit_set.all() # VesselExit.objects.filter(vessel=self)
        total_exit =  exit.aggregate(Sum('amount'))['amount__sum'] or 0
        
        attestation = self.vesselattestation_set.all() # VesselAttestation.objects.filter(vessel=self)
        total_attest = attestation.aggregate(Sum('amount'))['amount__sum'] or 0
        
        amend = self.vesselamend_set.all() # VesselAmend.objects.filter(vessel=self)
        total_amend = amend.aggregate(Sum('amount'))['amount__sum'] or 0
        
        total_manifestation = total_tc + total_manifest + total_parking + total_exit + total_attest + total_amend 
        
        return total_manifestation if total_manifestation else 0
    
    def total_expenses(self):
        expenses = self.vesselexpenses_set.all() # VesselExpenses.objects.filter(vessel=self)
        total = expenses.aggregate(Sum('amount'))['amount__sum']
        return total if total else 0
    
    def total_discount(self):
        discounts = VesselDiscount.objects.filter(vessel=self)
        total = discounts.aggregate(Sum('amount'))['amount__sum']
        return total if total else 0
    
    def get_extra_parking(self):
        park = self.vesselparking_set.all()
        total = 0
        for i in park:
            total += i.getExtraParking()
        return total if total else 0
    
    def total_receivees(self):
        receiveds =self.vesselaccount_set.all() # VesselAccount.objects.filter(vessel=self)
        total_receivees = receiveds.aggregate(Sum('amount'))['amount__sum']
        return total_receivees if total_receivees else 0
    
    def get_balance(self):
        discount = self.total_discount()
        expense = self.total_expenses()
        received = self.total_receivees()
        extra_park = self.get_extra_parking()

        exp, obtain = 0, 0
        if discount:
            obtain += discount
        if received:
            obtain += received
        if expense:
            exp += expense
        if extra_park:
            exp += extra_park
        if self.agenty:
            exp += int(self.agenty)
        else:
            exp += 3500 
            # exp += int(os.getenv('DEFAULT_AGENTY'))

        balance = int(exp - obtain)

        if balance < 0:
            return 0
        return balance 

    # def total_hamal_fees(self):
    #     res = 0
    #     for loading in self.hammal_set.all():
    #         res +=loading.hamalFee()
    #     return res
    
    # def get_total_transites_amount(self):
    #     transites = Transites.objects.filter(vessel=self)
    #     total_amount = transites.aggregate(Sum('amount'))['amount__sum']
    #     return total_amount if total_amount else 0

    # def get_alamwaj_transites_fee(self):
    #     transites = Transites.objects.filter(vessel=self, booked_by='alamwaj')
    #     local_tax_fee = 125
    #     transite_fee = 295
    #     total_fee = 0
    #     for t in transites:
    #         if t.type == 'local' or t.type == 'tax':
    #             total_fee += local_tax_fee
    #         elif t.type == 'transite':
    #             total_fee += transite_fee

    #     return total_fee if total_fee else 0
    
    def get_profit(self):
        total_manifestations = self.total_manifestation()
        total_expense = self.total_expenses()
        # total_hamali = self.total_hamal_fees()
        # total_booking = self.get_alamwaj_transites_fee()
        
        # total_tansite_sell = self.get_total_transites_amount()
        total_receivees = self.total_receivees()

        profit = ( #decimal.Decimal(str(total_tansite_sell)) + 
                decimal.Decimal(str(total_receivees))) - (
                # decimal.Decimal(str(total_booking))  + 
                decimal.Decimal(str(total_expense)) + 
                # decimal.Decimal(str(total_hamali)) +  
                decimal.Decimal(str(total_manifestations)))
        
        return profit if profit else 0
    

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
    
    def getVessel(self, *args, **kwargs):
        return self.vessel.launch.number

class VesselExpenses(models.Model):
    vessel  = models.ForeignKey(Vessel,on_delete=models.CASCADE)
    amount  = models.DecimalField(max_digits=8, decimal_places=2)
    date    = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file    = models.FileField(upload_to=generate_file_path, null=True,blank=True)
    note    = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.vessel.launch.number

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
    
    def getVesselNumber(self, *args, **kwargs):
        return self.vessel.launch.number
    def getVessel(self, *args, **kwargs):
        return self.vessel.launch.number

class VesselExit(models.Model):
    vessel = models.ForeignKey(Vessel,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=generate_file_path, null=True,blank=True)
    note = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.vessel.launch.number

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
    def getVessel(self, *args, **kwargs):
        return self.vessel.launch.number
    
class VesselManifest(models.Model):
    vessel = models.ForeignKey(Vessel,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=generate_file_path, null=True,blank=True)
    note = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.vessel.launch.number

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
    def getVessel(self, *args, **kwargs):
        return self.vessel.launch.number
class VesselAttestation(models.Model):
    vessel = models.ForeignKey(Vessel,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=generate_file_path, null=True,blank=True)
    note = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.vessel.launch.number

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
    
    def getVessel(self, *args, **kwargs):
        return self.vessel.launch.number
    
class VesselAmend(models.Model):
    vessel = models.ForeignKey(Vessel,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=generate_file_path, null=True,blank=True)
    note = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.vessel.launch.number

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
    def getVessel(self, *args, **kwargs):
        return self.vessel.launch.number
    
class VesselTrueCopy(models.Model):
    vessel = models.ForeignKey(Vessel,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=generate_file_path, null=True,blank=True)
    note = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.vessel.launch.number

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
    def getVessel(self, *args, **kwargs):
        return self.vessel.launch.number
    

class VesselHamali(models.Model):
    vessel = models.ForeignKey(Vessel,on_delete=models.CASCADE)
    hamal = models.ForeignKey(User,on_delete=models.CASCADE)     # hamal 
    hamal_loaded = models.DecimalField(max_digits=8, decimal_places=2) # how many ctn haml loaded
    container = models.DecimalField(max_digits=8, decimal_places=2)   # total loaded ctns 
    ctn_fees = models.DecimalField(default=265,max_digits=8, decimal_places=2)  # the per ctn fees 
    date = models.DateTimeField(auto_created=True, auto_now_add=True) 
    done_by = models.ForeignKey(User,related_name='done_by', on_delete=models.CASCADE)
    file = models.FileField(upload_to=generate_file_path, null=True,blank=True)
    note = models.TextField(null=True,blank=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # the per ctn fees 
    is_paid = models.BooleanField(default=False)  # the per ctn fees 

    def __str__(self):
        return self.vessel.launch.number

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
    
    def getVesselNumber(self, *args, **kwargs):
        return self.vessel.launch.number
    
    def getHamalName(self, *args, **kwargs):
        return self.hamal.username
    
    def getHamalFees(self, *args, **kwargs):
        return int(self.hamal_loaded * self.ctn_fees)

class VesselAccount(models.Model):
    vessel  = models.ForeignKey(Vessel,on_delete=models.CASCADE)
    amount  = models.DecimalField(max_digits=8, decimal_places=2)
    date    = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file    = models.FileField(upload_to=generate_file_path, null=True,blank=True)
    note    = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.vessel.launch.number

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
    
    def getVesselNumber(self, *args, **kwargs):
        return self.vessel.launch.number
    
class UserExpenseAccount(models.Model):
    amount  = models.DecimalField(max_digits=8, decimal_places=2)
    date    = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file    = models.FileField(upload_to=user_file_path, null=True,blank=True)
    note    = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.amount)

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
    
class UserReceiveAccount(models.Model):
    amount  = models.DecimalField(max_digits=8, decimal_places=2)
    date    = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file    = models.FileField(upload_to=user_file_path, null=True,blank=True)
    note    = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.amount)

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username

class VesselDiscount(models.Model):
    vessel  = models.ForeignKey(Vessel,on_delete=models.CASCADE)
    amount  = models.DecimalField(max_digits=8, decimal_places=2)
    date    = models.DateTimeField(auto_created=True, auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file    = models.FileField(upload_to=generate_file_path, null=True, blank=True)
    note    = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.amount)

    def getDoneByName(self, *args, **kwargs):
        return self.done_by.username
    
    def getVessel(self, *args, **kwargs):
        return self.vessel.launch.number