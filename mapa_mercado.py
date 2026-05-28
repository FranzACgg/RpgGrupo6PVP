# mapa_mercado.py — Mapa 1: El Mercado

from config import (
    MAPA_REAL_ALTO,
    MAPA_REAL_ANCHO,
    simbolos_entorno,
)


# ─── Arte ASCII del puesto con NPC ────────────────────────────────────────────
ARTE_PUESTO_NPC = [
    "┌─────┐",
    "│▒▒▒▒▒│",
    "│▒ N ▒│",
    "│[===]│",
    "└─────┘",
]


def generar_puesto_con_npc(mapa, f, c):
    """
    Dibuja el arte ASCII del puesto NPC en la posición (f, c),
    que corresponde a la esquina superior-izquierda del puesto.
    """
    for i, fila in enumerate(ARTE_PUESTO_NPC):
        for j, caracter in enumerate(fila):
            if 0 <= f + i < MAPA_REAL_ALTO and 0 <= c + j < MAPA_REAL_ANCHO:
                mapa[f + i][c + j] = caracter


def _generar_bordes_y_salidas(mapa):
    """Dibuja las paredes '▒' del perímetro y las salidas 'O'."""
    for f in range(MAPA_REAL_ALTO):
        for c in range(MAPA_REAL_ANCHO):
            if (
                f == 0
                or f == MAPA_REAL_ALTO - 1
                or c == 0
                or c == MAPA_REAL_ANCHO - 1
            ):
                mapa[f][c] = "▒"

    # Salidas del mercado
    mapa[30][129] = simbolos_entorno[1]  # O derecha  → regresa al Prado
    mapa[0][52] = simbolos_entorno[1]  # O arriba


def _generar_calles(mapa):
    """Dibuja la cuadrícula de calles (2 horizontales × 4 verticales)."""
    filas_h = [MAPA_REAL_ALTO // 3, (MAPA_REAL_ALTO // 3) * 2]
    cols_v = [
        MAPA_REAL_ANCHO // 5,
        (MAPA_REAL_ANCHO // 5) * 2,
        (MAPA_REAL_ANCHO // 5) * 3,
        (MAPA_REAL_ANCHO // 5) * 4,
    ]

    # Puestos a ambos lados de cada calle horizontal
    for f_calle in filas_h:
        for c_pos in range(2, MAPA_REAL_ANCHO - 8, 8):
            en_cruce = any(c_pos in range(cv - 2, cv + 2) for cv in cols_v)
            if not en_cruce:
                generar_puesto_con_npc(
                    mapa, f_calle - 5, c_pos
                )  # fila de arriba
                generar_puesto_con_npc(
                    mapa, f_calle + 1, c_pos
                )  # fila de abajo

    # Calles horizontales (encima de los puestos para limpiar solapamientos)
    for f in filas_h:
        for c in range(1, MAPA_REAL_ANCHO - 1):
            mapa[f][c] = "░"

    # Calles verticales
    for c in cols_v:
        for f in range(1, MAPA_REAL_ALTO - 1):
            mapa[f][c] = "░"


def generar_mapa_mercado_total():
    """
    Genera y devuelve la matriz del Mercado (mapa 1).

    Contenido:
      - Suelo base vacío
      - Paredes '▒' perimetrales con salidas 'O'
      - Cuadrícula de calles '░' (2H × 4V)
      - Puestos con NPC a ambos lados de cada calle horizontal
    """
    mapa = [
        [simbolos_entorno[0] for _ in range(MAPA_REAL_ANCHO)]
        for _ in range(MAPA_REAL_ALTO)
    ]

    _generar_bordes_y_salidas(mapa)
    _generar_calles(mapa)

    return mapa
