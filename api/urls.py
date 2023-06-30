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
# router.register(r'vessel/hamal', views.VesselHamaliViewSet)

# router.register(r'hamali-list', views.HamaliListViewSet)
# router.register(r'hamali-details', views.UserHamaliViewSet)

router.register(r'accounts', views.AccountViewSet)
router.register(r'vessel/account', views.VesselAccountViewSet)

router.register(r'expenses', views.ExpenseViewSet)
router.register(r'vessel/expense', views.VesselExpensesViewSet)

router.register(r'launch-search', views.LaunchSearchViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-details/', views.getUserDetails, name='user-details'),
    path('hamali-details/', views.UserHamaliViewSet.as_view({'get':'list'}), name='hamali-user'),
    path('hamali-list/', views.HamaliListViewSet.as_view({'get':'list'}), name='hmali-list'),
    # path('hamals/', views.HamaliViewSet.as_view({'get':'list'}), name='hamali-all'),
    path('vessel/hamal/', views.VesselHamaliViewSet.as_view({'get':'list'}), name='vessel-hamali'),

]
