from extras.plugins import PluginConfig

class NetboxIpmiOvhConfig(PluginConfig):
    name = 'netbox_ipmi_ovh_plugin'
    verbose_name = 'Netbox ipmi ovh'
    description = ''
    version = '0.0.1'
    author = 'Lisa Bekdache'
    author_email = 'lisa.bekdache@gmail.com'
    base_url = 'netbox-ipmi-ovh'
    required_settings = []
    default_settings = {}

config = NetboxIpmiOvhConfig
