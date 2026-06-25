import json
import os
import random

RUTA_ACTUAL = os.path.dirname(__file__)
RUTA_ITEMS = os.path.join(RUTA_ACTUAL, "datos", "items.json")

_catalogo = []


def cargar_catalogo():
    """
    Objetivo: cargar el catalogo de items desde datos/items.json a la variable
        del modulo. Se llama una vez al arrancar el juego. Si el archivo no
        existe o esta mal formado, lanza la excepcion para no seguir con un
        catalogo roto.
    Salida: none. Llena la lista interna _catalogo
    """
    try:
        with open(RUTA_ITEMS, "rt", encoding="utf-8") as archivo_items:
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
    """
    Objetivo: elegir un item al azar del catalogo (loot)
    Salida: Diccionario. Devuelve una copia para que quien lo reciba no
        modifique el item original del catalogo
    """
    item = random.choice(_catalogo)
    return item.copy()
