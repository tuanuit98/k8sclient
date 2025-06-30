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