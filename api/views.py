
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from api import serializers, models
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from api.exit_lauch_report import generate_pdf
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.generic import ListView
from django.conf import settings


class LaunchSearchViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LaunchSerializer
    queryset = models.Launch.objects.all()

    def get_queryset(self):
        queryset = models.Launch.objects.all()
        vessel_id = self.request.query_params.get('number')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(number__contains=vessel_id)
            return queryset
        return []
    
@csrf_exempt
@permission_classes([IsAuthenticated])
def getUserDetails(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        # Retrieve user from User model using the username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Serialize user object
        serializer = serializers.UserDetailsSerializer(user)

        # Return serialized object as JSON response
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class USRViewSet(viewsets.ModelViewSet):
    queryset = models.Usr.objects.all()
    serializer_class = serializers.USRSerializer

 
class LaunchViewSet(viewsets.ModelViewSet):
    queryset = models.Launch.objects.all().order_by('number')
    serializer_class = serializers.LaunchSerializer

class VesselViewSet(viewsets.ModelViewSet):
    queryset = models.Vessel.objects.filter(~Q(status = 'exit')).order_by('launch__number')
    serializer_class = serializers.VesselSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Check if the launch has no warning and is clear to register.
        if not self.is_data_valid(serializer.validated_data):
            # Return an error response
            return Response({"LaunchError": "This launch has warning!!!"}, status=status.HTTP_400_BAD_REQUEST )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def is_data_valid(self, data):
        try:
            obj = models.Launch.objects.get(number=data.get('launch', None))
        except models.Launch.DoesNotExist:
            # Handle the case when the Launch object with the specified number does not exist.
            return False
        
        if obj.warning:
            return False
        
        return True

@csrf_exempt
def Exitvessel(request):
    if request.method == 'POST':
        vessel = request.POST.get("vessel")
        note = request.POST.get("exit_note")
        try:
            obj = models.Vessel.objects.filter(pk = vessel).filter(~Q(status = 'exit')).first()
            obj.status = 'exit'
            obj.exit_note = note
           
             # Generate the PDF content
            pdf_filename = f'vessel_report_{obj.pk}.pdf'
            pdf_content = generate_pdf(obj)

            obj.exitReport.save(pdf_filename, ContentFile(pdf_content))

            # Send an email with the attached PDF  
            subject = 'Vessel Exit Report'
            message = f"Vessel {obj} has been exited. \nPlease see attached file the report."
            from_email = settings.EMAIL_HOST_USER
            users_emails = User.objects.filter(usr__vessel_exit_report=True).values_list('email', flat=True)
            recipient_list = list(users_emails)
            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach(pdf_filename, pdf_content, "application/pdf")
            email.send()

            serializer = serializers.VesselSerializer(obj,context={'request': request})
            return JsonResponse(serializer.data)
        except:
            return JsonResponse({'err':'something went wrong.'}, status=400)
        
    return JsonResponse({'error': 'something went wrong. launch did not exit...'})
    
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
    
class ExitViewSet(viewsets.ModelViewSet):
    queryset = models.VesselExit.objects.all()
    serializer_class = serializers.VesselExitSerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VesselExitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselExitSerializer
    queryset = models.VesselExit.objects.all()

    def get_queryset(self):
        queryset = models.VesselExit.objects.all()
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    
class TrueCopyViewSet(viewsets.ModelViewSet):
    queryset = models.VesselTrueCopy.objects.all()
    serializer_class = serializers.VesselTrueCopySerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VesselTrueCopyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselTrueCopySerializer
    queryset = models.VesselExit.objects.all()

    def get_queryset(self):
        queryset = models.VesselTrueCopy.objects.all()
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    
class ManifestViewSet(viewsets.ModelViewSet):
    queryset = models.VesselManifest.objects.all()
    serializer_class = serializers.VesselManifestSerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VesselManifestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselManifestSerializer
    queryset = models.VesselManifest.objects.all()

    def get_queryset(self):
        queryset = models.VesselManifest.objects.all()
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    
class AttestationViewSet(viewsets.ModelViewSet):
    queryset = models.VesselAttestation.objects.all()
    serializer_class = serializers.VesselAttestationSerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VesselAttestationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselAttestationSerializer
    queryset = models.VesselAttestation.objects.all()

    def get_queryset(self):
        queryset = models.VesselAttestation.objects.all()
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    
class AmendViewSet(viewsets.ModelViewSet):
    queryset = models.VesselAmend.objects.all()
    serializer_class = serializers.VesselAmendSerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VesselAmendViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselAmendSerializer
    queryset = models.VesselAmend.objects.all()

    def get_queryset(self):
        queryset = models.VesselAmend.objects.all()
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    
class HamaliListViewSet(viewsets.ModelViewSet):
    queryset = models.Usr.objects.all()
    serializer_class = serializers.USRSerializer
    def get_queryset(self):
        queryset = models.Usr.objects.all()
        hamal = self.request.query_params.get('type')  # Get the vessel ID from query parameters
        if hamal:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(type=hamal)
            return queryset
        # if nothing is giving in the url params; return all the usr lists
        return queryset
   
# general hamal list
class HamaliViewSet(viewsets.ModelViewSet):
    queryset = models.VesselHamali.objects.all()
    serializer_class = serializers.VesselHamaliSerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# gets the hamali based on vessels
class VesselHamaliViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselHamaliSerializer
    queryset = models.VesselHamali.objects.all()

    def get_queryset(self):
        queryset = models.VesselHamali.objects.all()
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    
    # gets hamal based on user pk

class UserHamaliViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselHamaliSerializer
    queryset = models.VesselHamali.objects.all()

    def get_queryset(self):
        queryset = models.VesselHamali.objects.all()
        hamal = self.request.query_params.get('hamal')  # Get the vessel ID from query parameters
        if hamal:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(hamal=hamal, is_paid = False)
            return queryset
        return []
    
class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.VesselAccount.objects.all()
    serializer_class = serializers.VesselAccountSerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class VesselAccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselAccountSerializer
    queryset = models.VesselAccount.objects.all()

    def get_queryset(self):
        queryset = models.VesselAccount.objects.all()
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    

    # this is vessel expenses 

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = models.VesselExpenses.objects.all()
    serializer_class = serializers.VesselExpenseSerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class VesselExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselExpenseSerializer
    queryset = models.VesselExpenses.objects.all()

    def get_queryset(self):
        queryset = models.VesselExpenses.objects.all()
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    
class ParkingMonthView(viewsets.ModelViewSet):
    serializer_class = serializers.VesselParkingSerializer
    queryset = models.VesselParking.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))
            
        return queryset
    
