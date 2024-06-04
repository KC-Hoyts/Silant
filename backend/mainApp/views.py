from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from rest_framework.request import Request
from rest_framework.response import Response
from .forms import *
from django.urls import reverse_lazy
import datetime
from .filters import *
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q

def logout_view(request):
    auth.logout(request)
    request.session.flush()
    request.user = "AnonymousUser"
    HttpResponseRedirect('/accounts/loggedout/')
    return redirect('vehicle_list')


class VehicleList(ListView):
    model = Vehicle #имя модели
    ordering = "-shipment_date" #сортировка по полю модели
    template_name = "flatpages/main.html" #название html шаблона
    context_object_name = 'vehicles' #контекстное название для исп.-я в шаблоне
    # paginate_by = 2  #также можно указать пагинацию (здесь на странице будет выводиться по 2 объекта)


    def get(self, request):
        current_user = str(request.user)
        if request.user.username:
            if SilantClient.objects.filter(user=User.objects.get(username=current_user)).exists():
                vehicles = Vehicle.objects.filter(client=SilantClient.objects.get(user=User.objects.get(username=current_user)))
            elif SilantServiceCompany.objects.filter(user=User.objects.get(username=current_user)).exists():
                vehicles = Vehicle.objects.filter(service_company=SilantServiceCompany.objects.get(user=User.objects.get(username=current_user)))
            else:
                vehicles = Vehicle.objects.all()
        else:
            vehicles = Vehicle.objects.all()

        filterset = VehicleFilter(self.request.GET, vehicles)
        vehicles = filterset.qs
        context = {
            "vehicles": vehicles,
            "filterset": filterset,
            "found": filterset.qs.count()
        }
        return HttpResponse(render(request, 'flatpages/main.html', context))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['found'] = self.filterset.qs.count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if str(self.request.user) == "AnonymousUser":
            self.filterset = UnauuthorizedVehicleFilter(self.request.GET, queryset)

        else:
            self.filterset = VehicleFilter(self.request.GET, queryset)
        return self.filterset.qs

class VehicleCreate(PermissionRequiredMixin, CreateView): #LoginRequiredMixin,
    permission_required = ('mainApp.add_vehicle',)
    raise_exception = True
    form_class = VehicleForm
    model = Vehicle            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "flatpages/new_vehicle.html"


