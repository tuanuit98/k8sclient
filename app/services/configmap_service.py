from kubernetes import client
import yaml
from datetime import datetime, timezone

def get_configmaps_in_namespace(namespace: str):
    v1 = client.CoreV1Api()
    configmaps = v1.list_namespaced_config_map(namespace)
    # Return a list of configmap names, their data, and age
    return [
        {
            "name": cm.metadata.name,
            "data": cm.data,
            "age": (
                f"{(datetime.now(timezone.utc) - cm.metadata.creation_timestamp).days}d"
                if cm.metadata.creation_timestamp else "N/A"
            )
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

def get_configmap_yaml(namespace: str, name: str):
    v1 = client.CoreV1Api()
    cm = v1.read_namespaced_config_map(name, namespace)
    cm_dict = cm.to_dict()
    return yaml.dump(cm_dict, sort_keys=False)