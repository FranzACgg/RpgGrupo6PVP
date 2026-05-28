# mapa_cueva.py — Mapa 4: La Cueva (acceso desde la cueva del Prado)

import random
from config import simbolos_entorno, simbolos_entornos_no_remplazables, simbolos_especiales

# ─── Dimensiones propias de la cueva ─────────────────────────────────────────
CUEVA_ALTO  = 45   # más largo que ancho → sensación de túnel
CUEVA_ANCHO = 50

# Símbolo de camino interior de la cueva
CAMINO_CUEVA = "▓"

# Decoraciones de la cueva
SIMBOLOS_DECO = ["💀", "⛏"]   # calavera, pico  (sin emojis de 2 chars problemáticos)
SIMBOLO_PARED = "#"
SIMBOLO_PISO  = "."
SIMBOLO_COFRE = "C"   # cofre al final del camino

# Mob de la cueva
SIMBOLO_GOBLIN = "G"   # ASCII simple, sin emoji de 2 chars


def _base_cueva():
    """Crea la matriz base: paredes '#' en bordes, piso '.' interior."""
    mapa = []
    for f in range(CUEVA_ALTO):
        fila = []
        for c in range(CUEVA_ANCHO):
            if f == 0 or f == CUEVA_ALTO - 1 or c == 0 or c == CUEVA_ANCHO - 1:
                fila.append(SIMBOLO_PARED)
            else:
                fila.append(SIMBOLO_PISO)
        mapa.append(fila)
    return mapa


def _dibujar_camino_central(mapa):
    """
    Traza un camino recto '▓' de izquierda a derecha por la fila central.
    Al final del camino (extremo derecho interior) coloca el cofre 'C'.
    """
    f_centro = CUEVA_ALTO // 2
    for c in range(1, CUEVA_ANCHO - 1):
        mapa[f_centro][c] = CAMINO_CUEVA

    # Cofre al final del camino (columna interior más a la derecha)
    mapa[f_centro][CUEVA_ANCHO - 2] = SIMBOLO_COFRE


def _colocar_decoraciones(mapa):
    """Siembra calaveras y picos aleatoriamente en el piso '.'."""
    f_centro = CUEVA_ALTO // 2
    for _ in range(25):
        f = random.randint(1, CUEVA_ALTO - 2)
        c = random.randint(1, CUEVA_ANCHO - 2)
        # No pisar el camino central ni el cofre
        if mapa[f][c] == SIMBOLO_PISO and f != f_centro:
            mapa[f][c] = random.choice(SIMBOLOS_DECO)


def _colocar_goblins(mapa):
    """
    Coloca 4 goblins 'G' en el piso de la cueva, alejados del camino.
    Devuelve la lista de dicts de goblins igual que lista_slimes en entidades.py.
    """
    f_centro = CUEVA_ALTO // 2
    goblins = []
    intentos = 0
    while len(goblins) < 4 and intentos < 200:
        intentos += 1
        f = random.randint(1, CUEVA_ALTO - 2)
        c = random.randint(1, CUEVA_ANCHO - 2)
        if mapa[f][c] == SIMBOLO_PISO and abs(f - f_centro) > 2:
            mapa[f][c] = SIMBOLO_GOBLIN
            goblins.append({"pos": [f, c], "debajo": SIMBOLO_PISO, "mapa": "cueva"})
    return goblins


def _colocar_entrada_salida(mapa):
    """
    Entrada (izquierda, fila central): 'O'
    Salida  (derecha, fila central, detrás del cofre): no hace falta —
    el jugador vuelve por la misma 'O'.
    """
    f_centro = CUEVA_ALTO // 2
    mapa[f_centro][0] = simbolos_entorno[1]   # O


def generar_mapa_cueva():
    """
    Genera y devuelve (mapa, lista_goblins).
    - mapa         : matriz CUEVA_ALTO × CUEVA_ANCHO
    - lista_goblins: lista de dicts con pos/debajo de cada goblin
    """
    mapa = _base_cueva()
    _dibujar_camino_central(mapa)
    _colocar_decoraciones(mapa)
    lista_goblins = _colocar_goblins(mapa)
    _colocar_entrada_salida(mapa)
    return mapa, lista_goblins
