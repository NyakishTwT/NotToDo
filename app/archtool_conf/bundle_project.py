import pathlib
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from archtool.dependency_injector import DependencyInjector
from web_fractal.building_utils import import_all_models, initialize_controllers_api
from sqlalchemy.pool import NullPool
import app.config as settings
from app.archtool_conf.custom_layers import APPS, app_layers
from web_fractal.db import Base


def bundle(app: FastAPI) -> DependencyInjector:
    backend_root = pathlib.Path(__file__).resolve().parents[2]

    injector = DependencyInjector(
        modules_list=APPS, layers=app_layers, project_root=backend_root
    )
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )
    session_maker = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    injector.register(key=AsyncEngine, value=engine, inject_into=False)
    injector.register(key=async_sessionmaker, value=session_maker, inject_into=False)

    import_all_models(Base=Base)

    injector.inject()

    app.state.injector = injector

    initialize_controllers_api(injector=injector, app=app)

    @app.on_event("startup")
    async def _create_tables() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return injector
