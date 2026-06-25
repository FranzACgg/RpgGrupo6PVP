# mapa_mercado.py — Mapa 1: El Mercado
# Ahora los puestos tienen aldeanos '@' dentro y cofres 'C' opcionales

from config import (
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    simbolos_entorno,
)
from aldeanos import ALDEANOS_MERCADO, registrar_aldeano, SIMBOLO_ALDEANO
# ALDEANOS_MERCADO tiene 3 de quest + 6 relleno = 9 total

ARTE_PUESTO_NPC = [
    "┌─────┐",
    "│▒▒▒▒▒│",
    "│▒ @ ▒│",   # '@' = aldeano visible dentro del puesto
    "│[───]│",
    "└─────┘",
]
PUESTO_ALTO  = len(ARTE_PUESTO_NPC)
PUESTO_ANCHO = len(ARTE_PUESTO_NPC[0])

# Posiciones de cofres en el mercado (fijas, entre los puestos)
_COFRES_MERCADO = []   # se llena al generar el mapa


def get_cofres_mercado():
    return list(_COFRES_MERCADO)


def _generar_bordes_y_salidas(mapa):
    for f in range(MAPA_REAL_ALTO):
        for c in range(MAPA_REAL_ANCHO):
            if f == 0 or f == MAPA_REAL_ALTO - 1 or c == 0 or c == MAPA_REAL_ANCHO - 1:
                mapa[f][c] = "▒"
    mapa[30][MAPA_REAL_ANCHO - 1] = simbolos_entorno[1]   # O derecha → Prado


def _generar_calles(mapa, posiciones_aldeanos):
    filas_h = [MAPA_REAL_ALTO // 3, (MAPA_REAL_ALTO // 3) * 2]
    cols_v  = [
        MAPA_REAL_ANCHO // 5,
        (MAPA_REAL_ANCHO // 5) * 2,
        (MAPA_REAL_ANCHO // 5) * 3,
        (MAPA_REAL_ANCHO // 5) * 4,
    ]

    for f in filas_h:
        for c in range(1, MAPA_REAL_ANCHO - 1):
            mapa[f][c] = "░"
    for c in cols_v:
        for f in range(1, MAPA_REAL_ALTO - 1):
            mapa[f][c] = "░"

    limites_c = [1] + cols_v + [MAPA_REAL_ANCHO - 1]
    puesto_idx = 0   # índice para asignar aldeanos a puestos

    for idx in range(len(limites_c) - 1):
        c_ini = limites_c[idx] + 1
        c_fin = limites_c[idx + 1] - 1
        ancho_bloque = c_fin - c_ini
        if ancho_bloque < PUESTO_ANCHO + 2:
            continue

        c_puesto = c_ini + (ancho_bloque - PUESTO_ANCHO) // 2

        for f_calle in filas_h:
            for f_puesto in [f_calle - PUESTO_ALTO - 1, f_calle + 2]:
                if f_puesto < 2:
                    continue
                if f_puesto + PUESTO_ALTO > MAPA_REAL_ALTO - 2:
                    continue

                # Dibujar puesto
                for i, fila_arte in enumerate(ARTE_PUESTO_NPC):
                    for j, char in enumerate(fila_arte):
                        mapa[f_puesto + i][c_puesto + j] = char

                # Registrar posición del aldeano ('@' está en fila 2 del arte)
                f_ald = f_puesto + 2
                c_ald = c_puesto + 3   # columna del '@' dentro del arte
                posiciones_aldeanos.append([f_ald, c_ald])
                puesto_idx += 1

    # Cofre en esquina inferior derecha del mercado
    _COFRES_MERCADO.clear()
    fc, cc = MAPA_REAL_ALTO - 5, MAPA_REAL_ANCHO - 5
    mapa[fc][cc] = "C"
    _COFRES_MERCADO.append([fc, cc])

    # La posición inicial del jugador [1][c_centro] queda con el suelo base " "


def generar_mapa_mercado_total():
    mapa = [
        [simbolos_entorno[0] for _ in range(MAPA_REAL_ANCHO)]
        for _ in range(MAPA_REAL_ALTO)
    ]
    _generar_bordes_y_salidas(mapa)
    posiciones_aldeanos = []
    _generar_calles(mapa, posiciones_aldeanos)

    # Asignar posiciones a los aldeanos y registrarlos
    for i, aldeano in enumerate(ALDEANOS_MERCADO):
        if i < len(posiciones_aldeanos):
            aldeano["pos"] = posiciones_aldeanos[i]
        else:
            aldeano["pos"] = None
        registrar_aldeano(aldeano)

    return mapa
