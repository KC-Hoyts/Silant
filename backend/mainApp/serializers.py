from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



class SilantClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = SilantClient  # модель из файла models.py
        fields = ['id', "user", "full_name"]


class SilantServiceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = SilantServiceCompany  # модель из файла models.py
        fields = ['id', "user", "service_name"]


class VehicleSerializer(serializers.ModelSerializer):
   class Meta:
       model = Vehicle #модель из файла models.py
       fields = ['id',
               "vehicle_model",
               "vehicle_SN",
               "engine_model",
               "engine_SN",
               "transmission_model",
               "transmission_SN",
               "driving_axle_model",
               "driving_axle_SN",
               "control_axle_model",
               "control_axle_SN",
               "invoice",
               "shipment_date",
               "final_user",
               "address",
               "vehicle_configuration",
               "client",
               "service_company"]

class TechnicalMaintenanceSerializer(serializers.ModelSerializer):
   class Meta:
       model = TechnicalMaintenance #модель из файла models.py
       fields = ['id',
                 "TM_type",
                   "TM_date",
                   "TM_operating_hours",
                   "TM_invoice",
                   "TM_invoice_date",
                   "TM_responsible_company",
                   "TM_vehicle_SN",
                   "TM_service_company"]

class ClientClaimSerializer(serializers.ModelSerializer):
   class Meta:
       model = ClientClaim #модель из файла models.py
       fields = ['id',
                 "CC_breakdown_date",
                 "CC_operating_hours",
                 "CC_breakdown_unit",
                 "CC_breakdown_description",
                 "CC_repair_type",
                 "CC_spares_list",
                 "CC_recovery_date",
                 "CC_vehicle_downtime",
                 "CC_vehicle_SN",
                 "CC_service_company"]


class GuideVehicleSerializer(serializers.ModelSerializer):
   class Meta:
       model =  GuideVehicle#модель из файла models.py
       fields = ['id', "name", "description"]

class GuideEngineSerializer(serializers.ModelSerializer):
   class Meta:
       model =  GuideEngine#модель из файла models.py
       fields = ['id', "name", "description"]

class GuideTransmissionSerializer(serializers.ModelSerializer):

   class Meta:
       model =  GuideTransmission# модель из файла models.py
       fields = ['id', "name", "description"]


class GuideDrivingAxleSerializer(serializers.ModelSerializer):
    class Meta:
        model =  GuideDrivingAxle# модель из файла models.py
        fields = ['id', "name", "description"]

class GuideControlAxleSerializer(serializers.ModelSerializer):
    class Meta:
        model =  GuideControlAxle# модель из файла models.py
        fields = ['id', "name", "description"]


class GuideTMSerializer(serializers.ModelSerializer):
    class Meta:
        model =  GuideTM# модель из файла models.py
        fields = ['id', "name", "description"]


class GuideTMCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideTMCompany # модель из файла models.py
        fields = ['id', "name", "description"]


class GuideBreakdownUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideBreakdownUnit # модель из файла models.py
        fields = ['id', "name", "description"]


class GuideRepairTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideRepairType # модель из файла models.py
        fields = ['id', "name", "description"]