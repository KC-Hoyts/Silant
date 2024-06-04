import django_filters
from django_filters import FilterSet, CharFilter, ChoiceFilter

from .models import *


class UnauuthorizedVehicleFilter(FilterSet):
    vehicle_SN = CharFilter(field_name='vehicle_SN', max_length=64, lookup_expr='icontains')

    def __init__(self, *args, **kwargs):
        super(UnauuthorizedVehicleFilter, self).__init__(*args, **kwargs)
        self.filters['vehicle_SN'].label = "Введите серийный номер техники"

class VehicleFilter(FilterSet):

    class Meta:
        model = Vehicle
        fields = [
            "vehicle_model",
            "engine_model",
            "transmission_model",
            "control_axle_model",
            "driving_axle_model"
        ]


    def __init__(self, *args, **kwargs):
        super(VehicleFilter, self).__init__(*args, **kwargs)
        self.filters['vehicle_model'].label = "Модель техники"
        self.filters['engine_model'].label = "Модель двигателя"
        self.filters['transmission_model'].label = "Модель трансмиссии"
        self.filters['control_axle_model'].label = "Модель управляемого моста"
        self.filters['driving_axle_model'].label = "Модель ведущего моста"


class TechnicalMaintenanceFilter(FilterSet):

    class Meta:
        model = TechnicalMaintenance
        fields = [
            "TM_type",
            "TM_vehicle_SN",
            "TM_service_company",
        ]


    def __init__(self, *args, **kwargs):
        super(TechnicalMaintenanceFilter, self).__init__(*args, **kwargs)
        self.filters['TM_type'].label = "Тип ТО"
        self.filters['TM_vehicle_SN'].label = "Модель и серийный номер техники"
        self.filters['TM_service_company'].label = "Сервисная компания"


class ClientClaimFilter(FilterSet):

    class Meta:
        model = ClientClaim
        fields = [
            "CC_breakdown_unit",
            "CC_repair_type",
            "CC_service_company",
        ]


    def __init__(self, *args, **kwargs):
        super(ClientClaimFilter, self).__init__(*args, **kwargs)
        self.filters['CC_breakdown_unit'].label = "Узел поломки"
        self.filters['CC_repair_type'].label = "Вид ремонта"
        self.filters['CC_service_company'].label = "Сервисная компания"
