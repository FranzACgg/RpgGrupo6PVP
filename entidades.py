# entidades.py — Mobs: Slimes (Prado) y Goblins (Cueva)
# Toda la info de mobs vive en contexto["mundo"]["enemigos"]
# Cada entrada: {"tipo": "slime"|"goblin", "pos": [f,c], "debajo": char, "hp_actual": int}

# TODO(deuda critica para combate): los enemigos viven en DOS fuentes a la vez:
#   - la lista (contexto["enemigos"]: pos, debajo)
#   - la matriz (simbolo dibujado en mapa_actual)
# Hoy se sincronizan a mano en mover_slimes. Al morir un enemigo hay que sacarlo de AMBOS.
# Decidir fuente unica o sincronizacion prolija antes de implementar combate.

import random
from config import (
<<<<<<< HEAD
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    simbolos_pasto, simbolo_slime, simbolo_goblin,
)

# ─── Stats de referencia (hp_max, fuerza, defensa, agilidad, habilidades) ─────
# pantalla_batalla.py los usa para construir la pelea.
STATS_ENEMIGOS = {
    "slime": {
        "nombre":    "Slime",
        "simbolo":   simbolo_slime,   # ζ
        "hp_max":    50,
        "fuerza":    35,
        "defensa":    5,
        "agilidad":  20,
        "habilidades": [
            {"nombre": "Disparo Ácido", "tipo": "Ataque",    "valor": 2.0, "probabilidad": 30,
             "descripcion": "Doble daño"},
            {"nombre": "Cuerpo Ácido",  "tipo": "Maldición", "valor": 0,   "probabilidad": 20,
             "descripcion": "20% de destruir un arma equipada"},
        ],
    },
    "goblin": {
        "nombre":    "Goblin",
        "simbolo":   simbolo_goblin,  # G
        "hp_max":    80,
        "fuerza":    40,
        "defensa":    8,
        "agilidad":  15,
        "habilidades": [
            {"nombre": "Daga Rompe Escudos", "tipo": "Maldición", "valor": 0,   "probabilidad": 35,
             "descripcion": "Anula el bono de defensa del escudo equipado"},
            {"nombre": "Modo Berserker",     "tipo": "Ataque",    "valor": 1.0, "probabilidad": 60,
             "descripcion": "40% de atacar 2 veces, 20% de atacar 3 veces"},
        ],
    },
    "jefe": {
        "nombre":    "El Campeón",
        "simbolo":   "J",
        "hp_max":    200,
        "fuerza":    55,
        "defensa":   20,
        "agilidad":  25,
        "habilidades": [
            {"nombre": "Golpe Devastador", "tipo": "Ataque",    "valor": 2.0,  "probabilidad": 40,
             "descripcion": "El doble del daño normal"},
            {"nombre": "Torbellino",       "tipo": "Ataque",    "valor": 1.5,  "probabilidad": 30,
             "descripcion": "Ataca 3 veces con daño reducido"},
            {"nombre": "Grito de Arena",   "tipo": "Maldición", "valor": 0,    "probabilidad": 25,
             "descripcion": "Rompe el escudo del jugador"},
        ],
    },
}


def generar_enemigos_prado():
    """Devuelve la lista inicial de enemigos del Prado con hp_actual completo."""
    hp = STATS_ENEMIGOS["slime"]["hp_max"]
    return [
        {"tipo": "slime", "pos": [40, 20],  "debajo": ",", "hp_actual": hp},
        {"tipo": "slime", "pos": [50, 60],  "debajo": ",", "hp_actual": hp},
        {"tipo": "slime", "pos": [30, 100], "debajo": "░", "hp_actual": hp},
    ]


def generar_enemigos_cueva():
    """Devuelve la lista inicial de goblins de la Cueva con hp_actual completo."""
    hp = STATS_ENEMIGOS["goblin"]["hp_max"]
    return [
        {"tipo": "goblin", "pos": [10, 10], "debajo": ".", "hp_actual": hp},
        {"tipo": "goblin", "pos": [20, 35], "debajo": ".", "hp_actual": hp},
        {"tipo": "goblin", "pos": [30, 20], "debajo": ".", "hp_actual": hp},
        {"tipo": "goblin", "pos": [15, 45], "debajo": ".", "hp_actual": hp},
    ]


