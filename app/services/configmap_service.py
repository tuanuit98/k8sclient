from kubernetes import client

def get_configmaps_in_namespace(namespace: str):
    v1 = client.CoreV1Api()
    configmaps = v1.list_namespaced_config_map(namespace)
    # Return a list of configmap names and their data
    return [
        {
            "name": cm.metadata.name,
            "data": cm.data
        }
        for cm in configmaps.items
    ]

def get_configmaps_in_namespace_plain(namespace: str):
    """
    Return all configmaps in the namespace as a plain text string.
    """
    v1 = client.CoreV1Api()
    configmaps = v1.list_namespaced_config_map(namespace)
    plain = ""
    for cm in configmaps.items:
        plain += f"===== {cm.metadata.name} =====\n"
        if cm.data:
            for key, value in cm.data.items():
                plain += f"{key}:\n{value}\n"
        else:
            plain += "(empty)\n"
        plain += "\n"
    return plain