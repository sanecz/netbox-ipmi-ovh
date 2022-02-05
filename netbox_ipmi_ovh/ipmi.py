import time
from netbox_ipmi_ovh.exceptions import NetboxIpmiOvhTimeout, NetboxIpmiOvhError

def wait_for_ovh_task(client, service_name, task_id):
    """
    Wait for OVH task to finish
    :param client: Instance of ovh.Client()
    :param service_name: Name of the dedicated server (by ovh name: nsXXXXXX.ip-XX-YY-ZZ.tld
    :param task_id: ID of the task from /dedicated/server/{service_name}/features/ipmi/access

    :raises NetboxIpmiOvhError: Raised when status is changed to ovhError/customerError and ipmi
    cannot be given
    :raises NetboxIpmiOvhTimeout: Raised when requests take more than 120seconds, should happend
    rarely / never except if your BMC is dying

    :return: Nothing, if it returns then the command is successful
    """
    for _ in range(120):  # ovh timeout is between 120 seconds and 20minutes in worst case (trust me i tried)
        result = client.get(f"/dedicated/server/{service_name}/task/{task_id}")
        if result["status"] == "done":
            return
        elif result["status"] in ["ovhError", "customerError"]:
            raise NetboxIpmiOvhError(result["status"]["comment"])
        time.sleep(1)
    else:
        raise NetboxIpmiOvhTimeout("Task is taking too long - Timeout")


def request_ipmi_access(client, service_name, access_type, ssh_key=None, ip_to_allow=None):
    """
    Request an IPMI access by calling the OVH API
    :param client: Instance of ovh.Client()
    :param service_name: Name of the dedicated server (by ovh name: nsXXXXXX.ip-XX-YY-ZZ.tld
    :param access_type: IPMI console access type
    :param ssh_key: SSH key name to allow access on KVM/IP interface with (name from /me/sshKey)
    :param ip_to_allow: IP to allow connection from for this IPMI session

    :return: URL to kvmIP, ssh command line in string or JNLP xml string depending on the access type
    :rtype: str
    """
    # I could also do the check of the features in the template_content
    # but i do not want to slow down the loading of the page, as we don't
    # know if the OVH api is up or down or very slow


    # Retreive available features for the server (sometime somes are not enabled or even IPMI is not enabled)
    result = client.get(
        f'/dedicated/server/{service_name}/features/ipmi'
    )

    supported_features = [k for k, v in result["supportedFeatures"].items() if v]

    if not result["activated"]:
        raise NetboxIpmiOvhError("IPMI is not active on this server")

    if not access_type in supported_features:
        raise NetboxIpmiOvhError(
            f"Access type {access_type} is not supported by this server. "
            f"Supported access types: {', '.join(supported_features)} "
        )

    # https://api.ovh.com/console/#/dedicated/server/{serviceName}/features/ipmi/access#POST
    parameters = {
        "type": access_type,
        "ttl": 15,
        "ipToAllow": ip_to_allow
    }

    if 'ssh' in access_type.lower() and not ssh_key:
        raise NetboxIpmiOvhError(
            f"SSH Key name required for {access_type}, please fill your "
            "ssh key name in your configuration" 
        )

    if ssh_key:
        parameters["sshKey"] = ssh_key

    result = client.post(
        f'/dedicated/server/{service_name}/features/ipmi/access',
        **parameters
    )

    wait_for_ovh_task(client, service_name, result['taskId'])

    # finally retreive the IPMI access
    result = client.get(
        f'/dedicated/server/{service_name}/features/ipmi/access',
        type=access_type
    )

    return result["value"]
