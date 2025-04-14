import os
import importlib

moduli = []

package = __name__

for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".py") and file != "__init__.py" and file != "Card.py":
        print(file)
        modulo = file[:-3]
        mod = importlib.import_module(f".{modulo}", package=package)
        moduli.append(mod)