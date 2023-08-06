from django.contrib import admin
from api   import models

admin.site.register(models.Usr)
admin.site.register(models.Launch)
admin.site.register(models.Vessel)
admin.site.register(models.VesselParking)
admin.site.register(models.VesselExit)
admin.site.register(models.VesselAmend)
admin.site.register(models.VesselAttestation)
admin.site.register(models.VesselManifest)
admin.site.register(models.VesselTrueCopy)
admin.site.register(models.VesselExpenses)
admin.site.register(models.VesselAccount)
admin.site.register(models.VesselHamali)
admin.site.register(models.UserReceiveAccount)
admin.site.register(models.UserExpenseAccount)
