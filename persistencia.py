import os
import json

RUTA_ACTUAL = os.path.dirname(__file__)
RUTA_PARTIDA = os.path.join(RUTA_ACTUAL, "partidas", "partida.json")
RUTA_PROGRESO = os.path.join(RUTA_ACTUAL, "partidas", "progreso.json")
PROGRESO_DEFAULT = {"clase_oculta_desbloqueada": False}


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
    try:
        with open(RUTA_PARTIDA, "rt", encoding="utf-8") as partida:
            contexto = json.load(partida)
        contexto = _deserializar_contexto(contexto)
        return contexto
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def existe_partida_guardada():
    return os.path.exists(RUTA_PARTIDA)


def borrar_partida():
    try:
        os.remove(RUTA_PARTIDA)
        return True
    except FileNotFoundError:
        return True


def guardar_progreso(progreso):
    try:
        with open(RUTA_PROGRESO, "wt", encoding="utf-8") as progreso_json:
            json.dump(progreso, progreso_json, indent=4)
        return True
    except IOError:
        return False


def cargar_progreso():
    try:
        with open(RUTA_PROGRESO, "rt", encoding="utf-8") as progreso_json:
            progreso = json.load(progreso_json)
        return progreso
    except FileNotFoundError:
        return PROGRESO_DEFAULT.copy()