def generar_enemigo_coliseo():
    """Un único jefe en el centro del coliseo."""
    hp = STATS_ENEMIGOS["jefe"]["hp_max"]
    return [
        {"tipo": "jefe", "pos": [25, 40], "debajo": "░", "hp_actual": hp},
    ]


def inicializar_enemigos(mapa, contexto):
    """Dibuja todos los enemigos del contexto en el mapa."""
    for en in contexto["mundo"]["enemigos"]:
        f, c = en["pos"]
        simbolo = STATS_ENEMIGOS[en["tipo"]]["simbolo"]
        mapa[f][c] = simbolo


def mover_enemigos(mapa, contexto):
=======
    MAPA_REAL_ALTO,
    MAPA_REAL_ANCHO,
    simbolos_pasto,
    simbolo_slime,
)


# TODO(refactor): inicializar_slimes ya lee del contexto pero NO está conectada.
# Conectarla al subir de nivel, junto con carga de enemigos, en:
#   - main_mapas.py -> iniciar_mapas()
#   - jugador.py    -> cambio_de_mapa() (al entrar al prado)
# Secuencia correcta al entrar a un mapa con enemigos:
#   1. generar mapa  2. contexto["enemigos"] = generar_enemigos_prado()  3. inicializar_slimes(mapa, contexto)


def inicializar_slimes(mapa, contexto):
    """Dibuja los slimes en su posición inicial en el mapa dado."""
    for slime in contexto["mundo"]["enemigos"]:
        f, c = slime["pos"]
        mapa[f][c] = simbolo_slime  # TODO # usar "tipo": "slime"


# TODO(deuda): el simbolo del enemigo esta fijo (simbolo_slime).
# Deberia salir de slime["tipo"] para soportar otros enemigos (goblins, etc.) sin redibujar mal.


def mover_slimes(mapa, contexto):
>>>>>>> origin/integracion_40
    """
    Mueve cada enemigo una celda al azar.
    No pisa al jugador ('P'), paredes ni otros enemigos.
    """
    alto  = contexto["mundo"]["dim_alto"]
    ancho = contexto["mundo"]["dim_ancho"]
    dirs  = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
    celdas_libres = simbolos_pasto + ["░", "▓", "."]

<<<<<<< HEAD
    for en in contexto["mundo"]["enemigos"]:
        f, c  = en["pos"]
        df, dc = random.choice(dirs)
=======
    for slime in contexto["mundo"]["enemigos"]:
        f, c = slime["pos"]
        df, dc = random.choice(direcciones)
>>>>>>> origin/integracion_40
        nf, nc = f + df, c + dc

        if not (0 <= nf < alto and 0 <= nc < ancho):
            continue

        celda = mapa[nf][nc]
        if celda not in celdas_libres:
            continue

<<<<<<< HEAD
        mapa[f][c]  = en["debajo"]
        en["debajo"] = celda
        en["pos"]    = [nf, nc]
        mapa[nf][nc] = STATS_ENEMIGOS[en["tipo"]]["simbolo"]
=======
                # Guardar lo que hay en la nueva celda
                slime["debajo"] = celda_destino
                slime["pos"] = [nf, nc]
>>>>>>> origin/integracion_40


def buscar_enemigo_en(pos, contexto):
    """Devuelve el primer enemigo en la posición dada, o None."""
    for en in contexto["mundo"]["enemigos"]:
        if en["pos"] == list(pos):
            return en
    return None


def eliminar_enemigo(enemigo, mapa, contexto):
    """Elimina el enemigo del mapa y de la lista de enemigos."""
    f, c = enemigo["pos"]
    mapa[f][c] = enemigo["debajo"]
    if enemigo in contexto["mundo"]["enemigos"]:
        contexto["mundo"]["enemigos"].remove(enemigo)
    contexto["progreso"]["enemigos_derrotados"] += 1
