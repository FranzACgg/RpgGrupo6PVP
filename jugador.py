# jugador.py — Movimiento, interacción con NPCs, cofres, tumbas y cambio de mapa

import random
from config import (
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    simbolos_entorno, simbolos_pasto, simbolos_especiales,
    TECLAS_MOVIMIENTO,
)
from catalogo         import item_aleatorio
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
from aldeanos         import buscar_aldeano_en, mostrar_dialogo, SIMBOLO_ALDEANO
from cofres           import abrir_cofre, excavar_tumba, SIMBOLO_COFRE, SIMBOLO_TUMBA_EXCAVABLE

# Símbolos transitables en el cementerio (senderos ▒ son piso, no pared)
CELDAS_TRANSITABLES_EXTRA = {"▒", "▓", "."}


def mover(tecla, contexto, obtener_tecla_fn=None):
    """
    Entrada: String (tecla), Diccionario (contexto), Funcion opcional (obtener_tecla_fn)
    Params:
        tecla: caracter de la tecla presionada (WASD segun TECLAS_MOVIMIENTO)
        contexto: el contexto completo del juego (mundo, inventario, progreso)
        obtener_tecla_fn: funcion para leer la siguiente tecla; necesaria para
            iniciar batallas. Si es None, los encuentros con enemigos no se procesan
    Objetivo: mover al jugador una celda en la direccion indicada, verificando
        colisiones, interacciones con NPCs, cofres, tumbas, enemigos e items.
        Si la celda destino es valida y libre, actualiza la posicion del jugador
        en el mapa y en el contexto
    Salida: none. Modifica el mapa y el contexto
    """
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

    # ── Colisión con paredes (▒ NO es pared — es sendero del cementerio) ─────
    if celda_destino in (simbolos_entorno[3], simbolos_entorno[2], "#", "+"):
        return

    # ── NPC aldeano ───────────────────────────────────────────────────────────
    if celda_destino == SIMBOLO_ALDEANO:
        aldeano = buscar_aldeano_en([nueva_f, nueva_c], contexto)
        if aldeano:
            mostrar_dialogo(aldeano, contexto["inventario"])
        return

    # ── Cofre ─────────────────────────────────────────────────────────────────
    if celda_destino == SIMBOLO_COFRE:
        abrir_cofre(contexto["inventario"], mapa_actual, [nueva_f, nueva_c])
        celda_destino = mapa_actual[nueva_f][nueva_c]

    # ── Tumba excavable ───────────────────────────────────────────────────────
    if celda_destino == SIMBOLO_TUMBA_EXCAVABLE:
        excavar_tumba(contexto["inventario"], mapa_actual, [nueva_f, nueva_c])
        return

    # ── Encuentro con enemigo ─────────────────────────────────────────────────
    enemigo = buscar_enemigo_en([nueva_f, nueva_c], contexto)
    if enemigo and obtener_tecla_fn:
        from pantalla_batalla import iniciar_batalla
        gano = iniciar_batalla(enemigo, mapa_actual, contexto, obtener_tecla_fn)
        if not gano:
            return
        celda_destino = mapa_actual[nueva_f][nueva_c]

    # ── Encuentro con el Jefe del Coliseo (símbolo 'J') ──────────────────────
    if celda_destino == "J" and mundo["numero_mapa"] == 5 and obtener_tecla_fn:
        from pantalla_batalla import iniciar_coliseo
        gano = iniciar_coliseo(mapa_actual, contexto, obtener_tecla_fn)
        if not gano:
            return
        celda_destino = mapa_actual[nueva_f][nueva_c]

    # ── Recoger ítem '*' ──────────────────────────────────────────────────────
    if celda_destino == simbolos_especiales[1]:
        respuesta = input("¿Deseas Recoger el Objeto? S/N: ")
        if respuesta.lower() == "s":
            item_base = item_aleatorio()
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
    mapa_actual[pos_p[0]][pos_p[1]] = simbolos_especiales[0]


