from kubernetes import client, config

def get_configmaps_in_namespace(namespace: str, kube_config: str = None):
    # Load kubeconfig from a file or default location
    if kube_config:
        config.load_kube_config(config_file=kube_config)
    else:
        config.load_kube_config()
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