from fastapi import APIRouter
from services.pod_service import get_pods_in_namespace
from services.pod_service import read_namespaced_pod

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
def get_pods_by_namespace(namespace: str, pod_name: str):
    pod_details = read_namespaced_pod(pod_name, namespace)
    return {"pod_details": pod_details}  