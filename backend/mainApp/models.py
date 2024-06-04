from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class SilantClient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=128)

    def __str__(self):
        return self.full_name


class SilantServiceCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=128)
    # company_description = models.TextField()

    def __str__(self):
        return self.service_name

class Vehicle(models.Model):
    vehicle_model = models.ForeignKey("GuideVehicle", on_delete=models.CASCADE)
    vehicle_SN = models.CharField(max_length=64, unique=True)
    engine_model = models.ForeignKey("GuideEngine", on_delete=models.CASCADE)
    engine_SN = models.CharField(max_length = 64)
    transmission_model = models.ForeignKey("GuideTransmission", on_delete=models.CASCADE)
    transmission_SN = models.CharField(max_length = 64)
    driving_axle_model = models.ForeignKey("GuideDrivingAxle", on_delete=models.CASCADE)
    driving_axle_SN = models.CharField(max_length = 64)
    control_axle_model = models.ForeignKey("GuideControlAxle", on_delete=models.CASCADE)
    control_axle_SN = models.CharField(max_length = 64)
    invoice = models.CharField(max_length = 64)
    shipment_date = models.DateField()
    final_user = models.CharField(max_length = 64)
    address = models.CharField(max_length = 128)
    vehicle_configuration = models.CharField(max_length = 256)
    client = models.ForeignKey(SilantClient, on_delete=models.CASCADE)
    service_company = models.ForeignKey(SilantServiceCompany, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.vehicle_model) + " - " + str(self.vehicle_SN)

    def get_absolute_url(self):
        return reverse('vehicle_list')

class TechnicalMaintenance(models.Model):
    TM_type = models.ForeignKey("GuideTM", on_delete=models.CASCADE)
    TM_date = models.DateField()
    TM_operating_hours = models.FloatField(max_length = 64)
    TM_invoice = models.CharField(max_length = 64)
    TM_invoice_date = models.DateField()
    TM_responsible_company = models.ForeignKey("GuideTMCompany", on_delete=models.CASCADE)
    TM_vehicle_SN = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    TM_service_company = models.ForeignKey(SilantServiceCompany, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.TM_vehicle_SN) + " - " + str(self.TM_type)

    def get_absolute_url(self):
        return reverse('tm_list')


class ClientClaim(models.Model):
    CC_breakdown_date = models.DateField()
    CC_operating_hours = models.FloatField(max_length = 64)
    CC_breakdown_unit = models.ForeignKey("GuideBreakdownUnit", on_delete=models.CASCADE)
    CC_breakdown_description = models.TextField()
    CC_repair_type = models.ForeignKey("GuideRepairType", on_delete=models.CASCADE)
    CC_spares_list = models.TextField()
    CC_recovery_date = models.DateField(null=True, blank=True)
    CC_vehicle_downtime = models.IntegerField(null=True, blank=True)
    CC_vehicle_SN = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    CC_service_company = models.ForeignKey(SilantServiceCompany, on_delete=models.CASCADE)

    def __str__(self):
        print(str(self.CC_vehicle_SN))
        return str(self.CC_vehicle_SN) + " - " + str(self.CC_breakdown_unit) + " / " + str(self.CC_repair_type)

    def get_absolute_url(self):
        return reverse('claim_list')



class GuideVehicle(models.Model):
    name = models.CharField(max_length = 64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gv')

class GuideEngine(models.Model):
    name = models.CharField(max_length = 64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ge')

class GuideTransmission(models.Model):
    name = models.CharField(max_length = 64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gt')

class GuideDrivingAxle(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gda')

class GuideControlAxle(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gca')

class GuideTM(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gtm')

class GuideTMCompany(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gtmc')

class GuideBreakdownUnit(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gbu')

class GuideRepairType(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('grt')
