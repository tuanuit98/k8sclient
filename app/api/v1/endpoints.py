from fastapi import APIRouter
from services.pod_service import get_pods_in_namespace
from services.pod_service import read_namespaced_pod
from services.log_service import get_pod_logs
from services.configmap_service import get_configmaps_in_namespace

router = APIRouter()

@router.get("/")
def read_root():
    pod_names = get_pods_in_namespace(namespace="default")
    for name in pod_names:
        print(name)
    return {"pods": pod_names}

@router.get("/namespace/{namespace}/pods")
def get_pods_by_namespace(namespace: str):
    pod_names = get_pods_in_namespace(namespace)
    return {"namespace": namespace, "pods": pod_names}

@router.get("/namespace/{namespace}/pod/{pod_name}")
def get_pod_by_namespace_and_name(namespace: str, pod_name: str):
    pod_details = read_namespaced_pod(pod_name, namespace)
    return {"pod_details": pod_details}

@router.get("/namespace/{namespace}/pod/{pod_name}/logs")
def get_pod_logs_route(namespace: str, pod_name: str, tail_lines: int = 100):
    logs = get_pod_logs(name=pod_name, namespace=namespace, tail_lines=tail_lines)
    log_lines = logs.splitlines() if logs else []
    return {"logs": log_lines}

@router.get("/namespace/{namespace}/configmaps")
def get_configmaps_by_namespace(namespace: str):
    configmaps = get_configmaps_in_namespace(namespace)
    return {"namespace": namespace, "configmaps": configmaps}