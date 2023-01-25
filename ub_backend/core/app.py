from fastapi import FastAPI

from .config import app_config


def init_middlewares(app: FastAPI) -> None:
    # app.add_middleware()
    pass


def init_routes(app: FastAPI) -> None:
    from ub_backend.api.routes import v1_router
    app.include_router(prefix="/api", router=v1_router)


def build_fastapi_app() -> FastAPI:
    app = FastAPI(
        title=app_config.profile.title,
        description=app_config.profile.description,
        version=app_config.profile.version,
    )

    init_middlewares(app)
    init_routes(app)
    
    return app


if __name__ == "__main__":
    import uvicorn

    app: FastAPI = build_fastapi_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)  # TODO: from config
