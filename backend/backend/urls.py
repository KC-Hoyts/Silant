"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'clients', views.SilantClientViewset)
router.register(r'services', views.SilantServiceCompanyViewset)

router.register(r'vehicles', views.VehicleViewset)
router.register(r'tm', views.TechnicalMaintenanceViewset)
router.register(r'claims', views.ClientClaimViewset)

router.register(r'guide_vehicle', views.GuideVehicleViewset)
router.register(r'guide_engine', views.GuideEngineViewset)
router.register(r'guide_transmission', views.GuideTransmissionViewset)
router.register(r'guide_driving_axle', views.GuideDrivingAxleViewset)
router.register(r'guide_control_axle', views.GuideControlAxleViewset)
router.register(r'guide_tm', views.GuideTMViewset)
router.register(r'guide_tm_company', views.GuideTMCompanyViewset)
router.register(r'guide_breakdown_unit', views.GuideBreakdownUnitViewset)
router.register(r'guide_repair_type', views.GuideRepairTypeViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('mainApp.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
