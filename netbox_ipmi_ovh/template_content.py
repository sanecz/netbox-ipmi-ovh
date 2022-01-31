from extras.plugins import PluginTemplateExtension

class IpmiButton(PluginTemplateExtension):
    """
    Extend the DCIM device template to include content from this plugin.
    """
    model = 'dcim.device'

    def buttons(self):
        return self.render('netbox_ipmi_ovh/ipmi_button.html')

template_extensions = [IpmiButton]
