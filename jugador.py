# jugador.py — Movimiento del jugador, cambio de mapa y disparo de combate

import random
from config import (
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    simbolos_entorno, simbolos_pasto, simbolos_especiales,
    TECLAS_MOVIMIENTO, items_mapa,
)
from mapa_prado       import generar_mapa_prado
from mapa_mercado     import generar_mapa_mercado_total
from mapa_cementerio  import generar_mapa_cementerio
from mapa_cueva       import generar_mapa_cueva, CUEVA_ALTO, CUEVA_ANCHO
from mapa_coliseo     import generar_mapa_coliseo, COLISEO_ALTO, COLISEO_ANCHO
from inventario       import agregar_item
from entidades        import (
    buscar_enemigo_en, inicializar_enemigos,
    generar_enemigos_prado, generar_enemigos_cueva, generar_enemigo_coliseo,
)


def mover(tecla, contexto, obtener_tecla_fn=None):
    mundo       = contexto["mundo"]
    pos_p       = mundo["pos_p"]
    mapa_actual = mundo["mapa_actual"]
    alto        = mundo["dim_alto"]
    ancho       = mundo["dim_ancho"]

    df, dc = 0, 0
    if   tecla == TECLAS_MOVIMIENTO[2]: df =  1
    elif tecla == TECLAS_MOVIMIENTO[0]: df = -1
    elif tecla == TECLAS_MOVIMIENTO[1]: dc = -1
    elif tecla == TECLAS_MOVIMIENTO[3]: dc =  1
    else: return

    nueva_f = pos_p[0] + df
    nueva_c = pos_p[1] + dc

    if not (0 <= nueva_f < alto and 0 <= nueva_c < ancho):
        return

    celda_destino = mapa_actual[nueva_f][nueva_c]

    # Colisión con paredes
    if celda_destino in (simbolos_entorno[3], simbolos_entorno[2], "#"):
        return

    # ── Encuentro con enemigo ─────────────────────────────────────────────────
    enemigo = buscar_enemigo_en([nueva_f, nueva_c], contexto)
    if enemigo and obtener_tecla_fn:
        from pantalla_batalla import iniciar_batalla
        gano = iniciar_batalla(enemigo, mapa_actual, contexto, obtener_tecla_fn)
        if not gano:
            return   # escapó o murió → no se mueve
        # El enemigo ya fue eliminado del mapa por iniciar_batalla.
        # Actualizamos celda_destino con lo que quedó (el "debajo" restaurado).
        celda_destino = mapa_actual[nueva_f][nueva_c]

    # ── Recoger ítem ──────────────────────────────────────────────────────────
    if celda_destino == simbolos_especiales[1]:
        respuesta = input(
            "¿Deseas Recoger el Objeto? S/N: "
        )  # TODO integrar input a rich
        if respuesta.lower() == "s":
            clave = random.choice(list(items_mapa.keys()))
            item_base = random.choice(items_mapa[clave])
            agregar_item(item_base, contexto["inventario"])

    # ── Mover ─────────────────────────────────────────────────────────────────
    mapa_actual[pos_p[0]][pos_p[1]] = mundo["simbolo_debajo"]

    if celda_destino in simbolos_pasto or celda_destino == simbolos_especiales[1]:
        mundo["simbolo_debajo"] = random.choice(simbolos_pasto)
    elif celda_destino == " ":
        mundo["simbolo_debajo"] = " "
    else:
        mundo["simbolo_debajo"] = celda_destino

    pos_p[0], pos_p[1] = nueva_f, nueva_c
    mapa_actual[pos_p[0]][pos_p[1]] = simbolos_especiales[0]  # P


def cambio_de_mapa(contexto):
    mundo = contexto["mundo"]
    if mundo["simbolo_debajo"] != "O":
        return

    numero_mapa = mundo["numero_mapa"]
    pos_p       = mundo["pos_p"]
    mapa_actual = mundo["mapa_actual"]

    def _confirmar(msg):
        return input(msg).lower() == "s"

    def _cargar(nuevo_mapa, nuevo_numero, nueva_pos, nuevo_debajo,
                alto=MAPA_REAL_ALTO, ancho=MAPA_REAL_ANCHO, enemigos=None):
        mapa_actual[pos_p[0]][pos_p[1]] = "O"
        mundo["mapa_actual"]    = nuevo_mapa
        mundo["numero_mapa"]    = nuevo_numero
        mundo["pos_p"]          = nueva_pos
        mundo["simbolo_debajo"] = nuevo_debajo
        mundo["dim_alto"]       = alto
        mundo["dim_ancho"]      = ancho
        mundo["enemigos"]       = enemigos or []
        if enemigos:
            inicializar_enemigos(nuevo_mapa, contexto)

    # Prado (2) → Mercado (1)
    if numero_mapa == 2 and pos_p[1] == 0:
        if _confirmar("¿Deseas entrar al Mercado? S/N: "):
            _cargar(generar_mapa_mercado_total(), 1, [30, 127], "░")

    # Prado (2) → Cementerio (3)
    elif numero_mapa == 2 and pos_p[0] == 89:
        if _confirmar("¿Deseas entrar al Cementerio? S/N: "):
            _cargar(generar_mapa_cementerio(), 3, [85, 73], simbolos_pasto[1])
            contexto["mundo"]["enemigos"] = []

    # Prado (2) → Cueva (4)
    elif numero_mapa == 2 and pos_p == [12, 10]:
        if _confirmar("¿Deseas entrar a la Cueva? S/N: "):
            _cargar(generar_mapa_cueva(), 4, [CUEVA_ALTO // 2, 1], "▓",
                    alto=CUEVA_ALTO, ancho=CUEVA_ANCHO,
                    enemigos=generar_enemigos_cueva())

    # Cementerio (3) → Prado (2): salida sur
    elif numero_mapa == 3 and pos_p[0] == 86:
        if _confirmar("¿Deseas volver al Prado? S/N: "):
            _cargar(generar_mapa_prado(), 2, [88, 65], "░",
                    enemigos=generar_enemigos_prado())

    # Cementerio (3) → Coliseo (5): salida norte (fila 2, col 65)
    elif numero_mapa == 3 and pos_p == [2, 65]:
        if _confirmar("¿Deseas entrar al Coliseo? S/N: "):
            _cargar(generar_mapa_coliseo(), 5, [40, 40], "░",
                    alto=COLISEO_ALTO, ancho=COLISEO_ANCHO,
                    enemigos=generar_enemigo_coliseo())

    # Mercado (1) → Prado (2)
    elif numero_mapa == 1 and pos_p[1] == MAPA_REAL_ANCHO - 1:
        if _confirmar("¿Deseas salir del Mercado? S/N: "):
            _cargar(generar_mapa_prado(), 2, [45, 1], "░",
                    enemigos=generar_enemigos_prado())

    # Cueva (4) → Prado (2)
    elif numero_mapa == 4 and pos_p[1] == 0:
        if _confirmar("¿Deseas salir de la Cueva? S/N: "):
            _cargar(generar_mapa_prado(), 2, [12, 11], ".",
                    enemigos=generar_enemigos_prado())

    # Coliseo (5) → Cementerio (3): salida sur (fila 40 es la entrada)
    elif numero_mapa == 5 and pos_p == [40, 40]:
        if mundo["enemigos"]:
            # El jefe sigue vivo, no se puede salir fácil
            print("¡El Campeón bloquea tu salida! Debes vencerlo.")
        else:
            if _confirmar("¿Deseas salir del Coliseo? S/N: "):
                _cargar(generar_mapa_cementerio(), 3, [3, 65], simbolos_pasto[1])
