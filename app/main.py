import time
start = time.time()
from fastapi import FastAPI
import uvicorn

from api.v1 import endpoints
print("Imports took", time.time() - start, "seconds")

app = FastAPI()

app.include_router(endpoints.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

