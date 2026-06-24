# main_mapas.py — Bucle principal del juego

import msvcrt

from config   import TECLAS_MOVIMIENTO, TECLAS_ACCION, MAPA_REAL_ALTO, MAPA_REAL_ANCHO
from mapa_mercado import generar_mapa_mercado_total
from jugador  import mover, cambio_de_mapa
from entidades import mover_enemigos, generar_enemigos_prado, inicializar_enemigos
from ui       import dibujar_juego_centrado, pantalla_menu_en_juego


def obtener_tecla():
    return msvcrt.getch().decode('utf-8', errors='ignore').lower()


def procesar_entrada(tecla, contexto):
    if tecla in TECLAS_MOVIMIENTO:
        mover(tecla, contexto, obtener_tecla)
    elif tecla == TECLAS_ACCION[3]:
        pantalla_menu_en_juego(obtener_tecla, contexto)


def iniciar_mapas(contexto):
    """Arranca en el Mercado (mapa 1), jugador arriba al centro."""
    mapa     = generar_mapa_mercado_total()
    c_centro = MAPA_REAL_ANCHO // 2
    mapa[1][c_centro] = "P"

    mundo = contexto["mundo"]
    mundo["mapa_actual"]    = mapa
    mundo["numero_mapa"]    = 1
    mundo["pos_p"]          = [1, c_centro]
    mundo["simbolo_debajo"] = "░"
    mundo["pasos_jugador"]  = 0
    mundo["dim_alto"]       = MAPA_REAL_ALTO
    mundo["dim_ancho"]      = MAPA_REAL_ANCHO
    mundo["enemigos"]       = []


def iniciar_mapa(contexto):
    while True:
        dibujar_juego_centrado(contexto)

        tecla = obtener_tecla()
        procesar_entrada(tecla, contexto)

        mundo = contexto["mundo"]
        mundo["pasos_jugador"] += 1

        # Mobs se mueven cada 2 pasos (solo en mapas con enemigos)
        if mundo["pasos_jugador"] % 2 == 0 and mundo["enemigos"]:
            mover_enemigos(mundo["mapa_actual"], contexto)

        cambio_de_mapa(contexto)


if __name__ == "__main__":
    from config import crear_contexto
    from personajes import crear_personaje
    from inventario import crear_inventario
    ctx = crear_contexto()
    ctx["personaje"]  = crear_personaje("Test", "Guerrero")
    ctx["inventario"] = crear_inventario()
    iniciar_mapas(ctx)
    iniciar_mapa(ctx)




