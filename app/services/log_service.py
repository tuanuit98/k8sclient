from kubernetes import client
from services.pod_service import get_software_container_name

def get_pod_logs(name: str, namespace: str, tail_lines: int = 500):
    v1 = client.CoreV1Api()
    container_names = get_software_container_name(name, namespace)
    container = container_names[0]
    log = v1.read_namespaced_pod_log(
        name=name,
        namespace=namespace,
        container=container,
        tail_lines=tail_lines
    )
    return {container: log}

def follow_pod_logs(name: str, namespace: str):
    v1 = client.CoreV1Api()
    container_names = get_software_container_name(name, namespace)
    container = container_names[0]
    stream = v1.read_namespaced_pod_log(
        name=name,
        namespace=namespace,
        container=container,
        follow=True,
        _preload_content=False,
        _return_http_data_only=True,
    )
    for line in stream:
        yield line.decode('utf-8').rstrip()


