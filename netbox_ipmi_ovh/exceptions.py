class NetboxIpmiOvh(Exception):
    """
    Base exception for the netbox-ipmi-ovh plugin
    """
    pass


class NetboxIpmiOvhTimeout(NetboxIpmiOvh):
    """
    Exception when OVH is too slow to answer
    i.e BMC is down on the server
    """
    pass


class NetboxIpmiOvhError(NetboxIpmiOvh):
    """
    Exception for wrong arguments or error thrown
    by the OVH API
    """
    pass
