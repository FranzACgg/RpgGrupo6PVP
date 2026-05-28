# jugador.py — Movimiento del jugador, cambio de mapa y disparo de combate

import random
from config import (
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    simbolos_entorno, simbolos_pasto, simbolos_especiales,
    TECLAS_MOVIMIENTO, items_mapa, estado,
    simbolo_slime, simbolo_goblin,
)
from mapa_prado       import generar_mapa_prado
from mapa_mercado     import generar_mapa_mercado_total
from mapa_cementerio  import generar_mapa_cementerio
from mapa_cueva       import generar_mapa_cueva, CUEVA_ALTO, CUEVA_ANCHO
from inventario       import agregar_item
import entidades


# ─── Dimensiones activas (se actualizan según el mapa) ───────────────────────
_alto_activo  = MAPA_REAL_ALTO
_ancho_activo = MAPA_REAL_ANCHO


def _set_dimensiones(alto, ancho):
    global _alto_activo, _ancho_activo
    _alto_activo  = alto
    _ancho_activo = ancho


# ─── Movimiento ───────────────────────────────────────────────────────────────

def mover(tecla, obtener_tecla_fn=None):
    """
    Mueve al jugador.
    Si la celda destino es un mob activa la batalla antes de moverse.
    obtener_tecla_fn se necesita para pasar a pantalla_batalla.
    """
    pos_p       = estado["pos_p"]
    mapa_actual = estado["mapa_actual"]

    df, dc = 0, 0
    if   tecla == TECLAS_MOVIMIENTO[2]: df =  1
    elif tecla == TECLAS_MOVIMIENTO[0]: df = -1
    elif tecla == TECLAS_MOVIMIENTO[1]: dc = -1
    elif tecla == TECLAS_MOVIMIENTO[3]: dc =  1
    else: return

    nueva_f = pos_p[0] + df
    nueva_c = pos_p[1] + dc

    if not (0 <= nueva_f < _alto_activo and 0 <= nueva_c < _ancho_activo):
        return

    celda_destino = mapa_actual[nueva_f][nueva_c]

    # ── Colisión con paredes ──────────────────────────────────────────────────
    if celda_destino in (simbolos_entorno[3], simbolos_entorno[2], "#"):
        return

    # ── Encuentro con mob → batalla (sin moverse encima del mob) ─────────────
    if celda_destino == simbolo_slime:
        slime = entidades.verificar_combate_slime([nueva_f, nueva_c])
        if slime and obtener_tecla_fn:
            from pantalla_batalla import iniciar_batalla
            gano = iniciar_batalla("ζ", "Slime", 40, obtener_tecla_fn)
            if gano:
                entidades.eliminar_slime(slime, mapa_actual)
                # Ahora sí mover al jugador a esa celda
            else:
                return   # escapó o murió, no se mueve
        else:
            return

    if celda_destino == simbolo_goblin:
        goblin = entidades.verificar_combate_goblin([nueva_f, nueva_c])
        if goblin and obtener_tecla_fn:
            from pantalla_batalla import iniciar_batalla
            gano = iniciar_batalla("G", "Goblin", 60, obtener_tecla_fn)
            if gano:
                entidades.eliminar_goblin(goblin, mapa_actual)
            else:
                return
        else:
            return

    # ── Recoger ítem ──────────────────────────────────────────────────────────
    if celda_destino == simbolos_especiales[1]:
        respuesta = input("¿Deseas Recoger el Objeto? S/N: ")
        if respuesta.lower() == "s":
            clave     = random.choice(list(items_mapa.keys()))
            item_base = random.choice(items_mapa[clave])
            agregar_item(item_base, estado["inventario"])

    # ── Mover ─────────────────────────────────────────────────────────────────
    mapa_actual[pos_p[0]][pos_p[1]] = estado["simbolo_debajo"]

    if celda_destino in simbolos_pasto or celda_destino == simbolos_especiales[1]:
        estado["simbolo_debajo"] = random.choice(simbolos_pasto)
    elif celda_destino == " ":
        estado["simbolo_debajo"] = " "
    else:
        estado["simbolo_debajo"] = celda_destino

    pos_p[0], pos_p[1] = nueva_f, nueva_c
    mapa_actual[pos_p[0]][pos_p[1]] = simbolos_especiales[0]   # P


# ─── Cambio de mapa ───────────────────────────────────────────────────────────

def cambio_de_mapa():
    if estado["simbolo_debajo"] != "O":
        return

    numero_mapa = estado["numero_mapa"]
    pos_p       = estado["pos_p"]
    mapa_actual = estado["mapa_actual"]

    def _confirmar(msg):
        return input(msg).lower() == "s"

    def _cargar(nuevo_mapa, nuevo_numero, nueva_pos, nuevo_debajo, alto=None, ancho=None):
        mapa_actual[pos_p[0]][pos_p[1]] = "O"
        estado["mapa_actual"]    = nuevo_mapa
        estado["numero_mapa"]    = nuevo_numero
        estado["pos_p"][:]       = nueva_pos
        estado["simbolo_debajo"] = nuevo_debajo
        _set_dimensiones(
            alto  if alto  else MAPA_REAL_ALTO,
            ancho if ancho else MAPA_REAL_ANCHO,
        )

    # Prado (2) → Mercado (1)
    if numero_mapa == 2 and pos_p[1] == 0:
        if _confirmar("¿Deseas entrar al Mercado? S/N: "):
            _cargar(generar_mapa_mercado_total(), 1, [30, 127], "░")

    # Prado (2) → Cementerio (3)
    elif numero_mapa == 2 and pos_p[0] == 89:
        if _confirmar("¿Deseas entrar al Cementerio? S/N: "):
            _cargar(generar_mapa_cementerio(), 3, [85, 73], simbolos_pasto[1])

    # Prado (2) → Cueva (4): el jugador pisa la entrada 'O' de la cueva (fila 12, col 13)
    elif numero_mapa == 2 and pos_p == [12, 10]:
        if _confirmar("¿Deseas entrar a la Cueva? S/N: "):
            mapa_cueva, lista_g = generar_mapa_cueva()
            entidades.cargar_goblins(lista_g)
            _cargar(mapa_cueva, 4, [CUEVA_ALTO // 2, 1], "▓",
                    alto=CUEVA_ALTO, ancho=CUEVA_ANCHO)

    # Cementerio (3) → Prado (2)
    elif numero_mapa == 3 and pos_p[0] == 86:
        if _confirmar("¿Deseas volver al Prado? S/N: "):
            _cargar(generar_mapa_prado(), 2, [88, 65], "░")

    # Mercado (1) → Prado (2)
    elif numero_mapa == 1 and pos_p[1] == MAPA_REAL_ANCHO - 1:
        if _confirmar("¿Deseas salir del Mercado? S/N: "):
            _cargar(generar_mapa_prado(), 2, [45, 1], "░")

    # Cueva (4) → Prado (2): salida izquierda
    elif numero_mapa == 4 and pos_p[1] == 0:
        if _confirmar("¿Deseas salir de la Cueva? S/N: "):
            _cargar(generar_mapa_prado(), 2, [12, 11], ".")
