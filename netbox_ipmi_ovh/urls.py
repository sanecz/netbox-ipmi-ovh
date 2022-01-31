from django.urls import path
from . import views

urlpatterns = [
    path('ipmi/', views.IpmiView.as_view(), name='ipmi'),
    path('ipmi/ipmi-config/', views.UserIpmiCfgView.as_view(), name='ipmi_config'),
]
