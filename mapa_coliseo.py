# mapa_coliseo.py — Mapa 5: El Coliseo
#
# Vista cenital (referencia):
#   - Arena oval central de suelo de tierra '░'
#   - Anillos concéntricos de paredes de piedra '#' que forman las gradas
#   - 8 puertas/arcos 'O' decorativos en el anillo exterior (solo visuales)
#   - Entrada sur del jugador 'O' en fila alta, columna central
#   - Jefe del coliseo 'J' en el centro exacto del mapa
#   - Columnas decorativas 'I' distribuidas en la arena
#   - 4 arcos de madera '[]' dentro del anillo interior (como las jaulas de la imagen)

COLISEO_ALTO  = 50
COLISEO_ANCHO = 80

SIMBOLO_ARENA    = "░"   # suelo de arena
SIMBOLO_PARED    = "#"   # muros/gradas
SIMBOLO_COLUMNA  = "I"   # columna decorativa en la arena
SIMBOLO_ARCO     = "["   # arco lateral izquierdo
SIMBOLO_ARCO_D   = "]"   # arco lateral derecho
SIMBOLO_JEFE     = "J"   # jefe del coliseo


def _es_en_elipse(f, c, cf, cc, ra, rb, margen=0):
    """Devuelve True si (f,c) está dentro de la elipse con centro (cf,cc) y semiejes ra,rb."""
    return ((f - cf) / ra) ** 2 + ((c - cc) / rb) ** 2 <= (1 + margen) ** 2


def generar_mapa_coliseo():
    """
    Genera la matriz del Coliseo (mapa 5).

    Layout:
      - Exterior: paredes '#'
      - Anillo de gradas: 3 anillos concéntricos de '#' con distintos radios
      - Arena interior: suelo '░'
      - Entrada del jugador: 'O' en la fila más baja del interior (sur)
      - Columnas 'I' simétricas en la arena
      - Jefe 'J' en el centro
    """
    from config import simbolos_entorno

    mapa = [["#"] * COLISEO_ANCHO for _ in range(COLISEO_ALTO)]

    cf = COLISEO_ALTO  // 2   # centro fila
    cc = COLISEO_ANCHO // 2   # centro columna

    # Semiejes de los 3 anillos (exterior → interior)
    anillos = [
        (cf - 2,  cc - 3,  1.5),   # anillo exterior (gradas externas)
        (cf - 5,  cc - 6,  1.2),   # anillo medio
        (cf - 8,  cc - 10, 1.0),   # anillo interior (borde de arena)
    ]

    # ── 1. Rellenar anillos de adentro hacia afuera ───────────────────────────
    # Anillo exterior: todo lo que esté dentro es pared gris (ya lo está)
    # Arena: todo dentro del anillo interior es arena

    ra_ext = cf - 2    # semieje vertical exterior
    rb_ext = cc - 3    # semieje horizontal exterior
    ra_int = cf - 9    # semieje vertical interior (arena)
    rb_int = cc - 11   # semieje horizontal interior (arena)

    for f in range(COLISEO_ALTO):
        for c in range(COLISEO_ANCHO):
            dentro_ext = _es_en_elipse(f, c, cf, cc, ra_ext, rb_ext)
            dentro_int = _es_en_elipse(f, c, cf, cc, ra_int, rb_int)

            if not dentro_ext:
                mapa[f][c] = "#"          # exterior sólido
            elif dentro_int:
                mapa[f][c] = SIMBOLO_ARENA  # piso de arena
            else:
                mapa[f][c] = "#"          # gradas

    # ── 2. Trazar senderos de gradas (anillos vacíos de 1 celda) ─────────────
    # Crea 3 "pasillos" concéntricos dentro de las gradas
    for grosor, (ra_g, rb_g) in enumerate([
        (ra_ext - 2, rb_ext - 3),
        (ra_ext - 4, rb_ext - 6),
        (ra_ext - 6, rb_ext - 9),
    ]):
        if ra_g <= 0 or rb_g <= 0:
            break
        for f in range(COLISEO_ALTO):
            for c in range(COLISEO_ANCHO):
                if _es_en_elipse(f, c, cf, cc, ra_g, rb_g, margen=0.07):
                    if not _es_en_elipse(f, c, cf, cc, ra_g - 1, rb_g - 1, margen=0.07):
                        mapa[f][c] = "░"   # pasillo de grada

    # ── 3. Arcos/jaulas 'O' en 8 puntos del anillo exterior ──────────────────
    import math
    for angulo_deg in range(0, 360, 45):
        ang = math.radians(angulo_deg)
        fa  = int(cf + (ra_ext - 1) * math.sin(ang))
        ca  = int(cc + (rb_ext - 1) * math.cos(ang))
        if 0 <= fa < COLISEO_ALTO and 0 <= ca < COLISEO_ANCHO:
            mapa[fa][ca] = "O"   # arco decorativo en las gradas

    # ── 4. Entrada real del jugador (sur de la arena) ─────────────────────────
    # Abre un hueco en la pared de gradas sur y pone la 'O' de teletransporte
    f_entrada = cf + ra_int - 1   # fila sur del borde de arena
    mapa[f_entrada][cc] = simbolos_entorno[1]   # O real

    # ── 5. Columnas decorativas en la arena ───────────────────────────────────
    offsets_columnas = [(-5, -8), (-5, 8), (5, -8), (5, 8)]
    for df, dc in offsets_columnas:
        f_col = cf + df
        c_col = cc + dc
        if 0 <= f_col < COLISEO_ALTO and 0 <= c_col < COLISEO_ANCHO:
            if mapa[f_col][c_col] == SIMBOLO_ARENA:
                mapa[f_col][c_col] = SIMBOLO_COLUMNA

    # ── 6. Jefe en el centro ──────────────────────────────────────────────────
    mapa[cf][cc] = SIMBOLO_JEFE

    return mapa