class VehicleDelete(PermissionRequiredMixin, DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    permission_required = ('mainApp.delete_vehicle',)
    model = Vehicle
    template_name = "flatpages/vehicle_delete.html"
    success_url = reverse_lazy('vehicle_list')

class TMList(ListView):
    model = TechnicalMaintenance #имя модели
    ordering = "-TM_date" #сортировка по полю модели
    template_name = "flatpages/TM.html" #название html шаблона
    context_object_name = 'TM' #контекстное название для исп.-я в шаблоне
    # paginate_by = 2  #также можно указать пагинацию (здесь на странице будет выводиться по 2 объекта)

    def get(self, request):
        current_user = str(request.user)

        if request.user.username:
            if SilantClient.objects.filter(user=User.objects.get(username=current_user)).exists():
                client = SilantClient.objects.get(user=User.objects.get(username=current_user))
                vehicles_set = Vehicle.objects.filter(client=client)
                TM = TechnicalMaintenance.objects.filter(TM_vehicle_SN__in=vehicles_set)
            elif SilantServiceCompany.objects.filter(user=User.objects.get(username=current_user)).exists():
                TM = TechnicalMaintenance.objects.filter(TM_service_company=SilantServiceCompany.objects.get(user=User.objects.get(username=current_user)))
            else:
                TM = TechnicalMaintenance.objects.all()
        else:
            TM = TechnicalMaintenance.objects.all()

        filterset = TechnicalMaintenanceFilter(self.request.GET, TM)
        TM = filterset.qs
        context = {
            "TM": TM,
            "filterset": filterset,
            "found": filterset.qs.count()
        }
        return HttpResponse(render(request, 'flatpages/TM.html', context))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['found'] = self.filterset.qs.count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = TechnicalMaintenanceFilter(self.request.GET, queryset)
        return self.filterset.qs

class TMCreate(PermissionRequiredMixin, CreateView): #LoginRequiredMixin,
    permission_required = ('mainApp.add_technicalmaintenance',)
    raise_exception = True
    form_class = TechnicalMaintenanceForm
    model = TechnicalMaintenance            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "flatpages/new_tm.html"

    def form_valid(self, form):
        TM = form.save(commit=False)
        TM.TM_service_company = Vehicle.objects.get(id=TM.TM_vehicle_SN_id).service_company
        return super().form_valid(form)


class TMDelete(PermissionRequiredMixin,  DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    permission_required = ('mainApp.delete_technicalmaintenance',)
    model = TechnicalMaintenance
    template_name = "flatpages/tm_delete.html"
    success_url = reverse_lazy('tm_list')


class ClaimList(ListView):
    model = ClientClaim #имя модели
    ordering = "-CC_breakdown_date" #сортировка по полю модели
    template_name = "flatpages/claims.html" #название html шаблона
    context_object_name = 'claims' #контекстное название для исп.-я в шаблоне
    # paginate_by = 2  #также можно указать пагинацию (здесь на странице будет выводиться по 2 объекта)

    def get(self, request):
        print('GET BEGIN')
        current_user = str(request.user)
        if request.user.username:

            if SilantClient.objects.filter(user=User.objects.get(username=current_user)).exists():
                client = SilantClient.objects.get(user=User.objects.get(username=current_user))
                vehicles_set = Vehicle.objects.filter(client=client)
                claims = ClientClaim.objects.filter(CC_vehicle_SN__in=vehicles_set)
            elif SilantServiceCompany.objects.filter(user=User.objects.get(username=current_user)).exists():
                claims = ClientClaim.objects.filter(CC_service_company=SilantServiceCompany.objects.get(user=User.objects.get(username=current_user)))
            else:
                claims = ClientClaim.objects.all()
        else:
            claims = ClientClaim.objects.all()

        filterset = ClientClaimFilter(self.request.GET, claims)
        claims = filterset.qs
        context = {
            "claims": claims,
            "filterset": filterset,
            "found": filterset.qs.count()
        }
        return HttpResponse(render(request, 'flatpages/claims.html', context))

    def get_context_data(self, **kwargs):
        print('GET_CONTEXT_DATA BEGIN')
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['found'] = self.filterset.qs.count()
        print('GET_CONTEXT_DATA END')
        return context

    def get_queryset(self):
        print('GET_QUERYSET BEGIN')
        queryset = super().get_queryset()
        self.filterset = ClientClaimFilter(self.request.GET, queryset)
        print('GET_QUERYSET END')
        return self.filterset.qs


class ClaimCreate(PermissionRequiredMixin, CreateView): #LoginRequiredMixin,
    permission_required = ('mainApp.add_clientclaim',)
    raise_exception = True
    form_class = ClaimForm
    model = ClientClaim            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "flatpages/new_claim.html"

    def form_valid(self, form):
        CC = form.save(commit=False)
        CC.CC_service_company = Vehicle.objects.get(id=CC.CC_vehicle_SN_id).service_company
        return super().form_valid(form)

class ClaimUpdate(PermissionRequiredMixin, UpdateView): #LoginRequiredMixin, PermissionRequiredMixin,
    permission_required = ('mainApp.change_clientclaim',)
    form_class = ClaimForm
    model = ClientClaim
    template_name = "flatpages/new_claim.html"


    def form_valid(self, form):
        obj = form.save(commit=False)
        b_date = obj.CC_breakdown_date
        r_date = obj.CC_recovery_date
        obj.CC_vehicle_downtime = int((r_date - b_date).days)
        return super(ClaimUpdate, self).form_valid(form)


class ClaimDelete(PermissionRequiredMixin,  DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    permission_required = ('mainApp.delete_clientclaim',)
    model = ClientClaim
    template_name = "flatpages/claim_delete.html"
    success_url = reverse_lazy('claim_list')


# --- СПИСОК ВЬЮШЕК НА СПРАВОЧНИКИ ---
class GuideVehicleList(ListView):
    model = GuideVehicle #имя модели
    ordering = "name"
    template_name = "guide_vehicle.html" #название html шаблона
    context_object_name = 'guide_vehicles' #контекстное название для исп.-я в шаблоне

class GuideVehicleView(DetailView):
    model = GuideVehicle
    template_name = "one_guide_object.html"
    context_object_name = 'one_guide_object'


class GuideVehicleCreate(CreateView): #LoginRequiredMixin,
    # permission_required = ('board.add_post',)
    raise_exception = True
    form_class = GuideVehicleForm
    model = GuideVehicle            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "new_guide.html"

class GuideVehicleUpdate(UpdateView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.change_post',)
    form_class = GuideVehicleForm
    model = GuideVehicle
    template_name = "new_guide.html"

class GuideVehicleDelete( DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.delete_post',)
    model = GuideVehicle
    template_name = "delete_guide.html"
    success_url = reverse_lazy('gv')


class GuideEngineList(ListView):
    model = GuideEngine #имя модели
    ordering = "name"
    template_name = "guide_engine.html" #название html шаблона
    context_object_name = 'guide_engines' #контекстное название для исп.-я в шаблоне

class GuideEngineView(DetailView):
    model = GuideEngine
    template_name = "one_guide_object.html"
    context_object_name = 'one_guide_object'


class GuideEngineCreate(CreateView): #LoginRequiredMixin,
    # permission_required = ('board.add_post',)
    raise_exception = True
    form_class = GuideEngineForm
    model = GuideEngine            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "new_guide.html"

class GuideEngineUpdate(UpdateView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.change_post',)
    form_class = GuideEngineForm
    model = GuideEngine
    template_name = "new_guide.html"

class GuideEngineDelete( DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.delete_post',)
    model = GuideEngine
    template_name = "delete_guide.html"
    success_url = reverse_lazy('ge')



class GuideTransmissionList(ListView):
    model = GuideTransmission #имя модели
    ordering = "name"
    template_name = "guide_transmission.html" #название html шаблона
    context_object_name = 'guide_transmissions' #контекстное название для исп.-я в шаблоне

class GuideTransmissionView(DetailView):
    model = GuideTransmission
    template_name = "one_guide_object.html"
    context_object_name = 'one_guide_object'


class GuideTransmissionCreate(CreateView): #LoginRequiredMixin,
    # permission_required = ('board.add_post',)
    raise_exception = True
    form_class = GuideTransmissionForm
    model = GuideTransmission            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "new_guide.html"

class GuideTransmissionUpdate(UpdateView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.change_post',)
    form_class = GuideTransmissionForm
    model = GuideTransmission
    template_name = "new_guide.html"

class GuideTransmissionDelete( DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.delete_post',)
    model = GuideTransmission
    template_name = "delete_guide.html"
    success_url = reverse_lazy('gt')



class GuideDrivingAxleList(ListView):
    model = GuideDrivingAxle #имя модели
    ordering = "name"
    template_name = "guide_driving_axle.html" #название html шаблона
    context_object_name = 'guide_driving_axles' #контекстное название для исп.-я в шаблоне

class GuideDrivingAxleView(DetailView):
    model = GuideDrivingAxle
    template_name = "one_guide_object.html"
    context_object_name = 'one_guide_object'


class GuideDrivingAxleCreate(CreateView): #LoginRequiredMixin,
    # permission_required = ('board.add_post',)
    raise_exception = True
    form_class = GuideDrivingAxleForm
    model = GuideDrivingAxle            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "new_guide.html"

class GuideDrivingAxleUpdate(UpdateView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.change_post',)
    form_class = GuideDrivingAxleForm
    model = GuideDrivingAxle
    template_name = "new_guide.html"

class GuideDrivingAxleDelete( DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.delete_post',)
    model = GuideDrivingAxle
    template_name = "delete_guide.html"
    success_url = reverse_lazy('gda')



class GuideControlAxleList(ListView):
    model = GuideControlAxle #имя модели
    ordering = "name"
    template_name = "guide_control_axle.html" #название html шаблона
    context_object_name = 'guide_control_axles' #контекстное название для исп.-я в шаблоне

class GuideControlAxleView(DetailView):
    model = GuideControlAxle
    template_name = "one_guide_object.html"
    context_object_name = 'one_guide_object'


class GuideControlAxleCreate(CreateView): #LoginRequiredMixin,
    # permission_required = ('board.add_post',)
    raise_exception = True
    form_class = GuideControlAxleForm
    model = GuideControlAxle            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "new_guide.html"

class GuideControlAxleUpdate(UpdateView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.change_post',)
    form_class = GuideControlAxleForm
    model = GuideControlAxle
    template_name = "new_guide.html"

class GuideControlAxleDelete( DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.delete_post',)
    model = GuideControlAxle
    template_name = "delete_guide.html"
    success_url = reverse_lazy('gca')



class GuideTMList(ListView):
    model = GuideTM #имя модели
    ordering = "name"
    template_name = "guide_tm.html" #название html шаблона
    context_object_name = 'guide_tms' #контекстное название для исп.-я в шаблоне

class GuideTMView(DetailView):
    model = GuideTM
    template_name = "one_guide_object.html"
    context_object_name = 'one_guide_object'


class GuideTMCreate(CreateView): #LoginRequiredMixin,
    # permission_required = ('board.add_post',)
    raise_exception = True
    form_class = GuideTMForm
    model = GuideTM            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "new_guide.html"

class GuideTMUpdate(UpdateView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.change_post',)
    form_class = GuideTMForm
    model = GuideTM
    template_name = "new_guide.html"

class GuideTMDelete( DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.delete_post',)
    model = GuideTM
    template_name = "delete_guide.html"
    success_url = reverse_lazy('gtm')



class GuideTMCompanyList(ListView):
    model = GuideTMCompany #имя модели
    ordering = "name"
    template_name = "guide_tm_company.html" #название html шаблона
    context_object_name = 'guide_tm_companys' #контекстное название для исп.-я в шаблоне

class GuideTMCompanyView(DetailView):
    model = GuideTMCompany
    template_name = "one_guide_object.html"
    context_object_name = 'one_guide_object'


class GuideTMCompanyCreate(CreateView): #LoginRequiredMixin,
    # permission_required = ('board.add_post',)
    raise_exception = True
    form_class = GuideTMCompanyForm
    model = GuideTMCompany            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "new_guide.html"

class GuideTMCompanyUpdate(UpdateView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.change_post',)
    form_class = GuideTMCompanyForm
    model = GuideTMCompany
    template_name = "new_guide.html"

class GuideTMCompanyDelete( DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.delete_post',)
    model = GuideTMCompany
    template_name = "delete_guide.html"
    success_url = reverse_lazy('gtmc')



class GuideBreakdownUnitList(ListView):
    model = GuideBreakdownUnit #имя модели
    ordering = "name"
    template_name = "guide_breakdown_unit.html" #название html шаблона
    context_object_name = 'guide_breakdown_units' #контекстное название для исп.-я в шаблоне

class GuideBreakdownUnitView(DetailView):
    model = GuideBreakdownUnit
    template_name = "one_guide_object.html"
    context_object_name = 'one_guide_object'


class GuideBreakdownUnitCreate(CreateView): #LoginRequiredMixin,
    # permission_required = ('board.add_post',)
    raise_exception = True
    form_class = GuideBreakdownUnitForm
    model = GuideBreakdownUnit            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "new_guide.html"

class GuideBreakdownUnitUpdate(UpdateView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.change_post',)
    form_class = GuideBreakdownUnitForm
    model = GuideBreakdownUnit
    template_name = "new_guide.html"

class GuideBreakdownUnitDelete( DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.delete_post',)
    model = GuideBreakdownUnit
    template_name = "delete_guide.html"
    success_url = reverse_lazy('gbu')


class GuideRepairTypeList(ListView):
    model = GuideRepairType #имя модели
    ordering = "name"
    template_name = "guide_repair_type.html" #название html шаблона
    context_object_name = 'guide_repair_types' #контекстное название для исп.-я в шаблоне

class GuideRepairTypeView(DetailView):
    model = GuideRepairType
    template_name = "one_guide_object.html"
    context_object_name = 'one_guide_object'


class GuideRepairTypeCreate(CreateView): #LoginRequiredMixin,
    # permission_required = ('board.add_post',)
    raise_exception = True
    form_class = GuideRepairTypeForm
    model = GuideRepairType            # также для этого класса переопределяем метод get_absolute_url в моделях
    template_name = "new_guide.html"

class GuideRepairTypeUpdate(UpdateView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.change_post',)
    form_class = GuideRepairTypeForm
    model = GuideRepairType
    template_name = "new_guide.html"

class GuideRepairTypeDelete( DeleteView): #LoginRequiredMixin, PermissionRequiredMixin,
    # permission_required = ('board.delete_post',)
    model = GuideRepairType
    template_name = "delete_guide.html"
    success_url = reverse_lazy('grt')


#####################################
#####################################
#####################################
#####################################


class SilantClientViewset(viewsets.ModelViewSet):
    queryset = SilantClient.objects.all()  #получаем все объекты модели
    serializer_class = SilantClientSerializer  #указываем наш сериалайзер из предыдущего пункта

class SilantServiceCompanyViewset(viewsets.ModelViewSet):
    queryset = SilantServiceCompany.objects.all()  #получаем все объекты модели
    serializer_class = SilantServiceCompanySerializer  #указываем наш сериалайзер из предыдущего пункта


class VehicleViewset(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()  #получаем все объекты модели
    serializer_class = VehicleSerializer  #указываем наш сериалайзер из предыдущего пункта

    def list(self, request):
        # print(f'self===:{self.__dict__}')
        print(f'request===:{request.data}')
        print(f'request.user===:{request.user}')
        return Response([])

class TechnicalMaintenanceViewset(viewsets.ModelViewSet):
    queryset = TechnicalMaintenance.objects.all()  #получаем все объекты модели
    serializer_class = TechnicalMaintenanceSerializer  #указываем наш сериалайзер из предыдущего пункта


class ClientClaimViewset(viewsets.ModelViewSet):
    queryset = ClientClaim.objects.all()  #получаем все объекты модели
    serializer_class = ClientClaimSerializer  #указываем наш сериалайзер из предыдущего пункта


class GuideVehicleViewset(viewsets.ModelViewSet):
    queryset = GuideVehicle.objects.all()
    serializer_class = GuideVehicleSerializer

class GuideEngineViewset(viewsets.ModelViewSet):
    queryset = GuideEngine.objects.all()
    serializer_class = GuideEngineSerializer

class GuideTransmissionViewset(viewsets.ModelViewSet):
    queryset = GuideTransmission.objects.all()
    serializer_class = GuideTransmissionSerializer

class GuideDrivingAxleViewset(viewsets.ModelViewSet):
    queryset = GuideDrivingAxle.objects.all()
    serializer_class = GuideDrivingAxleSerializer

class GuideControlAxleViewset(viewsets.ModelViewSet):
    queryset = GuideControlAxle.objects.all()
    serializer_class = GuideControlAxleSerializer

class GuideTMViewset(viewsets.ModelViewSet):
    queryset = GuideTM.objects.all()
    serializer_class = GuideTMSerializer

class GuideTMCompanyViewset(viewsets.ModelViewSet):
    queryset = GuideTMCompany.objects.all()
    serializer_class = GuideTMCompanySerializer

class GuideBreakdownUnitViewset(viewsets.ModelViewSet):
    queryset = GuideBreakdownUnit.objects.all()
    serializer_class = GuideBreakdownUnitSerializer

class GuideRepairTypeViewset(viewsets.ModelViewSet):
    queryset = GuideRepairType.objects.all()
    serializer_class = GuideRepairTypeSerializer