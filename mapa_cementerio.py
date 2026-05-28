# mapa_cementerio.py — Mapa 3: El Cementerio
# FIX: valla perimetral cambiada de '🚧' (emoji incompatible) a '+' ASCII

import random
from config import (
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    simbolos_entorno, simbolos_pasto,
)

SIMBOLO_VALLA = "+"   # ASCII puro — compatible con cualquier terminal

ARTE_ENTRADA = [
    " ┌─────┐ ",
    " │📜📜📜│ ",
    " │░░░░░│ ",
]


def _dibujar_valla_y_entrada_jugador(mapa):
    """Valla '+' perimetral y entrada 'O' para el jugador."""
    for f in range(2, MAPA_REAL_ALTO - 2):
        for c in range(2, MAPA_REAL_ANCHO - 2):
            if f == 2 or f == MAPA_REAL_ALTO - 3 or c == 2 or c == MAPA_REAL_ANCHO - 3:
                mapa[f][c] = SIMBOLO_VALLA

    mapa[86][73] = simbolos_entorno[1]   # O — entrada desde el Prado


def _dibujar_senderos(mapa):
    filas_h = [MAPA_REAL_ALTO // 3, (MAPA_REAL_ALTO // 3) * 2]
    cols_v  = [MAPA_REAL_ANCHO // 4, MAPA_REAL_ANCHO // 2, (MAPA_REAL_ANCHO // 4) * 3]

    for f in filas_h:
        for c in range(3, MAPA_REAL_ANCHO - 3):
            mapa[f][c]     = "▒"
            mapa[f + 1][c] = "▒"

    for c in cols_v:
        for f in range(3, MAPA_REAL_ALTO - 3):
            mapa[f][c]     = "▒"
            mapa[f][c + 1] = "▒"


def _sembrar_tumbas_y_arboles(mapa):
    for f in range(4, MAPA_REAL_ALTO - 4):
        for c in range(4, MAPA_REAL_ANCHO - 4):
            if mapa[f][c] not in simbolos_pasto:
                continue
            hay_camino = any(
                mapa[f + df][c + dc] == "▒"
                for df in range(-2, 3)
                for dc in range(-2, 3)
                if 0 <= f + df < MAPA_REAL_ALTO and 0 <= c + dc < MAPA_REAL_ANCHO
            )
            if hay_camino:
                prob = random.random()
                if   prob < 0.15: mapa[f][c] = "🪦"
                elif prob < 0.18: mapa[f][c] = "🗿"
                elif prob < 0.23: mapa[f][c] = "🌲"


def _dibujar_arco_entrada(mapa):
    f_entrada = MAPA_REAL_ALTO - 3
    c_entrada = MAPA_REAL_ANCHO // 2
    for i, fila in enumerate(ARTE_ENTRADA):
        for j, char in enumerate(fila):
            mapa[f_entrada - 2 + i][c_entrada - 4 + j] = char


def _colocar_farolas(mapa):
    for pos_f in [1, MAPA_REAL_ALTO - 1]:
        for pos_c in range(10, MAPA_REAL_ANCHO - 10, 20):
            mapa[pos_f][pos_c] = "🏮"


def generar_mapa_cementerio():
    mapa = [
        [random.choice(simbolos_pasto) for _ in range(MAPA_REAL_ANCHO)]
        for _ in range(MAPA_REAL_ALTO)
    ]
    _dibujar_valla_y_entrada_jugador(mapa)
    _dibujar_senderos(mapa)
    _sembrar_tumbas_y_arboles(mapa)
    _dibujar_arco_entrada(mapa)
    _colocar_farolas(mapa)
    return mapa
