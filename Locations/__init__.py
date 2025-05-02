import importlib
import inspect
import pathlib
from .Location import Location

mod_dir = pathlib.Path(__file__).parent

__all__ = ["Location"]

excluded = {"__init__.py", "Location.py"}
moduli = [
    f.stem for f in mod_dir.glob("*.py")
    if f.name.endswith(".py") and f.name not in excluded
]

for mod_name in moduli:
    module = importlib.import_module(f".{mod_name}", package=__name__)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module.__name__ and issubclass(obj, Location):
            globals()[name] = obj
            __all__.append(name)