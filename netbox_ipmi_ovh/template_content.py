from extras.plugins import PluginTemplateExtension
from django.conf import settings


PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("netbox_ipmi_ovh",  {})
OVH_ENDPOINT_FIELD = PLUGIN_SETTINGS["ovh_endpoint_field"]


class IpmiButton(PluginTemplateExtension):
    """
    Extend the DCIM device template to include content from this plugin.
    """
    model = 'dcim.device'

    def buttons(self):
        device = self.context["object"]
        has_ipmi = False

        if hasattr(device, OVH_ENDPOINT_FIELD) or OVH_ENDPOINT_FIELD in device.custom_field_data:
            has_ipmi = True

        return self.render(
            'netbox_ipmi_ovh/ipmi_button.html',
            extra_context={
                'has_ipmi': has_ipmi
            }
        )

template_extensions = [IpmiButton]
