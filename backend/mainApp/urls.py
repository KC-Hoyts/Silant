from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
   path('logout', logout_view, name='logout2'),

   path('vehicles/', VehicleList.as_view(), name="vehicle_list"),
   path('create_vehicle/', VehicleCreate.as_view(), name='vehicle_create'),
   path('<int:pk>/vehicle_delete/', VehicleDelete.as_view(), name='vehicle_delete'),

   path('technical_maintenances/', TMList.as_view(), name="tm_list"),
   path('create_tm/', TMCreate.as_view(), name='tm_create'),
   path('<int:pk>/tm_delete/', TMDelete.as_view(), name='tm_delete'),

   path('clients_claims/', ClaimList.as_view(), name="claim_list"),
   path('create_claim/', ClaimCreate.as_view(), name='claim_create'),
   path('<int:pk>/claim_edit/', ClaimUpdate.as_view(), name='claim_update'),
   path('<int:pk>/claim_delete/', ClaimDelete.as_view(), name='claim_delete'),

   path('guides/', TemplateView.as_view(template_name="flatpages/guides.html"), name="guides_list"),

   path('guide_vehicle/', GuideVehicleList.as_view(), name="gv"),
   path('vehicle/<int:pk>', GuideVehicleView.as_view(), name='gv_view'),
   path('create_gv/', GuideVehicleCreate.as_view(), name='gv_create'),
   path('<int:pk>/gv_edit/', GuideVehicleUpdate.as_view(), name='gv_update'),
   path('<int:pk>/gv_delete/', GuideVehicleDelete.as_view(), name='gv_delete'),

   path('guide_engine/', GuideEngineList.as_view(), name="ge"),
   path('engine/<int:pk>', GuideEngineView.as_view(), name='ge_view'),
   path('create_ge/', GuideEngineCreate.as_view(), name='ge_create'),
   path('<int:pk>/ge_edit/', GuideEngineUpdate.as_view(), name='ge_update'),
   path('<int:pk>/ge_delete/', GuideEngineDelete.as_view(), name='ge_delete'),

   path('guide_transmission/', GuideTransmissionList.as_view(), name="gt"),
   path('transmission/<int:pk>', GuideTransmissionView.as_view(), name='gt_view'),
   path('create_gt/', GuideTransmissionCreate.as_view(), name='gt_create'),
   path('<int:pk>/gt_edit/', GuideTransmissionUpdate.as_view(), name='gt_update'),
   path('<int:pk>/gt_delete/', GuideTransmissionDelete.as_view(), name='gt_delete'),

   path('guide_driving_axle/', GuideDrivingAxleList.as_view(), name="gda"),
   path('driving_axle/<int:pk>', GuideDrivingAxleView.as_view(), name='gda_view'),
   path('create_gda/', GuideDrivingAxleCreate.as_view(), name='gda_create'),
   path('<int:pk>/gda_edit/', GuideDrivingAxleUpdate.as_view(), name='gda_update'),
   path('<int:pk>/gda_delete/', GuideDrivingAxleDelete.as_view(), name='gda_delete'),

   path('guide_control_axle/', GuideControlAxleList.as_view(), name="gca"),
   path('control_axle/<int:pk>', GuideControlAxleView.as_view(), name='gca_view'),
   path('create_gca/', GuideControlAxleCreate.as_view(), name='gca_create'),
   path('<int:pk>/gca_edit/', GuideControlAxleUpdate.as_view(), name='gca_update'),
   path('<int:pk>/gca_delete/', GuideControlAxleDelete.as_view(), name='gca_delete'),

   path('guide_tm/', GuideTMList.as_view(), name="gtm"),
   path('technical_maintenance/<int:pk>', GuideTMView.as_view(), name='gtm_view'),
   path('create_gtm/', GuideTMCreate.as_view(), name='gtm_create'),
   path('<int:pk>/gtm_edit/', GuideTMUpdate.as_view(), name='gtm_update'),
   path('<int:pk>/gtm_delete/', GuideTMDelete.as_view(), name='gtm_delete'),

   path('guide_tm_company/', GuideTMCompanyList.as_view(), name="gtmc"),
   path('tm_company/<int:pk>', GuideTMCompanyView.as_view(), name='gtmc_view'),
   path('create_gtmc/', GuideTMCompanyCreate.as_view(), name='gtmc_create'),
   path('<int:pk>/gtmc_edit/', GuideTMCompanyUpdate.as_view(), name='gtmc_update'),
   path('<int:pk>/gtmc_delete/', GuideTMCompanyDelete.as_view(), name='gtmc_delete'),

   path('guide_breakdown_unit/', GuideBreakdownUnitList.as_view(), name="gbu"),
   path('breakdown_unit/<int:pk>', GuideBreakdownUnitView.as_view(), name='gbu_view'),
   path('create_gbu/', GuideBreakdownUnitCreate.as_view(), name='gbu_create'),
   path('<int:pk>/gbu_edit/', GuideBreakdownUnitUpdate.as_view(), name='gbu_update'),
   path('<int:pk>/gbu_delete/', GuideBreakdownUnitDelete.as_view(), name='gbu_delete'),

   path('guide_repair_type', GuideRepairTypeList.as_view(), name="grt"),
   path('repair_type/<int:pk>', GuideRepairTypeView.as_view(), name='grt_view'),
   path('create_grt/', GuideRepairTypeCreate.as_view(), name='grt_create'),
   path('<int:pk>/grt_edit/', GuideRepairTypeUpdate.as_view(), name='grt_update'),
   path('<int:pk>/grt_delete/', GuideRepairTypeDelete.as_view(), name='grt_delete'),
]


