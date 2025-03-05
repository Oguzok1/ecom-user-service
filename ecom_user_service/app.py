import fastapi

from ecom_user_service.containers.application import ApplicationContainer
from ecom_user_service.routers.root import router as root_router
from ecom_user_service.routers.v1 import router as v1


def get_container() -> ApplicationContainer:
    return ApplicationContainer()


def create_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    app.container = get_container()
    app.include_router(root_router)
    app.include_router(v1)
    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "ecom_user_service.app:create_app",
        host="localhost",
        port=8001,
    )
