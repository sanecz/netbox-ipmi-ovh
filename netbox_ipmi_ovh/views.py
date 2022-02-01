from dcim.models import Device
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from ovh import Client, APIError

from netbox_ipmi_ovh.forms import UserIpmiCfgForm
from netbox_ipmi_ovh.models import Ipmi as UserIpmiCfg
from netbox_ipmi_ovh.ipmi import request_ipmi_access
from netbox_ipmi_ovh.exceptions import NetboxIpmiOvh


PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("netbox_ipmi_ovh", {})
OVH_ENDPOINTS = PLUGIN_SETTINGS["endpoints"]
OVH_ENDPOINT_FIELD = PLUGIN_SETTINGS["ovh_endpoint_field"]
OVH_SERVER_NAME_FIELD = PLUGIN_SETTINGS["ovh_server_name_field"]

MAPPING_ACCESS_TYPE = {
    "kvmipHtml5URL": lambda access: redirect(access),
    "kvmipJnlp": lambda access: HttpResponse(access, content_type='application/x-java-jnlp-file'),
    "serialOverLanURL": lambda access: redirect(access),
    "serialOverLanSshKey": lambda access: HttpResponse(f"Please connect to: {access}")
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
    template_error = "netbox_ipmi_ovh/ipmi_error.html"

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
            return render(request, self.template_error, {
                "error_message": "No OVH endpoint has been detected, cannot process request"
            })

        if ovh_endpoint not in OVH_ENDPOINTS:
            return render(request, self.template_error, {
                "error_message": f"Endpoint {ovh_endpoint} does not exist, please check endpoint name or your PLUGIN_SETTINGS"
            })

        client = Client(**OVH_ENDPOINTS[ovh_endpoint])

        # trying to retrieive user IP to send to ovh
        # if no ip is send in args to ovh api, they will use the ip used for
        # the http call to their api, and it will be the server ip

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            access = request_ipmi_access(
                client, ovh_server_name,
                access_type, ip_to_allow=usercfg.ip_to_allow or ip,
                ssh_key=usercfg.ssh_key_name
            )
        except APIError as e:
            return render(request, self.template_error, {
                "error_message": f"An error occured while contacting OVH: {e}"
            })

        except NetboxIpmiOvh as e:
            return render(request, self.template_error, {
                "error_message": f"An error occured while trying to request IPMI access: {e}"
            })

        # we should never trigger this as it's handled in request_ipmi_access
        assert access_type in MAPPING_ACCESS_TYPE

        return MAPPING_ACCESS_TYPE[access_type](access)
