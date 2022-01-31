from extras.plugins import PluginConfig

class NetboxIpmiOvhConfig(PluginConfig):
    name = 'netbox_ipmi_ovh'
    verbose_name = 'Netbox ipmi ovh'
    description = ''
    version = '0.0.1'
    author = 'Lisa Bekdache'
    author_email = 'lisa.bekdache@gmail.com'
    base_url = 'netbox_ipmi_ovh'
    required_settings = ['ovh_server_name_field', 'ovh_endpoint_field', 'endpoints']
    default_settings = {}

config = NetboxIpmiOvhConfig