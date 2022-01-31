from django import forms
from netbox_ipmi_ovh.models import Ipmi
from utilities.forms import BootstrapMixin

class UserIpmiCfgForm(BootstrapMixin, forms.ModelForm):
    ssh_key_name = forms.CharField(
        label="SSH key name",
        help_text="Name of the ssh key added in the OVH Manager",
        max_length=100,
        required=False
    )
    ip_to_allow = forms.CharField(
        label="IP to allow",
        help_text="Leave this value to empty if you want to ip from your http request to be allowed for the IPMI connection. If you're using a proxy or VPN, please set the correct IP to be sent to allowed ip for the ipmi login.",
        max_length=100,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Ipmi
        fields = ["ssh_key_name", "ip_to_allow"]

