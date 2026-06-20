import pathlib, sys


BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

import uvicorn
from fastapi import FastAPI
from app.archtool_conf.bundle_project import bundle
from app.config import settings


def create_app() -> FastAPI:
    application = FastAPI(title="My app")
    bundle(app=application)
    return application


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
