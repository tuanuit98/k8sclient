from kubernetes import client

def get_namespaces():
    """
    Return a list of all namespace names in the cluster.
    """
    v1 = client.CoreV1Api()
    namespaces = v1.list_namespace()
    return [ns.metadata.name for ns in namespaces.items]