import importlib
import inspect
import pathlib

from .Card import Card

mod_dir = pathlib.Path(__file__).parent

__all__ = ["Card"]

excluded = {"__init__.py", "Card.py"}
moduli = [
    f.stem for f in mod_dir.glob("*.py")
    if f.name.endswith(".py") and f.name not in excluded
]

for mod_name in moduli:
    module = importlib.import_module(f".{mod_name}", package=__name__)

    # Importa solo le classi che:
    # - sono definite in questo modulo (evita import esterni)
    # - sono sottoclassi di Card
    # - NON sono inner class (cioè hanno __module__ uguale a module.__name__)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module.__name__ and issubclass(obj, Card):
            globals()[name] = obj
            __all__.append(name)