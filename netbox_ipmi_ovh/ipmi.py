import ovh
import signal
import time
import sys

ALLOWED_ACCESS_TYPE = ["kvmipHtml5URL", "kvmipJnlp", "serialOverLanURL", "serialOverLanSshKey"]

def wait_for_ovh_task(client, service_name, task_id):
    # should take less than 30 secs
    for _ in range(30):
        result = client.get(f"/dedicated/server/{service_name}/task/{task_id}")
        if result["status"] == "done":
            return
        time.sleep(1)
    else:
        raise Exception  # fixme

def request_ipmi_access(client, service_name, access_type, ssh_key=None, ip_to_allow=None):
    result = client.get(
        f'/dedicated/server/{service_name}/features/ipmi'
    )

    assert access_type in ALLOWED_ACCESS_TYPE

    parameters = {
        "type": access_type,
        "ttl": 15
    }

    if ssh_key:
        parameters["sshKey"] = ssh_key
    if ip_to_allow:
        parameters["ipToAllow"] = ip_to_allow

    #fixme: add parameters later

    result = client.post(
        f'/dedicated/server/{service_name}/features/ipmi/access',
        **parameters
    )
    
    wait_for_ovh_task(client, service_name, result['taskId'])

    result = client.get(
        f'/dedicated/server/{service_name}/features/ipmi/access',
        type=access_type
    )

    return result["value"]

def get_prefered_ipmi_access(features_ipmi):
    """
    Return the prefered ipmi access type based on the order of
    prefered_access_type
    """
    assert features_ipmi["activated"]

    for access_type in prefered_access_type:
        if features_ipmi["supportedFeatures"].get(access_type, False):
            return access_type


if __name__ == "__main__":
    client = ovh.Client(endpoint="ovh-us")
    print(request_ipmi_access(client, sys.argv[1]))
