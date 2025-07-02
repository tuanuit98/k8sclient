import time
start = time.time()
from fastapi import FastAPI
import uvicorn
from kubernetes import config
from fastapi.staticfiles import StaticFiles

from api.v1 import endpoints
print("Imports took", time.time() - start, "seconds")

# Load kubeconfig ONCE at startup
config.load_kube_config()

app = FastAPI()

app.include_router(endpoints.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

