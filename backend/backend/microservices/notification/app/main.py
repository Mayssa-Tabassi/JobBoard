
"""Notification microservice - entry point."""

import os
from contextlib import asynccontextmanager

import py_eureka_client.eureka_client as eureka_client
from fastapi import FastAPI

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Enregistrement asynchrone dans Eureka
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka/",
        app_name="NOTIFICATION",
        instance_host="localhost",
        instance_ip="127.0.0.1",
        instance_port=PORT,
        health_check_url=f"http://localhost:{PORT}/health",
        status_page_url=f"http://localhost:{PORT}/info"
    )

    print(f"NOTIFICATION enregistré sur le port {PORT}")

    yield

    # Arrêt du client Eureka
    await eureka_client.stop_async()
    print("Client Eureka arrêté")


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description="Notification microservice",
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    docs_url="/swagger-ui",
    openapi_url="/v3/api-docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Conserver les routes existantes
app.include_router(notification.router)


# Endpoint Health
@app.get("/health")
def health():
    return {"status": "UP"}


# Endpoint Info
@app.get("/info")
def info():
    return {
        "name": "NOTIFICATION",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT
    )
