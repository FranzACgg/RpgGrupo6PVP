import json
import os
import random


RUTA_ACTUAL = os.path.dirname(__file__)
RUTA_ITEMS = os.path.join(RUTA_ACTUAL, "datos", "items.json")

_catalogo = []


def cargar_catalogo():
    try:
        with open(RUTA_ITEMS, "rt") as archivo_items:
            datos_items = json.load(archivo_items)
            _catalogo.clear()
            _catalogo.extend(datos_items)
    except FileNotFoundError as e:
        print(e)
        raise
    except json.JSONDecodeError as e:
        print(e)
        raise


def item_aleatorio():
    item = random.choice(_catalogo)
    return item.copy()
