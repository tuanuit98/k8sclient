from kubernetes import client, config

def get_pod_logs(name: str, namespace: str, kube_config: str = None, tail_lines: int = 100):
    # Load kubeconfig from a file or default location
    if kube_config:
        config.load_kube_config(config_file=kube_config)
    else:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        logs = v1.read_namespaced_pod_log(
            name=name,
            namespace=namespace,
            tail_lines=tail_lines
        )
        return logs
    except client.exceptions.ApiException as e:
        return f"Error fetching logs: {e}"

def follow_pod_logs(name: str, namespace: str, kube_config: str = None, container: str = None):
    """
    Stream logs from a pod (like `kubectl logs -f`).
    Yields log lines as they arrive.
    """
    if kube_config:
        config.load_kube_config(config_file=kube_config)
    else:
        config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        stream = v1.read_namespaced_pod_log(
            name=name,
            namespace=namespace,
            container=container,
            follow=True,
            _preload_content=False,
            _return_http_data_only=True,
        )
        for line in stream:
            yield line.decode("utf-8").rstrip()
    except client.exceptions.ApiException as e:
        yield f"Error fetching logs: {e}"

# Example usage:
# logs = get_pod_logs("nginx-deployment-pod", "default")
# print(logs)
#
# for log_line in follow_pod_logs("nginx-deployment-pod", "default"):
#     print(log_line)