class ManifestMonthView(viewsets.ModelViewSet):
    serializer_class = serializers.VesselManifestSerializer
    queryset = models.VesselManifest.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class ExitMonthView(viewsets.ModelViewSet):
    serializer_class = serializers.VesselExitSerializer
    queryset = models.VesselExit.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class AttestationMonthView(viewsets.ModelViewSet):
    serializer_class = serializers.VesselAttestationSerializer
    queryset = models.VesselAttestation.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class AmendMonthView(viewsets.ModelViewSet):
    serializer_class = serializers.VesselAmendSerializer
    queryset = models.VesselAmend.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class TrueCopyMonthView(viewsets.ModelViewSet):
    serializer_class = serializers.VesselTrueCopySerializer
    queryset = models.VesselTrueCopy.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class ManifestMonthView(viewsets.ModelViewSet):
    serializer_class = serializers.VesselManifestSerializer
    queryset = models.VesselManifest.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class ExpensesMonthView(viewsets.ModelViewSet):
    serializer_class = serializers.VesselExpenseSerializer
    queryset = models.VesselExpenses.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class VesselAccountMonth(viewsets.ModelViewSet):
    serializer_class = serializers.VesselAccountSerializer
    queryset = models.VesselAccount.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class UserExpenseViewSet(viewsets.ModelViewSet):
    queryset = models.UserExpenseAccount.objects.all()
    serializer_class = serializers.UserExpenseSerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
     
class UserReceiveViewSet(viewsets.ModelViewSet):
    queryset = models.UserReceiveAccount.objects.all()
    serializer_class = serializers.UserReceiveSerializer
    parser_classes = [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class UserExpenseMonth(viewsets.ModelViewSet):
    serializer_class = serializers.UserExpenseSerializer
    queryset = models.UserExpenseAccount.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class LoadingMonth(viewsets.ModelViewSet):
    serializer_class = serializers.VesselHamaliSerializer
    queryset = models.VesselHamali.objects.filter(is_paid = True)

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class LoadingHamalMonth(viewsets.ModelViewSet):
    serializer_class = serializers.VesselHamaliSerializer
    queryset = models.VesselHamali.objects.filter(is_paid = True)

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(hamal=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class BookingMonth(viewsets.ModelViewSet):
    serializer_class = serializers.VesselBookingSerializer
    queryset = models.VesselBooking.objects.filter(amount__gt=0)

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class TransiteSellMonth(viewsets.ModelViewSet):
    serializer_class = serializers.VesselBookingSerializer
    queryset = models.VesselBooking.objects.filter(paid = True)

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(received_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class UserReceiveMonth(viewsets.ModelViewSet):
    serializer_class = serializers.UserReceiveSerializer
    queryset = models.UserReceiveAccount.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('usr'):
            queryset = queryset.filter(done_by=self.request.query_params.get('usr'))
        if self.request.query_params.get('yr'):
            queryset = queryset.filter(date__year = self.request.query_params.get('yr'))
        if self.request.query_params.get('mth') :
            queryset = queryset.filter(date__month = self.request.query_params.get('mth'))

        return queryset
    
class LaunchVesselList(viewsets.ModelViewSet):
    serializer_class = serializers.VesselSerializer
    queryset = models.Vessel.objects.all()
    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('launch'):
            queryset = queryset.filter(launch__pk=self.request.query_params.get('launch'))
            return queryset
        return []

class VesselDiscountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselDiscountSerializer
    queryset = models.VesselDiscount.objects.all()


class VesselDiscViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselDiscountSerializer
    queryset = models.VesselDiscount.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselBookingSerializer
    queryset = models.VesselBooking.objects.all()



from rest_framework.pagination import PageNumberPagination
class TransitePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TransitesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselBookingSerializer
    queryset = models.VesselBooking.objects.filter(paid=False).filter(final_stamp = True)
    pagination_class = TransitePagination


class VesselBookingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VesselBookingSerializer
    queryset = models.VesselBooking.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        vessel_id = self.request.query_params.get('vessel_id')  # Get the vessel ID from query parameters
        if vessel_id:
            # Filter the queryset based on the vessel ID
            queryset = queryset.filter(vessel=vessel_id)
            return queryset
        return []
    
class HSCodeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HSCodeSerializer
    queryset = models.HS_codes.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(Q(description__icontains=name))
            return queryset
        return models.HS_codes.objects.all()
    
class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = models.Company.objects.all()

