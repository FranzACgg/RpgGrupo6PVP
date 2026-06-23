# mapa_cueva.py — Mapa 4: La Cueva
# El cofre 'C' al final del camino central es interactuable (cofres.py)

import random
from config import simbolos_entorno

CUEVA_ALTO  = 45
CUEVA_ANCHO = 50
SIMBOLO_PISO   = "."
SIMBOLO_PARED  = "#"
SIMBOLO_CAMINO = "▓"
SIMBOLO_COFRE  = "C"
SIMBOLOS_DECO  = ["💀", "⛏"]

# Posición fija del cofre (se expone para que jugador.py la use)
POS_COFRE_CUEVA = [CUEVA_ALTO // 2, CUEVA_ANCHO - 2]


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

    f_centro = CUEVA_ALTO // 2
    for c in range(1, CUEVA_ANCHO - 1):
        mapa[f_centro][c] = SIMBOLO_CAMINO

    # Cofre al final del camino
    mapa[POS_COFRE_CUEVA[0]][POS_COFRE_CUEVA[1]] = SIMBOLO_COFRE

    for _ in range(25):
        f = random.randint(1, CUEVA_ALTO - 2)
        c = random.randint(1, CUEVA_ANCHO - 2)
        if mapa[f][c] == SIMBOLO_PISO and f != f_centro:
            mapa[f][c] = random.choice(SIMBOLOS_DECO)

    mapa[f_centro][0] = simbolos_entorno[1]   # O entrada
    return mapa
