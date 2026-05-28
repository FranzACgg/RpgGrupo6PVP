# jugador.py — Movimiento del jugador y cambio de mapa

import random
from config import (
    MAPA_REAL_ALTO,
    MAPA_REAL_ANCHO,
    simbolos_entorno,
    simbolos_pasto,
    simbolos_especiales,
    TECLAS_MOVIMIENTO,
    items_mapa,
)
from mapa_prado import generar_mapa_prado, generar_enemigos_prado
from mapa_mercado import generar_mapa_mercado_total
from mapa_cementerio import generar_mapa_cementerio
from inventario import agregar_item
from entidades import inicializar_slimes


# ─── Movimiento ───────────────────────────────────────────────────────────────


def mover(tecla, contexto):
    """Mueve al jugador según la tecla pulsada, con colisiones e ítems."""
    pos_p = contexto["mundo"]["pos_p"]
    mapa_actual = contexto["mundo"]["mapa_actual"]

    df, dc = 0, 0
    if tecla == TECLAS_MOVIMIENTO[2]:
        df = 1  # s
    elif tecla == TECLAS_MOVIMIENTO[0]:
        df = -1  # w
    elif tecla == TECLAS_MOVIMIENTO[1]:
        dc = -1  # a
    elif tecla == TECLAS_MOVIMIENTO[3]:
        dc = 1  # d
    else:
        return

    nueva_f = pos_p[0] + df
    nueva_c = pos_p[1] + dc

    if not (0 <= nueva_f < MAPA_REAL_ALTO and 0 <= nueva_c < MAPA_REAL_ANCHO):
        return

    celda_destino = mapa_actual[nueva_f][nueva_c]

    # Colisión con paredes
    if celda_destino in (simbolos_entorno[3], simbolos_entorno[2]):
        return

    # Recoger ítem — usa el sistema nuevo de inventario.py
    if celda_destino == simbolos_especiales[1]:
        respuesta = input(
            "¿Deseas Recoger el Objeto? S/N: "
        )  # TODO integrar input a rich
        if respuesta.lower() == "s":
            clave = random.choice(list(items_mapa.keys()))
            item_base = random.choice(items_mapa[clave])
            agregar_item(item_base, contexto["inventario"])

    # 1. Restaurar celda anterior
    mapa_actual[pos_p[0]][pos_p[1]] = contexto["mundo"]["simbolo_debajo"]

    # 2. Guardar símbolo de la celda destino
    if (
        celda_destino in simbolos_pasto
        or celda_destino == simbolos_especiales[1]
    ):
        contexto["mundo"]["simbolo_debajo"] = random.choice(simbolos_pasto)
    elif celda_destino == " ":
        contexto["mundo"]["simbolo_debajo"] = " "
    else:
        contexto["mundo"]["simbolo_debajo"] = celda_destino

    # 3. Mover al jugador
    pos_p[0], pos_p[1] = nueva_f, nueva_c
    mapa_actual[pos_p[0]][pos_p[1]] = simbolos_especiales[0]  # P


# ─── Cambio de mapa ───────────────────────────────────────────────────────────


def cambio_de_mapa(contexto):
    """
    Si el jugador está parado sobre una entrada 'O', ofrece cambiar de mapa.
    """
    if contexto["mundo"]["simbolo_debajo"] != "O":
        return

    numero_mapa = contexto["mundo"]["numero_mapa"]
    pos_p = contexto["mundo"]["pos_p"]
    mapa_actual = contexto["mundo"]["mapa_actual"]

    def _confirmar(msg):
        return input(msg).lower() == "s"

    def _cargar(nuevo_mapa, nuevo_numero, nueva_pos, nuevo_debajo):
        mapa_actual[pos_p[0]][pos_p[1]] = (
            "O"  # restaurar entrada en mapa viejo
        )
        contexto["mundo"]["mapa_actual"] = nuevo_mapa
        contexto["mundo"]["numero_mapa"] = nuevo_numero
        contexto["mundo"]["pos_p"] = nueva_pos
        contexto["mundo"]["simbolo_debajo"] = nuevo_debajo

    # Prado (2) → Mercado (1): salida izquierda
    if numero_mapa == 2 and pos_p[1] == 0:
        if _confirmar(
            "¿Deseas entrar al Mercado? S/N: "
        ):  # TODO integrar input con rich
            _cargar(generar_mapa_mercado_total(), 1, [30, 128], "░")
            contexto["mundo"]["enemigos"] = []

    # Prado (2) → Cementerio (3): salida inferior
    elif numero_mapa == 2 and pos_p[0] == 89:
        if _confirmar("¿Deseas entrar al Cementerio? S/N: "):
            _cargar(generar_mapa_cementerio(), 3, [85, 73], simbolos_pasto[1])
            contexto["mundo"]["enemigos"] = []

    # Cementerio (3) → Prado (2): salida superior
    elif numero_mapa == 3 and pos_p[0] == 86:
        if _confirmar("¿Deseas volver al Prado? S/N: "):
            _cargar(generar_mapa_prado(), 2, [88, 65], "░")
            contexto["mundo"]["enemigos"] = generar_enemigos_prado()
            inicializar_slimes(contexto["mundo"]["mapa_actual"], contexto)

    # Mercado (1) → Prado (2): salida derecha
    elif numero_mapa == 1 and pos_p[1] == 129:
        if _confirmar("¿Deseas salir del Mercado? S/N: "):
            _cargar(generar_mapa_prado(), 2, [45, 1], "░")
            contexto["mundo"]["enemigos"] = generar_enemigos_prado()
            inicializar_slimes(contexto["mundo"]["mapa_actual"], contexto)
