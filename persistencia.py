import os
import json

RUTA_ACTUAL = os.path.dirname(__file__)
RUTA_PARTIDA = os.path.join(RUTA_ACTUAL, "partidas", "partida.json")
RUTA_PROGRESO = os.path.join(RUTA_ACTUAL, "partidas", "progreso.json")
PROGRESO_DEFAULT = {"clase_oculta_desbloqueada": False}


def _serializar_contexto(contexto):
    """
    Entrada: Diccionario (contexto)
    Objetivo: armar una copia del contexto lista para guardar como JSON. JSON
        no soporta sets, asi que el set de enemigos_derrotados se pasa a lista.
        No se toca el contexto original que sigue jugandose.
    Salida: Diccionario copia, JSON-serializable
    """
    copia = contexto.copy()
    copia["progreso"] = contexto["progreso"].copy()
    copia["progreso"]["enemigos_derrotados"] = list(
        contexto["progreso"]["enemigos_derrotados"]
    )
    return copia


def _deserializar_contexto(datos):
    """
    Entrada: Diccionario (datos leidos del JSON)
    Objetivo: reconstruir el contexto al cargar. La lista de enemigos
        derrotados se vuelve a convertir en set. Como datos viene recien
        leido del archivo, se puede modificar directo.
    Salida: Diccionario contexto
    """
    # datos viene de json.load, no hay original que proteger -> mutación deliberada
    datos["progreso"]["enemigos_derrotados"] = set(
        datos["progreso"]["enemigos_derrotados"]
    )
    return datos


def guardar_partida(contexto):
    """
    Entrada: Diccionario (contexto)
    Objetivo: guardar la partida en curso en partidas/partida.json
    Salida: True si se guardo bien, False si hubo error de escritura
    """
    copia = _serializar_contexto(contexto)
    try:
        with open(RUTA_PARTIDA, "wt", encoding="utf-8") as partida:
            json.dump(copia, partida, indent=4)
        return True
    except IOError:
        return False


def cargar_partida():
    """
    Objetivo: cargar la partida guardada desde partidas/partida.json
    Salida: el contexto si existe y es valido, None si no hay save o esta roto
    """
    try:
        with open(RUTA_PARTIDA, "rt", encoding="utf-8") as partida:
            contexto = json.load(partida)
        return _deserializar_contexto(contexto)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def existe_partida_guardada():
    """
    Objetivo: avisar si hay una partida guardada para ofrecer CONTINUAR
    Salida: True si existe el archivo de partida, False si no
    """
    return os.path.exists(RUTA_PARTIDA)


def borrar_partida():
    """
    Objetivo: borrar el save de la partida (al terminar el juego)
    Salida: True. Si el archivo no existia igual devuelve True porque el
        objetivo (que no haya partida) ya esta cumplido
    """
    try:
        os.remove(RUTA_PARTIDA)
        return True
    except FileNotFoundError:
        return True


def guardar_progreso(progreso):
    """
    Entrada: Diccionario (progreso)
    Params:
        progreso: dict plano con el progreso permanente entre partidas
    Objetivo: guardar el progreso en partidas/progreso.json
    Salida: True si se guardo bien, False si hubo error de escritura
    """
    try:
        with open(RUTA_PROGRESO, "wt", encoding="utf-8") as progreso_json:
            json.dump(progreso, progreso_json, indent=4)
        return True
    except IOError:
        return False


def cargar_progreso():
    """
    Objetivo: cargar el progreso permanente. Si todavia no existe (primera
        vez que se juega) devuelve una copia del progreso por defecto.
    Salida: Diccionario con el progreso
    """
    try:
        with open(RUTA_PROGRESO, "rt", encoding="utf-8") as progreso_json:
            return json.load(progreso_json)
    except FileNotFoundError:
        return PROGRESO_DEFAULT.copy()
