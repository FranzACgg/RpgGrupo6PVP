# entidades.py — Mobs y enemies del mapa

import random
from config import (
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    simbolos_pasto, simbolo_slime, simbolo_goblin,
)

STATS_ENEMIGOS = {
    "slime": {
        "nombre":   "Slime",
        "simbolo":  simbolo_slime,
        "hp_max":   50,
        "fuerza":   35,
        "defensa":   5,
        "agilidad": 20,
        "habilidades": [
            {"nombre": "Disparo Ácido", "tipo": "Ataque",    "valor": 2.0, "probabilidad": 30},
            {"nombre": "Cuerpo Ácido",  "tipo": "Maldición", "valor": 0,   "probabilidad": 20},
        ],
    },
    "goblin": {
        "nombre":   "Goblin",
        "simbolo":  simbolo_goblin,
        "hp_max":   80,
        "fuerza":   40,
        "defensa":   8,
        "agilidad": 15,
        "habilidades": [
            {"nombre": "Daga Rompe Escudos", "tipo": "Maldición", "valor": 0,   "probabilidad": 35},
            {"nombre": "Modo Berserker",     "tipo": "Ataque",    "valor": 1.0, "probabilidad": 60},
        ],
    },
    "jefe": {
        "nombre":   "El Campeón",
        "simbolo":  "J",
        "hp_max":   200,
        "fuerza":   55,
        "defensa":  20,
        "agilidad": 25,
        "habilidades": [
            {"nombre": "Golpe Devastador", "tipo": "Ataque",    "valor": 2.0, "probabilidad": 40},
            {"nombre": "Torbellino",       "tipo": "Ataque",    "valor": 1.5, "probabilidad": 30},
            {"nombre": "Grito de Arena",   "tipo": "Maldición", "valor": 0,   "probabilidad": 25},
        ],
    },
}


def generar_enemigos_prado():
    """
    Objetivo: armar la lista de slimes del prado, cada uno con su posicion y su
        HP inicial
    Salida: Lista de diccionarios de enemigos
    """
    hp = STATS_ENEMIGOS["slime"]["hp_max"]
    return [
        {"tipo": "slime", "pos": [40, 20],  "debajo": ",", "hp_actual": hp},
        {"tipo": "slime", "pos": [50, 60],  "debajo": ",", "hp_actual": hp},
        {"tipo": "slime", "pos": [30, 100], "debajo": "░", "hp_actual": hp},
        {"tipo": "slime", "pos": [15, 30],  "debajo": ",", "hp_actual": hp},
        {"tipo": "slime", "pos": [20, 75],  "debajo": ";", "hp_actual": hp},
        {"tipo": "slime", "pos": [35, 45],  "debajo": "'", "hp_actual": hp},
        {"tipo": "slime", "pos": [65, 90],  "debajo": ",", "hp_actual": hp},
        {"tipo": "slime", "pos": [70, 115], "debajo": ";", "hp_actual": hp},
    ]


def generar_enemigos_cueva():
    """
    Objetivo: armar la lista de goblins de la cueva, cada uno con su posicion y
        su HP inicial
    Salida: Lista de diccionarios de enemigos
    """
    hp = STATS_ENEMIGOS["goblin"]["hp_max"]
    return [
        {"tipo": "goblin", "pos": [10, 10], "debajo": ".", "hp_actual": hp},
        {"tipo": "goblin", "pos": [20, 35], "debajo": ".", "hp_actual": hp},
        {"tipo": "goblin", "pos": [30, 20], "debajo": ".", "hp_actual": hp},
        {"tipo": "goblin", "pos": [15, 45], "debajo": ".", "hp_actual": hp},
    ]


def generar_enemigo_coliseo():
    """
    En el coliseo ya no hay un jefe estático en el mapa —
    la batalla de rivales se dispara automáticamente al entrar.
    Devuelve lista vacía: el mapa solo tiene la arena.
    """
    return []


def inicializar_enemigos(mapa, contexto):
    """
    Entrada: Lista de listas (mapa), Diccionario (contexto)
    Objetivo: dibujar en el mapa el simbolo de cada enemigo segun su posicion
    Salida: none. Modifica el mapa
    """
    for en in contexto["mundo"]["enemigos"]:
        f, c = en["pos"]
        simbolo = STATS_ENEMIGOS[en["tipo"]]["simbolo"]
        mapa[f][c] = simbolo


def mover_enemigos(mapa, contexto):
    """
    Entrada: Lista de listas (mapa), Diccionario (contexto)
    Objetivo: mover cada enemigo a una celda libre vecina al azar, actualizando
        el mapa y lo que queda debajo
    Salida: none. Modifica el mapa y las posiciones de los enemigos
    """
    alto  = contexto["mundo"]["dim_alto"]
    ancho = contexto["mundo"]["dim_ancho"]
    dirs  = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
    celdas_libres = simbolos_pasto + ["░", "▓", "."]

    for en in contexto["mundo"]["enemigos"]:
        f, c   = en["pos"]
        df, dc = random.choice(dirs)
        nf, nc = f + df, c + dc
        if not (0 <= nf < alto and 0 <= nc < ancho):
            continue
        celda = mapa[nf][nc]
        if celda not in celdas_libres:
            continue
        mapa[f][c]   = en["debajo"]
        en["debajo"] = celda
        en["pos"]    = [nf, nc]
        mapa[nf][nc] = STATS_ENEMIGOS[en["tipo"]]["simbolo"]


def buscar_enemigo_en(pos, contexto):
    """
    Entrada: Lista [fila, col] (pos), Diccionario (contexto)
    Objetivo: buscar si hay un enemigo en esa posicion
    Salida: el diccionario del enemigo si lo encuentra, None si no
    """
    for en in contexto["mundo"]["enemigos"]:
        if en["pos"] == list(pos):
            return en
    return None


def eliminar_enemigo(enemigo, mapa, contexto):
    """
    Entrada: Diccionario (enemigo), Lista de listas (mapa), Diccionario (contexto)
    Objetivo: sacar al enemigo del mapa y de la lista, y darle al jugador el
        item que dropea segun su tipo
    Salida: none. Modifica el mapa, la lista de enemigos y el inventario
    """
    f, c = enemigo["pos"]
    mapa[f][c] = enemigo["debajo"]
    if enemigo in contexto["mundo"]["enemigos"]:
        contexto["mundo"]["enemigos"].remove(enemigo)

    from inventario import agregar_item
    drops = {
        "slime":  {"id_item": 51, "nombre": "Baba de Slime",
                   "tipo": "consumible", "cantidad": 1, "equipado": False},
        "goblin": {"id_item": 52, "nombre": "Cabeza de Goblin",
                   "tipo": "clave", "cantidad": 1, "equipado": False},
    }
    if enemigo["tipo"] in drops:
        agregar_item(drops[enemigo["tipo"]], contexto["inventario"])
