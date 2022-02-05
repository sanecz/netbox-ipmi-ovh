from extras.plugins import PluginConfig

class NetboxIpmiOvhConfig(PluginConfig):
    name = 'netbox_ipmi_ovh'
    verbose_name = 'Netbox ipmi ovh'
    description = 'A plugin used to add a button in the dcim.device to allow easier access to the IPMI for OVH managed bare metal servers.'
    version = '1.0.2'
    author = 'Lisa Bekdache'
    author_email = 'lisa.bekdache@gmail.com'
    base_url = 'netbox_ipmi_ovh'
    required_settings = ['ovh_server_name_field', 'ovh_endpoint_field', 'endpoints']
    default_settings = {}

config = NetboxIpmiOvhConfig
