# main_mapas.py — Bucle principal del juego

import msvcrt

from config    import estado, TECLAS_MOVIMIENTO, TECLAS_ACCION
from mapa_mercado import generar_mapa_mercado_total
from jugador   import mover, cambio_de_mapa, _set_dimensiones
from entidades import mover_slimes, mover_goblins
from ui        import dibujar_juego_centrado, pantalla_menu_en_juego
from mapa_cueva import CUEVA_ALTO, CUEVA_ANCHO
from config    import MAPA_REAL_ALTO, MAPA_REAL_ANCHO


def obtener_tecla():
    return msvcrt.getch().decode('utf-8', errors='ignore').lower()


def procesar_entrada(tecla):
    if tecla in TECLAS_MOVIMIENTO:
        mover(tecla, obtener_tecla)
    elif tecla == TECLAS_ACCION[3]:
        pantalla_menu_en_juego(obtener_tecla)


def iniciar_mapas():
    """Carga el Mercado como mapa inicial y pone al jugador arriba."""
    from mapa_mercado import generar_mapa_mercado_total
    mapa = generar_mapa_mercado_total()
    c_centro = MAPA_REAL_ANCHO // 2
    estado["mapa_actual"]    = mapa
    estado["numero_mapa"]    = 1           # 1 = Mercado
    estado["pos_p"][:]       = [1, c_centro]
    estado["simbolo_debajo"] = "░"
    estado["pasos_jugador"]  = 0
    mapa[1][c_centro]        = "P"
    _set_dimensiones(MAPA_REAL_ALTO, MAPA_REAL_ANCHO)
    return mapa


def iniciar_mapa():
    while True:
        dibujar_juego_centrado()

        tecla = obtener_tecla()
        procesar_entrada(tecla)

        n = estado["numero_mapa"]
        estado["pasos_jugador"] += 1

        # Mobs se mueven cada 2 pasos
        if estado["pasos_jugador"] % 2 == 0:
            if n == 2:   # Prado → slimes
                mover_slimes(estado["mapa_actual"])
            elif n == 4: # Cueva → goblins
                mover_goblins(estado["mapa_actual"])

        cambio_de_mapa()


if __name__ == "__main__":
    iniciar_mapas()
    iniciar_mapa()
