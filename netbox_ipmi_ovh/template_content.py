from extras.plugins import PluginTemplateExtension
from django.conf import settings
from packaging import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("netbox_ipmi_ovh",  {})
OVH_ENDPOINT_FIELD = PLUGIN_SETTINGS["ovh_endpoint_field"]


class IpmiButton(PluginTemplateExtension):
    """
    Extend the DCIM device template to include content from this plugin.
    """
    model = 'dcim.device'
    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_button =  'netbox_ipmi_ovh/ipmi_button_3.x.html'
    else:
        template_button =  'netbox_ipmi_ovh/ipmi_button.html'

    def buttons(self):
        device = self.context["object"]
        has_ipmi = False

        if getattr(device, OVH_ENDPOINT_FIELD, None) or device.custom_field_data.get(OVH_ENDPOINT_FIELD, None):
            has_ipmi = True

        return self.render(
            self.template_button,
            extra_context={
                'has_ipmi': has_ipmi
            }
        )

template_extensions = [IpmiButton]
