# mapa_cueva.py — Mapa 4: La Cueva

import random
from config import simbolos_entorno

CUEVA_ALTO  = 45
CUEVA_ANCHO = 50
SIMBOLO_PISO   = "."
SIMBOLO_PARED  = "#"
SIMBOLO_CAMINO = "▓"
SIMBOLO_COFRE  = "C"
SIMBOLO_GOBLIN = "G"
SIMBOLOS_DECO  = ["💀", "⛏"]


def generar_mapa_cueva():
    mapa = []
    for f in range(CUEVA_ALTO):
        fila = []
        for c in range(CUEVA_ANCHO):
            if f == 0 or f == CUEVA_ALTO - 1 or c == 0 or c == CUEVA_ANCHO - 1:
                fila.append(SIMBOLO_PARED)
            else:
                fila.append(SIMBOLO_PISO)
        mapa.append(fila)

    # Camino central
    f_centro = CUEVA_ALTO // 2
    for c in range(1, CUEVA_ANCHO - 1):
        mapa[f_centro][c] = SIMBOLO_CAMINO
    mapa[f_centro][CUEVA_ANCHO - 2] = SIMBOLO_COFRE

    # Decoración
    for _ in range(25):
        f = random.randint(1, CUEVA_ALTO - 2)
        c = random.randint(1, CUEVA_ANCHO - 2)
        if mapa[f][c] == SIMBOLO_PISO and f != f_centro:
            mapa[f][c] = random.choice(SIMBOLOS_DECO)

    # Entrada
    mapa[f_centro][0] = simbolos_entorno[1]   # O

    return mapa