def cambio_de_mapa(contexto):
    """
    Entrada: Diccionario (contexto)
    Objetivo: detectar si el jugador esta parado sobre un portal 'O' y ofrecer
        el cambio al mapa correspondiente segun el numero de mapa actual y la
        posicion del jugador. Cada transicion regenera el mapa destino y
        reubica al jugador en la posicion de entrada correcta
    Salida: none. Modifica el contexto (mundo) si se acepta el cambio
    """
    mundo = contexto["mundo"]
    if mundo["simbolo_debajo"] != "O":
        return

    numero_mapa  = mundo["numero_mapa"]
    pos_p        = mundo["pos_p"]
    mapa_actual  = mundo["mapa_actual"]
    bloqueado    = contexto["progreso"].get("cementerio_bloqueado", False)

    def _confirmar(msg):
        """
        Entrada: String (msg)
        Objetivo: mostrar un mensaje al jugador y esperar confirmacion S/N
        Salida: True si el jugador ingresa 's', False en cualquier otro caso
        """
        return input(msg).lower() == "s"

    def _cargar(nuevo_mapa, nuevo_numero, nueva_pos, nuevo_debajo,
                alto=MAPA_REAL_ALTO, ancho=MAPA_REAL_ANCHO, enemigos=None):
        """
        Entrada: Lista de listas (nuevo_mapa), Int (nuevo_numero),
            Lista [fila, col] (nueva_pos), String (nuevo_debajo),
            Int (alto), Int (ancho), Lista opcional (enemigos)
        Objetivo: realizar el cambio de mapa: restaurar el portal en el mapa
            actual, reemplazar mapa, posicion, dimensiones y enemigos en el
            contexto, dibujar al jugador en la posicion de entrada e
            inicializar los enemigos en el nuevo mapa si los hay
        Salida: none. Modifica el contexto (mundo) y el mapa actual
        """
        mapa_actual[pos_p[0]][pos_p[1]] = "O"
        mundo["mapa_actual"]    = nuevo_mapa
        mundo["numero_mapa"]    = nuevo_numero
        mundo["pos_p"]          = nueva_pos
        mundo["simbolo_debajo"] = nuevo_debajo
        mundo["dim_alto"]       = alto
        mundo["dim_ancho"]      = ancho
        mundo["enemigos"]       = enemigos or []
        nuevo_mapa[nueva_pos[0]][nueva_pos[1]] = simbolos_especiales[0]
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

    # Prado (2) → Cueva (4)
    elif numero_mapa == 2 and pos_p == [12, 10]:
        if _confirmar("¿Deseas entrar a la Cueva? S/N: "):
            _cargar(generar_mapa_cueva(), 4, [CUEVA_ALTO // 2, 1], "▓",
                    alto=CUEVA_ALTO, ancho=CUEVA_ANCHO,
                    enemigos=generar_enemigos_cueva())

    # Cementerio (3) → Prado (2): BLOQUEADO si murió
    elif numero_mapa == 3 and pos_p[0] == 86:
        if bloqueado:
            print("La puerta al Prado está sellada. Solo puedes ir al Coliseo.")
        elif _confirmar("¿Deseas volver al Prado? S/N: "):
            _cargar(generar_mapa_prado(), 2, [88, 65], "░",
                    enemigos=generar_enemigos_prado())

    # Cementerio (3) → Coliseo (5): siempre disponible
    elif numero_mapa == 3 and pos_p == [2, 65]:
        if _confirmar("¿Deseas entrar al Coliseo? S/N: "):
            mapa_col = generar_mapa_coliseo()
            _cargar(mapa_col, 5, [40, 40], "░",
                    alto=COLISEO_ALTO, ancho=COLISEO_ANCHO,
                    enemigos=generar_enemigo_coliseo())
            # Disparar batalla de rivales inmediatamente al entrar
            contexto["mundo"]["coliseo_pendiente"] = True

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

    # Coliseo (5) → Cementerio (3): solo disponible si completó el coliseo
    elif numero_mapa == 5 and pos_p == [40, 40]:
        if not contexto["progreso"].get("coliseo_completado", False):
            print("¡Debes enfrentarte a los rivales primero!")
        elif _confirmar("¿Deseas salir del Coliseo? S/N: "):
            _cargar(generar_mapa_cementerio(), 3, [3, 65], simbolos_pasto[1])
