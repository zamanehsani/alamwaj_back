# Routers provide an easy way of automatically determining the URL conf.
from django.urls import path, include

from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'usr', views.USRViewSet)
router.register(r'launches', views.LaunchViewSet)
router.register(r'vessels', views.VesselViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
