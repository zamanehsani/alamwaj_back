from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from datetime import datetime
import sys
from api import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

# Function to send the VesselExpenses objects as an email
def daily_report_email(vesselExpense, vesselAccount, userExpense,userReceive,
                        vesselExit, vesselParking, vesselTrueCopy, vesselAttest, 
                        vesselManifest,vesselAmend, hamali, booking, transiteSell):
    
    subject = 'Daily Report'
    message = "Hey there, \nHere is the list of today's report."
    from_email = settings.EMAIL_HOST_USER
    users_to_notify = User.objects.filter(usr__daily_report=True)
    
    # get emails of users with checked on daily report
    to_emails = [user.email for user in users_to_notify]

    counter =1
    # Create a string representation of the VesselExpenses objects
    if userReceive.count() > 0:
        message += '\n...........................................\n'
        message += 'Users Recevings:\n'
        for index, exp in enumerate(userReceive):
            message += f'{index+1}. {exp.done_by} received {exp.amount} on his personal account.\n'

    if userExpense.count() > 0:
        message += '\n...........................................\n'
        message += 'Users Expenses:\n'
        for index, exp in enumerate(userExpense):
            message += f'{index+1}. {exp.done_by} paid {exp.amount} as of personal expense.\n'
    
    if vesselExpense.count() > 0:
        message += '\n...........................................\n'
        message += 'Vessel Expenses:\n'
        for index, exp in enumerate(vesselExpense):
            message += f'{index+1}. {exp.done_by} paid {exp.amount} for expenses of {exp.getVessel()}.\n'

    if booking.count() > 0:
        message += '\n...........................................\n'
        message += 'Booking:\n'
        for index, book in enumerate(booking):
            message += f'{index+1}. {book.done_by} paid {book.amount} for booking of {book.type} for {book.getVessel()}.\n'

    if transiteSell.count() > 0:
        message += '\n...........................................\n'
        message += 'Transite Sell:\n'
        for index, transite in enumerate(transiteSell):
            message += f'{index+1}. {transite.received_by} received {transite.amount_paid} for selling {book.type} of {book.company}.\n'
        
    if vesselAccount.count()> 0:
        message += '\n...........................................\n'
        message += 'Vessel Account:\n'
        for index, account in enumerate(vesselAccount):
            message += f'{index+1}. {account.done_by} received {account.amount} from account of {account.getVesselNumber()}.\n'

    if hamali.count()>0:
        message += '\n...........................................\n'
        message += 'Loading:\n'
        for index, loading in enumerate(hamali):
            message += f'{index+1}. {loading.done_by} paid {loading.getHamalFees()} for {loading.hamal_loaded} to {loading.getHamalName()} for loading of {loading.getVesselNumber()}.\n'

    if vesselExit.count() > 0:
        message += '\n...........................................\n'
        message += 'Vessel Exit:\n'
        for exit in enumerate(vesselExit):
            message += f'{counter}. {exit.done_by} paid {exit.amount} for Exit of {exit.getVessel()}.\n'
            counter +=1

    if vesselAttest.count() > 0:
        message += '\n...........................................\n'
        message += 'Vessel Attestation:\n'
        for attest in enumerate(vesselAttest):
            message += f'{counter}. {attest.done_by} paid {attest.amount} for Attestation of {attest.getVessel()}.\n'
            counter +=1

    if vesselTrueCopy.count() > 0: 
        message += '\n...........................................\n'
        message += 'Vessel True Copy:\n'
        for true in enumerate(vesselTrueCopy):
            message += f'{counter}. {true.done_by} paid {true.amount} for True Copy of {true.getVessel()}.\n'
            counter +=1

    if vesselManifest.count() >0:
        message += '\n...........................................\n'
        message += 'Vessel Manifest:\n'
        for manifest in enumerate(vesselManifest):
            message += f'{counter}. {manifest.done_by} paid {manifest.amount} for Manifest of {manifest.getVessel()}.\n'
            counter +=1

    if vesselAmend.count() > 0:
        message += '\n...........................................\n'
        message += 'Vessel Amendment:\n'
        for amend in enumerate(vesselAmend):
            amend_object = amend[1]  # Unpack the second element of the tuple (the Amend object)
            message += f'{counter}. {amend_object.getDoneByName()} paid {amend_object.amount} for Amendment of {amend_object.getVessel()}.\n'
            counter += 1

    if vesselParking.count() > 0:
        message += '\n...........................................\n'
        message += 'Vessel Parking:\n'
        for park in enumerate(vesselParking):
            message += f'{counter}. {park.done_by} paid {park.amount} for {park.days} of Parking of {park.getVessel()}.\n'
            counter +=1
        
    send_mail(subject,message,from_email,to_emails,fail_silently=False,)


# This is the function you want to schedule
def daily_breif():
    # Get the current date in the timezone of your project
    current_date = timezone.now().date()

    # Calculate the start and end datetime for today
    start_datetime = datetime.combine(current_date, datetime.min.time())
    end_datetime = datetime.combine(current_date, datetime.max.time())
    vesselExpense = models.VesselExpenses.objects.filter(date__range=(start_datetime, end_datetime))
    vesselAccount = models.VesselAccount.objects.filter(date__range=(start_datetime, end_datetime))
    vesselExit = models.VesselExit.objects.filter(date__range=(start_datetime, end_datetime))
    vesselParking = models.VesselParking.objects.filter(date__range=(start_datetime, end_datetime))
    vesselTrueCopy = models.VesselTrueCopy.objects.filter(date__range=(start_datetime, end_datetime))
    vesselAttest = models.VesselAttestation.objects.filter(date__range=(start_datetime, end_datetime))
    vesselManifest = models.VesselManifest.objects.filter(date__range=(start_datetime, end_datetime))
    vesselAmend = models.VesselAmend.objects.filter(date__range=(start_datetime, end_datetime))
    hamali = models.VesselHamali.objects.filter(date__range=(start_datetime, end_datetime))
    booking = models.VesselBooking.objects.filter(date__range=(start_datetime, end_datetime))
    transiteSell = models.VesselBooking.objects.filter(pay_date__range=(start_datetime, end_datetime))

    userReceive = models.UserReceiveAccount.objects.filter(date__range=(start_datetime, end_datetime))
    userExpense = models.UserExpenseAccount.objects.filter(date__range=(start_datetime, end_datetime))

    daily_report_email(vesselExpense, vesselAccount, 
                       userExpense,userReceive,vesselExit, vesselParking, 
                        vesselTrueCopy, vesselAttest, vesselManifest,vesselAmend, hamali, 
                        booking, transiteSell)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # Remove all missed jobs before adding new ones
    scheduler.remove_all_jobs()
    # run this job every 24 hours
    scheduler.add_job(daily_breif, 'interval',hours=1, name='daily_report', jobstore='default')
    # Schedule the job using the "cron" trigger with hours and minutes set to 0

    # from apscheduler.triggers.cron import CronTrigger
    # scheduler.add_job(daily_breif, trigger=CronTrigger(hour=0, minute=0),name='daily_report', jobstore='default')

    register_events(scheduler)
    scheduler.start()
    print("daily report Scheduler started...", file=sys.stdout)