# mapa_prado.py — Mapa 2: El Prado

import random
from config import (
    MAPA_REAL_ALTO,
    MAPA_REAL_ANCHO,
    simbolos_entorno,
    simbolos_pasto,
    simbolos_especiales,
)
from estructuras import (
    generar_cueva,
    generar_casa_destruida,
    generar_lago,
    generar_caminos_principales,
    elementos_decorativos,
    elementos_interactuables,
)


def generar_enemigos_prado():
    return [
        {"tipo": "slime", "pos": [40, 20], "debajo": "."},
        {"tipo": "slime", "pos": [50, 60], "debajo": ","},
        {"tipo": "slime", "pos": [30, 100], "debajo": "░"},
    ]


def generar_mapa_prado():
    """
    Genera y devuelve la matriz del Prado (mapa 2).

    Contenido:
      - Suelo de pasto aleatorio
      - Borde de tréboles '♣'
      - Cruz de caminos centrales con entradas 'O'
      - 1 cueva (esquina superior-izquierda)
      - 1 casa destruida (esquina superior-derecha)
      - 1 lago (zona inferior-izquierda)
      - Flores, rocas y otros decorativos
      - 7 ítems '*' recogibles
    """
    # 1. Base: todo vacío
    mapa = [
        [simbolos_entorno[0] for _ in range(MAPA_REAL_ANCHO)]
        for _ in range(MAPA_REAL_ALTO)
    ]

    # 2. Borde de tréboles y relleno de pasto
    for f in range(MAPA_REAL_ALTO):
        for c in range(MAPA_REAL_ANCHO):
            if (
                f == 0
                or f == MAPA_REAL_ALTO - 1
                or c == 0
                or c == MAPA_REAL_ANCHO - 1
            ):
                mapa[f][c] = simbolos_entorno[3]  # ♣
            elif mapa[f][c] == simbolos_entorno[0]:
                mapa[f][c] = random.choice(simbolos_pasto)

    # 3. Ítems y decoración
    elementos_interactuables(mapa)
    elementos_decorativos(mapa)

    # 4. Caminos centrales con entradas
    generar_caminos_principales(mapa)

    # 5. Posición inicial del jugador
    mapa[1][52] = simbolos_especiales[0]  # P

    # 6. Estructuras
    generar_cueva(mapa, 10, 10, 6, 4)
    generar_casa_destruida(mapa, 11, 90, 15, 10)
    generar_lago(mapa, 60, 20, 15, 20)

    return mapa
