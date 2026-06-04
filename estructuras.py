# estructuras.py — Estructuras genéricas reutilizables en cualquier mapa

import random
from config import (
    MAPA_REAL_ALTO,
    MAPA_REAL_ANCHO,
    simbolos_entorno,
    simbolos_entornos_no_remplazables,
    simbolos_especiales,
)


def generar_cueva(mapa, f_inicio, c_inicio, ancho, alto):
    """Dibuja una cueva rectangular con paredes '#' y piso '.'."""
    f_fin = f_inicio + alto
    c_fin = c_inicio + ancho

    for f in range(f_inicio, f_fin + 1):
        for c in range(c_inicio, c_fin + 1):
            if 0 <= f < MAPA_REAL_ALTO and 0 <= c < MAPA_REAL_ANCHO:
                if f == f_inicio or f == f_fin or c == c_inicio or c == c_fin:
                    # Entrada en el centro de la pared izquierda
                    if c == c_inicio and f == f_inicio + (alto // 2):
                        mapa[f][c] = simbolos_entorno[1]  # O
                    else:
                        mapa[f][c] = simbolos_entorno[2]  # #
                else:
                    mapa[f][c] = simbolos_entorno[4]  # .


def generar_casa_destruida(mapa, f_inicio, c_inicio, ancho, alto):
    """Dibuja una casa destruida con paredes de tronco '=' y piso '.'."""
    f_fin = f_inicio + alto
    c_fin = c_inicio + ancho

    for f in range(f_inicio, f_fin + 1):
        for c in range(c_inicio, c_fin + 1):
            if 0 <= f < MAPA_REAL_ALTO and 0 <= c < MAPA_REAL_ANCHO:
                if f == f_inicio or f == f_fin or c == c_inicio or c == c_fin:
                    if c == c_inicio and f == f_inicio + (alto // 2):
                        mapa[f][c] = simbolos_entorno[1]  # O entrada
                    else:
                        mapa[f][c] = simbolos_entornos_no_remplazables[
                            3
                        ]  # = tronco
                else:
                    mapa[f][c] = simbolos_entorno[4]  # . piso


def generar_lago(mapa, f_inicio, c_inicio, ancho, alto):
    """Dibuja un lago rectangular con olas aleatorias ('≈' / '~')."""
    f_fin = f_inicio + alto
    c_fin = c_inicio + ancho

    for f in range(f_inicio, f_fin + 1):
        for c in range(c_inicio, c_fin + 1):
            if 0 <= f < MAPA_REAL_ALTO and 0 <= c < MAPA_REAL_ANCHO:
                mapa[f][c] = simbolos_entornos_no_remplazables[
                    random.randint(6, 7)
                ]


def generar_caminos_principales(mapa):
    """Cruz central de caminos con entradas 'O' en los 4 extremos."""
    f_centro = MAPA_REAL_ALTO // 2
    c_centro = MAPA_REAL_ANCHO // 2

    for c in range(MAPA_REAL_ANCHO):
        mapa[f_centro][c] = simbolos_entornos_no_remplazables[5]  # ░

    for f in range(MAPA_REAL_ALTO):
        mapa[f][c_centro] = simbolos_entornos_no_remplazables[5]  # ░

    entradas = [
        (f_centro, 0),
        (f_centro, MAPA_REAL_ANCHO - 1),
        (0, c_centro),
        (MAPA_REAL_ALTO - 1, c_centro),
    ]
    for f, c in entradas:
        mapa[f][c] = simbolos_entorno[1]  # O


def elementos_decorativos(mapa):
    """Siembra flores, troncos y rocas aleatorias en el mapa."""
    cantidades = [
        (30, 0),  # ✿
        (30, 1),  # ❀
        (30, 2),  # ⚜
        (5, 3),  # =
        (8, 4),  # 🪨
    ]
    for cantidad, indice in cantidades:
        for _ in range(cantidad):
            f = random.randint(1, MAPA_REAL_ALTO - 2)
            c = random.randint(1, MAPA_REAL_ANCHO - 2)
            mapa[f][c] = simbolos_entornos_no_remplazables[indice]


def elementos_interactuables(mapa):
    """Coloca 7 ítems '*' en posiciones aleatorias."""
    for _ in range(7):
        f = random.randint(1, MAPA_REAL_ALTO - 2)
        c = random.randint(1, MAPA_REAL_ANCHO - 2)
        mapa[f][c] = simbolos_especiales[1]  # *
