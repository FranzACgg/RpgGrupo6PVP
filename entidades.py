# entidades.py — Mobs: Slimes y futuros enemigos

# TODO(deuda critica para combate): los enemigos viven en DOS fuentes a la vez:
#   - la lista (contexto["enemigos"]: pos, debajo)
#   - la matriz (simbolo dibujado en mapa_actual)
# Hoy se sincronizan a mano en mover_slimes. Al morir un enemigo hay que sacarlo de AMBOS.
# Decidir fuente unica o sincronizacion prolija antes de implementar combate.

import random
from config import (
    MAPA_REAL_ALTO,
    MAPA_REAL_ANCHO,
    simbolos_pasto,
    simbolo_slime,
)


# ─── Estado de los slimes ─────────────────────────────────────────────────────
# Cada entrada: {"pos": [fila, col], "debajo": símbolo_que_pisaba}
lista_slimes = [
    {"pos": [40, 20], "debajo": "."},
    {"pos": [50, 60], "debajo": ","},
    {"pos": [30, 100], "debajo": "░"},
]

# TODO(refactor): inicializar_slimes ya lee del contexto pero NO está conectada.
# Conectarla al subir de nivel, junto con carga de enemigos, en:
#   - main_mapas.py -> iniciar_mapas()
#   - jugador.py    -> cambio_de_mapa() (al entrar al prado)
# Secuencia correcta al entrar a un mapa con enemigos:
#   1. generar mapa  2. contexto["enemigos"] = generar_enemigos_prado()  3. inicializar_slimes(mapa, contexto)


def inicializar_slimes(mapa, contexto):
    """Dibuja los slimes en su posición inicial en el mapa dado."""
    for slime in contexto["enemigos"]:
        f, c = slime["pos"]
        mapa[f][c] = simbolo_slime  # TODO # usar "tipo": "slime"


# TODO(deuda): el simbolo del enemigo esta fijo (simbolo_slime).
# Deberia salir de slime["tipo"] para soportar otros enemigos (goblins, etc.) sin redibujar mal.


def mover_slimes(mapa, contexto):
    """
    Mueve cada slime una celda al azar (o lo deja quieto).
    Solo se mueve si la celda destino es pasto o camino '░'.
    """
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]

    for slime in contexto["enemigos"]:
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
                slime["pos"] = [nf, nc]

                # Dibujar el slime
                mapa[nf][nc] = simbolo_slime
