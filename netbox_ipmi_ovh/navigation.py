from extras.plugins import PluginMenuItem

# Add the IPMI Config link to the menu Plugins
menu_items = (
    PluginMenuItem(
        link_text="IPMI OVH", link="plugins:netbox_ipmi_ovh:ipmi_config",
        permissions=["netbox_ipmi_ovh.view_ipmi"],
    ),
)
