import uvicorn
from fastapi import FastAPI


def init_middlewares(app: FastAPI) -> None:
    # app.add_middleware()
    pass


def init_routers(app: FastAPI) -> None:
    # app.include_router()
    pass


def build_fastapi_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI",
        description="",
        version="0.1.0",
    ) # TODO: load from config

    init_middlewares(app)

    return app


if __name__ == "__main__":
    app: FastAPI = build_fastapi_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)  # TODO: from config
