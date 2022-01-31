from dcim.models import Device
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages

from netbox_ipmi_ovh.forms import UserIpmiCfgForm
from netbox_ipmi_ovh.models import Ipmi as UserIpmiCfg
from netbox_ipmi_ovh.ipmi import request_ipmi_access

from ovh import Client

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("netbox_ipmi_ovh", dict())

OVH_ENDPOINTS = PLUGIN_SETTINGS["endpoints"]
OVH_ENDPOINT_FIELD = PLUGIN_SETTINGS["ovh_endpoint_field"]
OVH_SERVER_NAME_FIELD = PLUGIN_SETTINGS["ovh_server_name_field"]

MAPPING_ACCESS_TYPE = {
    "kvmipHtml5URL": "url",
    "kvmipJnlp": "jnlp",
    "serialOverLanURL": "url",
    "serialOverLanSshKey": "ssh"
}

class BaseIpmiView(PermissionRequiredMixin, View):
    permission_required = 'netbox_ipmi_ovh.view_ipmi'

    @staticmethod
    def _get_user_config(user):
        try:
            usercfg = UserIpmiCfg.objects.get(user=user)
        except UserIpmiCfg.DoesNotExist:
            usercfg = UserIpmiCfg(user=user)
        return usercfg


class UserIpmiCfgView(BaseIpmiView):
    template_name = 'netbox_ipmi_ovh/ipmi_config.html'

    def post(self, request):
        usercfg = self._get_user_config(request.user)

        form = UserIpmiCfgForm(data=request.POST, instance=usercfg)

        if form.is_valid():
            usercfg = form.save(commit=False)
            usercfg.user = request.user
            usercfg.save()
            messages.success(request, "Settings has been changed successfully.")

        return render(request, self.template_name, {
            'object': usercfg,
            'form': form
        })

    def get(self, request):
        usercfg = self._get_user_config(request.user)
        form = UserIpmiCfgForm(instance=usercfg)

        return render(request, self.template_name, {
            'object': usercfg,
            'form': form
        })


class IpmiView(BaseIpmiView):
    def get(self, request):
        device_id = request.GET.get("device")
        access_type = request.GET.get("type")
        usercfg = self._get_user_config(request.user)
        device = Device.objects.get(id=device_id)

        ovh_server_name = getattr(device, OVH_SERVER_NAME_FIELD)

        if hasattr(device, OVH_ENDPOINT_FIELD):
            ovh_endpoint = getattr(device, OVH_ENDPOINT_FIELD)
        elif OVH_ENDPOINT_FIELD in device.custom_field_data:
            ovh_endpoint = device.custom_field_data[OVH_ENDPOINT_FIELD]
        else:
            raise Exception # something?

        client = Client(**OVH_ENDPOINTS[ovh_endpoint])
        access = request_ipmi_access(
            client,
            ovh_server_name,
            access_type,
            ip_to_allow=usercfg.ip_to_allow,
            ssh_key=usercfg.ssh_key_name
        )

        if MAPPING_ACCESS_TYPE[access_type] == "url":
            return redirect(access)
        elif MAPPING_ACCESS_TYPE[access_type] == "jnlp":
            return HttpResponse(access, content_type='application/x-java-jnlp-file')
        elif MAPPING_ACCESS_TYPE[access_type] == "ssh":
            return HttpResponse(f"Please connect to: {access}")

            

