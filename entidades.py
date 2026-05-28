# entidades.py — Mobs: Slimes (Prado) y Goblins (Cueva)
#
#  v2: stats_slime() y stats_goblin() ahora retornan dicts completos
#      con hp, fuerza, defensa, agilidad y habilidades.
#      pantalla_batalla.py los lee desde STATS_ENEMIGOS (centralizado allí).

import random
from config import (
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    simbolos_pasto, simbolo_slime, simbolo_goblin,
)

# ─── Slimes del Prado ─────────────────────────────────────────────────────────
lista_slimes = [
    {"pos": [40, 20],  "debajo": ","},
    {"pos": [50, 60],  "debajo": ","},
    {"pos": [30, 100], "debajo": "░"},
]

# ─── Goblins de la Cueva ──────────────────────────────────────────────────────
lista_goblins = []


def stats_slime():
    """
    Retorna el diccionario de stats del Slime.
    Vida: 50 | Fuerza: 10 | Defensa: 5 | Agilidad: 20%
    Habilidades:
      - Disparo Ácido  : doble daño, 30% de probabilidad
      - Cuerpo Ácido   : 20% de destruir un arma equipada
    """
    return {
        "nombre"    : "Slime",
        "hp_max"    : 50,
        "fuerza"    : 10,
        "defensa"   : 5,
        "agilidad"  : 20,
        "habilidades": [
            {
                "nombre"      : "Disparo Ácido",
                "tipo"        : "Ataque",
                "descripcion" : "Hace el doble de daño",
                "valor"       : 2.0,
                "probabilidad": 30,
            },
            {
                "nombre"      : "Cuerpo Ácido",
                "tipo"        : "Maldición",
                "descripcion" : "20% de probabilidad de destruir un arma equipada",
                "valor"       : 0,
                "probabilidad": 20,
            },
        ],
    }


def stats_goblin():
    """
    Retorna el diccionario de stats del Goblin.
    Vida: 100 | Fuerza: 20 | Defensa: 8 | Agilidad: 15%
    Habilidades:
      - Daga Rompe Escudos : reduce a 0 el bonus de defensa del escudo equipado
      - Modo Berserker     : 40% de atacar 2 veces, 20% de atacar 3 veces
    """
    return {
        "nombre"    : "Goblin",
        "hp_max"    : 100,
        "fuerza"    : 20,
        "defensa"   : 8,
        "agilidad"  : 15,
        "habilidades": [
            {
                "nombre"      : "Daga Rompe Escudos",
                "tipo"        : "Maldición",
                "descripcion" : "Reduce a 0 el bono de defensa del escudo equipado",
                "valor"       : 0,
                "probabilidad": 35,
            },
            {
                "nombre"      : "Modo Berserker",
                "tipo"        : "Ataque",
                "descripcion" : "40% de atacar 2 veces, 20% de atacar 3 veces",
                "valor"       : 1.0,
                "probabilidad": 60,
            },
        ],
    }


def inicializar_slimes(mapa):
    """Dibuja los slimes en su posición inicial."""
    for slime in lista_slimes:
        f, c = slime["pos"]
        mapa[f][c] = simbolo_slime


def mover_slimes(mapa):
    """Mueve cada slime una celda al azar (sin pisar al jugador)."""
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]

    for slime in lista_slimes:
        f, c = slime["pos"]
        df, dc = random.choice(direcciones)
        nf, nc = f + df, c + dc

        if not (0 <= nf < MAPA_REAL_ALTO and 0 <= nc < MAPA_REAL_ANCHO):
            continue

        celda_destino = mapa[nf][nc]
        if celda_destino not in simbolos_pasto and celda_destino != "░":
            continue

        mapa[f][c]       = slime["debajo"]
        slime["debajo"]  = celda_destino
        slime["pos"]     = [nf, nc]
        mapa[nf][nc]     = simbolo_slime


def verificar_combate_slime(pos_jugador):
    """Devuelve el slime si el jugador está en la misma celda, None si no."""
    for slime in lista_slimes:
        if slime["pos"] == pos_jugador:
            return slime
    return None


def eliminar_slime(slime, mapa):
    """Elimina un slime del mapa y de la lista tras ser derrotado."""
    f, c = slime["pos"]
    mapa[f][c] = slime["debajo"]
    if slime in lista_slimes:
        lista_slimes.remove(slime)


# ─── Goblins (cueva) ──────────────────────────────────────────────────────────
from mapa_cueva import CUEVA_ALTO, CUEVA_ANCHO, SIMBOLO_GOBLIN, SIMBOLO_PISO


def cargar_goblins(lista):
    """Reemplaza la lista de goblins con la generada al crear el mapa cueva."""
    global lista_goblins
    lista_goblins = lista


def mover_goblins(mapa):
    """Mueve goblins en la cueva (igual lógica que slimes)."""
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]

    for goblin in lista_goblins:
        f, c = goblin["pos"]
        df, dc = random.choice(direcciones)
        nf, nc = f + df, c + dc

        if not (0 <= nf < CUEVA_ALTO and 0 <= nc < CUEVA_ANCHO):
            continue

        celda_destino = mapa[nf][nc]
        if celda_destino not in (SIMBOLO_PISO, "▓"):
            continue

        mapa[f][c]        = goblin["debajo"]
        goblin["debajo"]  = celda_destino
        goblin["pos"]     = [nf, nc]
        mapa[nf][nc]      = SIMBOLO_GOBLIN


def verificar_combate_goblin(pos_jugador):
    for g in lista_goblins:
        if g["pos"] == list(pos_jugador):
            return g
    return None


def eliminar_goblin(goblin, mapa):
    f, c = goblin["pos"]
    mapa[f][c] = goblin["debajo"]
    if goblin in lista_goblins:
        lista_goblins.remove(goblin)
