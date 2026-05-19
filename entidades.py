# entidades.py — Mobs: Slimes y futuros enemigos

import random
from config import (
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    simbolos_pasto, simbolo_slime,
)


# ─── Estado de los slimes ─────────────────────────────────────────────────────
# Cada entrada: {"pos": [fila, col], "debajo": símbolo_que_pisaba}
lista_slimes = [
    {"pos": [40, 20],  "debajo": "."},
    {"pos": [50, 60],  "debajo": ","},
    {"pos": [30, 100], "debajo": "░"},
]


def inicializar_slimes(mapa):
    """Dibuja los slimes en su posición inicial en el mapa dado."""
    for slime in lista_slimes:
        f, c = slime["pos"]
        mapa[f][c] = simbolo_slime


def mover_slimes(mapa):
    """
    Mueve cada slime una celda al azar (o lo deja quieto).
    Solo se mueve si la celda destino es pasto o camino '░'.
    """
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]

    for slime in lista_slimes:
        f, c = slime["pos"]
        df, dc = random.choice(direcciones)
        nf, nc = f + df, c + dc

        if 0 <= nf < MAPA_REAL_ALTO and 0 <= nc < MAPA_REAL_ANCHO:
            celda_destino = mapa[nf][nc]

            if celda_destino in simbolos_pasto or celda_destino == "░":
                # Restaurar la celda anterior
                mapa[f][c] = slime["debajo"]

                # Guardar lo que hay en la nueva celda
                slime["debajo"] = celda_destino
                slime["pos"]    = [nf, nc]

                # Dibujar el slime
                mapa[nf][nc] = simbolo_slime
