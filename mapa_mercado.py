# mapa_mercado.py — Mapa 1: El Mercado
#
# FIX: el jugador aparece arriba (fila 1, col central) pisando un camino '░'
# FIX: las tiendas ya no quedan entrecortadas por el camino —
#      se colocan DESPUÉS de trazar las calles, en espacios libres entre columnas verticales

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
PUESTO_ALTO  = len(ARTE_PUESTO_NPC)       # 5
PUESTO_ANCHO = len(ARTE_PUESTO_NPC[0])    # 7


def generar_puesto_con_npc(mapa, f, c):
    for i, fila in enumerate(ARTE_PUESTO_NPC):
        for j, caracter in enumerate(fila):
            if 0 <= f + i < MAPA_REAL_ALTO and 0 <= c + j < MAPA_REAL_ANCHO:
                mapa[f + i][c + j] = caracter


def _generar_bordes_y_salidas(mapa):
    """Paredes '▒' perimetrales y salida 'O' derecha → Prado."""
    for f in range(MAPA_REAL_ALTO):
        for c in range(MAPA_REAL_ANCHO):
            if (
                f == 0
                or f == MAPA_REAL_ALTO - 1
                or c == 0
                or c == MAPA_REAL_ANCHO - 1
            ):
                mapa[f][c] = "▒"

    # Salida derecha → Prado
    mapa[30][MAPA_REAL_ANCHO - 1] = simbolos_entorno[1]   # O


def _generar_calles(mapa):
    """
    Traza la cuadrícula de calles '░' PRIMERO,
    luego coloca los puestos en los huecos entre calles verticales
    para que nunca queden partidos.
    """
    # ── Posiciones de calles ──────────────────────────────────────────────────
    filas_h = [MAPA_REAL_ALTO // 3, (MAPA_REAL_ALTO // 3) * 2]   # filas 30 y 60
    cols_v  = [
        MAPA_REAL_ANCHO // 5,
        (MAPA_REAL_ANCHO // 5) * 2,
        (MAPA_REAL_ANCHO // 5) * 3,
        (MAPA_REAL_ANCHO // 5) * 4,
    ]   # cols ~26, 52, 78, 104

    # ── 1. Dibujar calles horizontales y verticales ───────────────────────────
    for f in filas_h:
        for c in range(1, MAPA_REAL_ANCHO - 1):
            mapa[f][c] = "░"

    for c in cols_v:
        for f in range(1, MAPA_REAL_ALTO - 1):
            mapa[f][c] = "░"

    # ── 2. Colocar puestos en bloques entre calles verticales ─────────────────
    # Los bloques horizontales son los espacios entre cols_v (y bordes).
    # Para cada bloque × cada zona (arriba/abajo de cada calle H),
    # colocamos 1 puesto centrado en el bloque, si hay espacio suficiente.

    limites_c = [1] + cols_v + [MAPA_REAL_ANCHO - 1]   # bordes de cada bloque

    for idx in range(len(limites_c) - 1):
        c_ini = limites_c[idx] + 1          # columna inicio del bloque
        c_fin = limites_c[idx + 1] - 1      # columna fin del bloque
        ancho_bloque = c_fin - c_ini

        if ancho_bloque < PUESTO_ANCHO + 2:
            continue   # bloque demasiado estrecho

        c_puesto = c_ini + (ancho_bloque - PUESTO_ANCHO) // 2   # centrado

        for f_calle in filas_h:
            # Zona ARRIBA de la calle: el puesto termina 1 fila antes de la calle
            f_arriba = f_calle - PUESTO_ALTO - 1
            if f_arriba >= 2:
                generar_puesto_con_npc(mapa, f_arriba, c_puesto)

            # Zona ABAJO de la calle: el puesto empieza 1 fila después
            f_abajo = f_calle + 2
            if f_abajo + PUESTO_ALTO <= MAPA_REAL_ALTO - 2:
                generar_puesto_con_npc(mapa, f_abajo, c_puesto)

    # ── 3. Posición inicial del jugador ──────────────────────────────────────
    # Fila 1 (arriba del todo), columna central → pisa un camino '░'
    c_centro = MAPA_REAL_ANCHO // 2
    mapa[1][c_centro] = "░"   # asegurar que haya camino bajo el jugador


def generar_mapa_mercado_total():
    mapa = [
        [simbolos_entorno[0] for _ in range(MAPA_REAL_ANCHO)]
        for _ in range(MAPA_REAL_ALTO)
    ]
    _generar_bordes_y_salidas(mapa)
    _generar_calles(mapa)
    return mapa
