# main_mapas.py — Bucle principal del juego

<<<<<<< HEAD
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
=======
import msvcrt  # Solo Windows. En Linux/Mac: import tty, sys, termios

from config import TECLAS_MOVIMIENTO, TECLAS_ACCION
from mapa_prado import generar_mapa_prado, generar_enemigos_prado
from jugador import mover
from entidades import inicializar_slimes
from ui import pantalla_menu_en_juego


# ─── Entrada de teclado ───────────────────────────────────────────────────────


def obtener_tecla():
    """Lee una tecla sin necesidad de pulsar Enter (solo Windows)."""
    return msvcrt.getch().decode("utf-8", errors="ignore").lower()


# ─── Procesado de entrada ─────────────────────────────────────────────────────


def procesar_entrada(tecla, contexto):
    if tecla in TECLAS_MOVIMIENTO:
        mover(tecla, contexto)
    elif tecla == TECLAS_ACCION[3]:  # o → menú de pausa
        pantalla_menu_en_juego(obtener_tecla, contexto)


# ─── Configurar contexto antes de entrar al bucle ───────────────────────────────


def iniciar_mapas(contexto):
    """
    Genera el mapa inicial (Prado) y guarda el contexto.
    Llamado desde main.py después de elegir personaje.
    """
    mapa = generar_mapa_prado()
    contexto["mundo"]["mapa_actual"] = mapa
    contexto["mundo"]["enemigos"] = generar_enemigos_prado()
    contexto["mundo"]["numero_mapa"] = 2
    contexto["mundo"]["pos_p"] = [1, 52]
    contexto["mundo"]["simbolo_debajo"] = "░"
    contexto["mundo"]["pasos_jugador"] = 0
    inicializar_slimes(mapa, contexto)
>>>>>>> origin/integracion_40
