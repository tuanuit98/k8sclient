from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from services.pod_service import *
from services.log_service import *
from services.configmap_service import *
from services.namespace_service import *
import time

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/")
def read_root(request: Request):
    namespaces = get_namespaces()
    selected_namespace = "default"
    pods = get_pods_in_namespace(selected_namespace)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "namespaces": namespaces,
            "pods": pods,
            "selected_namespace": selected_namespace,
        }
    )

@router.get("/namespace/{namespace}/pods")
def get_pods_by_namespace(namespace: str):
    pod_list = get_pods_in_namespace(namespace)
    return {"pods": pod_list}

@router.get("/namespace/{namespace}/pod/{pod_name}")
def get_pod_by_namespace_and_name(namespace: str, pod_name: str):
    pod_details = read_namespaced_pod(pod_name, namespace)
    return pod_details


@router.get("/namespace/{namespace}/pod/{pod_name}/logs")
def get_pod_logs_route(namespace: str, pod_name: str, tail_lines: int = 100):
    logs = get_pod_logs(name=pod_name, namespace=namespace, tail_lines=tail_lines)
    # logs is a dict: {container_name: log_string}
    # Join all logs as plain text (if multiple containers, concatenate with header)
    if isinstance(logs, dict):
        plain_logs = ""
        for container, log in logs.items():
            plain_logs += f"===== {container} =====\n{log}\n"
    else:
        plain_logs = logs
    return PlainTextResponse(plain_logs)

@router.get("/namespace/{namespace}/pod/{pod_name}/logs/follow")
def follow_pod_logs_route(namespace: str, pod_name: str):
    def log_stream():
        start_time = time.time()
        for line in follow_pod_logs(name=pod_name, namespace=namespace):
            if time.time() - start_time > 90:
                break
            yield line + "\n"
    return StreamingResponse(log_stream(), media_type="text/plain")

@router.get("/namespace/{namespace}/configmaps")
def get_configmaps_by_namespace(namespace: str):
    configmaps = get_configmaps_in_namespace(namespace)
    return {"configmaps": configmaps}

@router.get("/namespace/{namespace}/pod/{pod_name}/fragment")
def get_pod_by_namespace_and_name(request: Request, namespace: str, pod_name: str):
    pod_details = read_namespaced_pod(pod_name, namespace)
    return templates.TemplateResponse(
        "pod_detail.html",
        {"request": request, "namespace": namespace, "pod_details": pod_details},
    )
