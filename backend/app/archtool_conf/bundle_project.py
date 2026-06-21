import pathlib
from fastapi import FastAPI
from archtool.dependency_injector import DependencyInjector
from web_fractal.building_utils import import_all_models, initialize_controllers_api
from app.archtool_conf.custom_layers import APPS, app_layers
from web_fractal.db import Base
from app.core_integrations.reg_deps import reg_deps

BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[1]


def bundle(app: FastAPI) -> DependencyInjector:

    injector = DependencyInjector(
        modules_list=APPS, layers=app_layers, project_root=BACKEND_ROOT
    )
    reg_deps(injector)
    import_all_models(Base=Base)
    injector.inject()

    # Универсальная доинъекция для обхода бага archtool 2.1.1
    for instance in injector.dependencies.values():
        cls = type(instance)
        if not hasattr(cls, "__annotations__"):
            continue
        for attr_name, attr_type in cls.__annotations__.items():
            if hasattr(instance, attr_name):
                continue
            try:
                dep = injector.get_dependency(attr_type)
                setattr(instance, attr_name, dep)
            except Exception:
                pass

    # web_fractal==0.0.1 still reads the pre-2.0 private attribute name;
    # archtool>=2.0 renamed it to the public `dependencies`. Bridge until
    # web_fractal catches up.
    injector._dependencies = injector.dependencies
    initialize_controllers_api(injector=injector, app=app)
    return injector
