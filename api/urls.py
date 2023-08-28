# Routers provide an easy way of automatically determining the URL conf.
from django.urls import path, include

from rest_framework import routers
from api import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
# router.register(r'get-user', views.UserDetails)
router.register(r'usr', views.USRViewSet)
router.register(r'launches', views.LaunchViewSet)
router.register(r'vessels', views.VesselViewSet)
router.register(r'exits', views.ExitViewSet)
router.register(r'vessel/exit', views.VesselExitViewSet)

router.register(r'parkings', views.ParkingViewSet)
router.register(r'vessel/parking', views.VesselParkingViewSet)

router.register(r'manifests', views.ManifestViewSet)
router.register(r'vessel/manifest', views.VesselManifestViewSet)

router.register(r'attestations', views.AttestationViewSet)
router.register(r'vessel/attestation', views.VesselAttestationViewSet)

router.register(r'true-copys', views.TrueCopyViewSet)
router.register(r'vessel/true-copy', views.VesselTrueCopyViewSet)

router.register(r'amends', views.AmendViewSet)
router.register(r'vessel/amend', views.VesselAmendViewSet)

router.register(r'hamals', views.HamaliViewSet)
router.register(r'vessel-discount', views.VesselDiscountViewSet)
router.register(r'vessel/discount', views.VesselDiscViewSet)


# transites and booking of tax, local, transite
router.register(r'booking', views.BookingViewSet)
router.register(r'transites', views.TransitesViewSet)
router.register(r'vessel/booking', views.VesselBookingViewSet)

router.register(r'accounts', views.AccountViewSet)
router.register(r'vessel/account', views.VesselAccountViewSet)

router.register(r'expenses', views.ExpenseViewSet)
router.register(r'vessel/expense', views.VesselExpensesViewSet)

router.register(r'launch-search', views.LaunchSearchViewSet)
router.register(r'user-expense', views.UserExpenseViewSet)
router.register(r'user-receive', views.UserReceiveViewSet)

router.register(r'company', views.CompanyViewSet)
router.register(r'hs-code', views.HSCodeViewSet)
# router.register(r'parking-month-view', views.ParkingMonthView)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-details/', views.getUserDetails, name='user-details'),
    path('hamali-details/', views.UserHamaliViewSet.as_view({'get':'list'}), name='hamali-user'),
    path('hamali-list/', views.HamaliListViewSet.as_view({'get':'list'}), name='hmali-list'),
    path('vessel/hamal/', views.VesselHamaliViewSet.as_view({'get':'list'}), name='vessel-hamali'),

    path('parking-month/', views.ParkingMonthView.as_view({'get':'list'}), name='parking_month'),
    path('exit-month/', views.ExitMonthView.as_view({'get':'list'}), name='exit_month'),
    path('attest-month/', views.AttestationMonthView.as_view({'get':'list'}), name='attest_month'),
    path('true-copy-month/', views.TrueCopyMonthView.as_view({'get':'list'}), name='true_copy_month'),
    path('manifest-month/', views.ManifestMonthView.as_view({'get':'list'}), name='manifest_month'),
    path('amend-month/', views.AmendMonthView.as_view({'get':'list'}), name='amend_month'),
    path('expense-month/', views.ExpensesMonthView.as_view({'get':'list'}), name='expense_month'),
    path('vessel-account-month/', views.VesselAccountMonth.as_view({'get':'list'}), name='vessel_account_month'),
    path('user-expense-month/', views.UserExpenseMonth.as_view({'get':'list'}), name='vessel_expense_month'),
    path('user-receive-month/', views.UserReceiveMonth.as_view({'get':'list'}), name='user_receive_month'),
    path('loading-month/', views.LoadingMonth.as_view({'get':'list'}), name='loading_month'),
    path('loading-hamal-month/', views.LoadingHamalMonth.as_view({'get':'list'}), name='loading_hamal_month'),
    path('booking-month/', views.BookingMonth.as_view({'get':'list'}), name='booking_month'),
    path('transite-sell-month/', views.TransiteSellMonth.as_view({'get':'list'}), name='transite_sell_month'),
    path('launch-vessel-list/', views.LaunchVesselList.as_view({'get':'list'}), name='launch_vessel_list'),
    path('vessel-exit/', views.Exitvessel, name='exit_vessel'),
    path('balance-pending-vessels/', views.PendingBalanceVessels.as_view({'get':'list'}), name='balance_pending_vessel'),

]
