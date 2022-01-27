from extras.plugins import PluginTemplateExtension
from django.conf import settings
from packaging import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)


class IpmiButton(PluginTemplateExtension):
    """
    Extend the DCIM site template to include content from this plugin.
    """
    model = 'dcim.site'

    def buttons(self):
        return self.render('netbox_ipmi_ovh_plugin/ipmi_button.html')


template_extensions = [IpmiButton]
