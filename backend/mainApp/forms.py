# from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from random import randint
from .models import *

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
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
            "service_company"
        ]
        labels = {
            "vehicle_model" : "Модель техники",
            "vehicle_SN" : "Серийный номер техники",
            "engine_model" : "Модель двигателя",
            "engine_SN" : "Серийный номер двигателя",
            "transmission_model" : "Модель трансмиссии",
            "transmission_SN" : "Серийный номер трансмиссии",
            "driving_axle_model" : "Модель ведущего моста",
            "driving_axle_SN" : "Серийный номер ведущего моста",
            "control_axle_model" : "Модель управляемого моста",
            "control_axle_SN" : "Серийный номер управляемого моста",
            "invoice" : "Заказ №",
            "shipment_date" : "Дата отгрузки",
            "final_user" : "Получатель (конечный пользователь)",
            "address" : "Адрес получателя:",
            "vehicle_configuration" : "Комплектация техники",
            "client" : "Клиент (Заказчик)",
            "service_company" : "Сервисная компания"
        }
        widgets = {
            'shipment_date': forms.SelectDateWidget(),
        }


class TechnicalMaintenanceForm(forms.ModelForm):
    class Meta:
        model = TechnicalMaintenance
        fields = [
            "TM_type",
            "TM_date",
            "TM_operating_hours",
            "TM_invoice",
            "TM_invoice_date",
            "TM_responsible_company",
            "TM_vehicle_SN"
        ]
        labels = {
            "TM_type" : "Тип ТО",
            "TM_date" : "Дата проведения ТО",
            "TM_operating_hours" : "Наработка, м/ч",
            "TM_invoice" : "Заказ №",
            "TM_invoice_date" : "Дата заказа",
            "TM_responsible_company" : "Компания, проводившая ТО",
            "TM_vehicle_SN" : "Серийный номер техники"
        }
        widgets = {
            'TM_date': forms.SelectDateWidget(),
            "TM_invoice_date": forms.SelectDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(TechnicalMaintenanceForm, self).__init__(*args, **kwargs)
        self.fields['TM_vehicle_SN'].queryset = self.fields['TM_vehicle_SN'].queryset.order_by('-vehicle_model')

    def clean(self):
        cleaned_data = super().clean()
        tm = cleaned_data.get("TM_type")
        vehicle_model_and_SN = cleaned_data.get('TM_vehicle_SN')
        if TechnicalMaintenance.objects.filter(TM_type=tm, TM_vehicle_SN=vehicle_model_and_SN):
            raise ValidationError({
                "TM_type": f'Запись о "{tm}" для "{vehicle_model_and_SN}" уже присутствует в базе!'
            })

        return cleaned_data

class ClaimForm(forms.ModelForm):
    class Meta:
        model = ClientClaim
        fields = [
            "CC_breakdown_date",
            "CC_operating_hours",
            "CC_breakdown_unit",
            "CC_breakdown_description",
            "CC_repair_type",
            "CC_spares_list",
            "CC_recovery_date",
            "CC_vehicle_SN",
        ]
        labels = {
            "CC_breakdown_date": "Дата поломки",
            "CC_operating_hours": "Наработка, м/ч",
            "CC_breakdown_unit": "Узел поломки",
            "CC_breakdown_description": "Описание поломки",
            "CC_repair_type": "Тип ремонта",
            "CC_spares_list": "Список запчастей",
            "CC_recovery_date": "Дата восстановления",
            "CC_vehicle_SN": "Серийный номер техники",
        }
        widgets = {
            'CC_breakdown_date': forms.SelectDateWidget(),
            "CC_recovery_date": forms.SelectDateWidget(),
        }


        def __init__(self, *args, **kwargs):
            super(ClaimForm, self).__init__(*args, **kwargs)
            self.fields['CC_vehicle_SN'].queryset = self.fields['CC_vehicle_SN'].queryset.order_by('-vehicle_model')


class GuideVehicleForm(forms.ModelForm):
    class Meta:
        model = GuideVehicle
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": "Название",
            "description": "Описание",
        }

class GuideEngineForm(forms.ModelForm):
    class Meta:
        model = GuideEngine
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": "Название",
            "description": "Описание",
        }

class GuideTransmissionForm(forms.ModelForm):
    class Meta:
        model = GuideTransmission
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": "Название",
            "description": "Описание",
        }

class GuideDrivingAxleForm(forms.ModelForm):
    class Meta:
        model = GuideDrivingAxle
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": "Название",
            "description": "Описание",
        }

class GuideControlAxleForm(forms.ModelForm):
    class Meta:
        model = GuideControlAxle
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": "Название",
            "description": "Описание",
        }

class GuideTMForm(forms.ModelForm):
    class Meta:
        model = GuideTM
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": "Название",
            "description": "Описание",
        }

class GuideTMCompanyForm(forms.ModelForm):
    class Meta:
        model = GuideTMCompany
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": "Название",
            "description": "Описание",
        }

class GuideBreakdownUnitForm(forms.ModelForm):
    class Meta:
        model = GuideBreakdownUnit
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": "Название",
            "description": "Описание",
        }


class GuideRepairTypeForm(forms.ModelForm):
    class Meta:
        model = GuideRepairType
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": "Название",
            "description": "Описание",
        }