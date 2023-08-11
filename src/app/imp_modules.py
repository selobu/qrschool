# coding: utf-8
__all__ = ["modulesResolver"]
import pkgutil
import importlib
from app import modules


def _import_submodules(module, item="model"):
    """Import all submodules of a module, recursively."""
    res = []
    for loader, module_name, is_pkg in pkgutil.walk_packages(
        module.__path__, module.__name__ + "."
    ):
        if is_pkg:
            try:
                importlib.import_module(f"{module_name}.{item}")
            except Exception as e:
                print(e)
                print(f"No se pudo importar  {module_name}.{item}")
            res.append(module_name.split(".")[-1])
    return res


def modulesResolver(app, enabled_modules=None, **kwargs):
    enabled_modules = _import_submodules(modules, "model")
    # Import router endpoints
    for module_name in enabled_modules:
        try:
            route = importlib.import_module(
                f"app.modules.{module_name}.routes", package=__name__
            )
        except ModuleNotFoundError as e:
            print(f"-> No se pudo importar  app.{module_name}.routes")
            print(e)
        if False:
            for element in dir(route):
                attr = getattr(route, element)
                if isinstance(attr, app.api):
                    app.include_router(attr)
