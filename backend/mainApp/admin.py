from django.contrib import admin
from .models import *


admin.site.register(SilantClient)
admin.site.register(SilantServiceCompany)
admin.site.register(Vehicle)
admin.site.register(TechnicalMaintenance)
admin.site.register(ClientClaim)


admin.site.register(GuideVehicle)
admin.site.register(GuideEngine)
admin.site.register(GuideTransmission)
admin.site.register(GuideDrivingAxle)
admin.site.register(GuideControlAxle)
admin.site.register(GuideTM)
admin.site.register(GuideTMCompany)
admin.site.register(GuideBreakdownUnit)
admin.site.register(GuideRepairType)
