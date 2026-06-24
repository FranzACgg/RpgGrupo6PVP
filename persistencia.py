import os
import json

RUTA_ACTUAL = os.path.dirname(__file__)
RUTA_PARTIDA = os.path.join(RUTA_ACTUAL, "partidas", "partida.json")
RUTA_PROGRESO = os.path.join(RUTA_ACTUAL, "partidas", "progreso.json")


def _serializar_contexto(contexto):
    copia = contexto.copy()
    copia["progreso"] = contexto["progreso"].copy()
    copia["progreso"]["enemigos_derrotados"] = list(
        contexto["progreso"]["enemigos_derrotados"]
    )
    return copia


def _deserializar_contexto(datos):
    datos["progreso"]["enemigos_derrotados"] = set(
        datos["progreso"]["enemigos_derrotados"]
    )
    return datos


def guardar_partida(contexto):
    try:
        with open(RUTA_PARTIDA, "wt", encoding="utf-8") as partida:
            copia = _serializar_contexto(contexto)
            json.dump(copia, partida, indent=4)
        return True
    except IOError:
        return False


def cargar_partida():
    contexto = {}
    try:
        with open(RUTA_PARTIDA, "rt") as partida:
            json.load(contexto, partida)
        copia = _deserializar_contexto(contexto)
        return copia
    except FileNotFoundError:
        pass


def existe_partida_guardada():
    return os.path.exists(RUTA_PARTIDA)


def borrar_partida():
    try:
        os.remove(RUTA_PARTIDA)
    except FileNotFoundError:
        pass


def guardar_progreso(progreso):
    try:
        with open(RUTA_PROGRESO, "wt") as progreso:
            pass
    except FileNotFoundError:
        pass


def cargar_progreso():
    try:
        with open(RUTA_PROGRESO, "rt") as progreso:
            pass
    except FileNotFoundError:
        pass
