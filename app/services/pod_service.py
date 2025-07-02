from kubernetes import client
from datetime import datetime, timezone

def get_pods_in_namespace(namespace: str):
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace)
    pod_list = []
    for pod in pods.items:
        # Count ready containers
        ready = 0
        total = len(pod.status.container_statuses) if pod.status.container_statuses else 0
        if pod.status.container_statuses:
            for cs in pod.status.container_statuses:
                if cs.ready:
                    ready += 1
        # Pod status
        status = pod.status.phase
        # Restarts (sum for all containers)
        restarts = sum(cs.restart_count for cs in pod.status.container_statuses) if pod.status.container_statuses else 0
        # Age (in days)
        start_time = pod.status.start_time
        if start_time:
            age_days = (datetime.now(timezone.utc) - start_time).days
            age_str = f"{age_days}d"
        else:
            age_str = "N/A"
        pod_list.append({
            "name": pod.metadata.name,
            "ready": f"{ready}/{total}",
            "status": status,
            "restarts": restarts,
            "age": age_str
        })
    return pod_list

def read_namespaced_pod(name: str, namespace: str):
    v1 = client.CoreV1Api()
    pod = v1.read_namespaced_pod(name=name, namespace=namespace)

    # Try to get current usage from metrics API
    current_usage = {}
    try:
        metrics_api = client.CustomObjectsApi()
        metrics = metrics_api.get_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="pods",
            name=name
        )
        # Build a dict of current usage per container
        for c in metrics.get("containers", []):
            current_usage[c["name"]] = {
                "cpu": format_cpu(c["usage"].get("cpu")),
                "memory": format_memory(c["usage"].get("memory"))
            }
    except Exception as e:
        # Metrics API might not be available
        pass

    pod_details = {
        "name": pod.metadata.name,
        "namespace": pod.metadata.namespace,
        "status": pod.status.phase,
        "node_name": pod.spec.node_name,
        "start_time": str(pod.status.start_time),
        "containers": [],
        "labels": pod.metadata.labels,
        "annotations": pod.metadata.annotations,
        "host_ip": pod.status.host_ip,
        "pod_ip": pod.status.pod_ip,
        "conditions": []
    }

    # Add container details with resources and current usage
    for container in pod.spec.containers:
        # Only show CPU & memory for requests/limits
        requests = {}
        limits = {}
        if container.resources and container.resources.requests:
            if "cpu" in container.resources.requests:
                requests["cpu"] = container.resources.requests["cpu"]
            if "memory" in container.resources.requests:
                requests["memory"] = container.resources.requests["memory"]
        if container.resources and container.resources.limits:
            if "cpu" in container.resources.limits:
                limits["cpu"] = container.resources.limits["cpu"]
            if "memory" in container.resources.limits:
                limits["memory"] = container.resources.limits["memory"]

        # Set to None if empty
        requests_out = requests if requests else None
        limits_out = limits if limits else None
        current_out = current_usage.get(container.name, {})
        if not current_out or not any(current_out.values()):
            current_out = {"cpu": None, "memory": None}
        else:
            # Ensure both keys exist and set to None if missing
            current_out = {
                "cpu": current_out.get("cpu", None),
                "memory": current_out.get("memory", None)
            }

        container_info = {
            "name": container.name,
            "image": container.image,
            "resources": {
                "requests": requests_out if requests_out else {"cpu": None, "memory": None},
                "limits": limits_out if limits_out else {"cpu": None, "memory": None},
                "current": current_out
            }
        }
        pod_details["containers"].append(container_info)

    # Add readable conditions
    if pod.status.conditions:
        for cond in pod.status.conditions:
            pod_details["conditions"].append({
                "type": cond.type,
                "status": cond.status,
                "last_probe_time": str(cond.last_probe_time) if cond.last_probe_time else None,
                "last_transition_time": str(cond.last_transition_time) if cond.last_transition_time else None
            })

    return pod_details

def format_cpu(cpu_str):
    # CPU is usually in nanocores (e.g., "123456n"), convert to millicores ("m")
    if cpu_str is None:
        return "0m"
    if cpu_str.endswith("n"):
        millicores = int(cpu_str[:-1]) / 1_000_000
        return f"{int(millicores)}m"
    if cpu_str.endswith("m"):
        return cpu_str
    try:
        # Assume it's in cores (e.g., "1"), convert to millicores
        millicores = float(cpu_str) * 1000
        return f"{int(millicores)}m"
    except Exception:
        return cpu_str

def format_memory(mem_str):
    # Memory is usually in Ki, Mi, Gi, etc. Convert Ki to Mi for display
    if mem_str is None:
        return "0Mi"
    if mem_str.endswith("Ki"):
        mebibytes = int(mem_str[:-2]) / 1024
        return f"{int(mebibytes)}Mi"
    if mem_str.endswith("Mi") or mem_str.endswith("Gi"):
        return mem_str
    try:
        # If it's just a number, assume bytes and convert to Mi
        mebibytes = int(mem_str) / (1024 * 1024)
        return f"{int(mebibytes)}Mi"
    except Exception:
        return mem_str

def get_software_container_name(name: str, namespace: str):
    """
    Return a list of container names for the given pod,
    excluding any container whose name includes 'proxy'.
    """
    v1 = client.CoreV1Api()
    pod = v1.read_namespaced_pod(name=name, namespace=namespace)
    return [container.name for container in pod.spec.containers if "proxy" not in container.name]


