# main_mapas.py — Bucle principal del juego (mapas)

import msvcrt  # Solo Windows. En Linux/Mac: import tty, sys, termios

from config import TECLAS_MOVIMIENTO, TECLAS_ACCION
from mapa_prado import generar_mapa_prado, generar_enemigos_prado
from jugador import mover, cambio_de_mapa
from entidades import mover_slimes, inicializar_slimes
from ui import dibujar_juego_centrado, pantalla_menu_en_juego


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
    contexto["enemigos"] = generar_enemigos_prado()
    contexto["mundo"]["numero_mapa"] = 2
    contexto["mundo"]["pos_p"] = [1, 52]
    contexto["mundo"]["simbolo_debajo"] = "░"
    contexto["mundo"]["pasos_jugador"] = 0
    inicializar_slimes(mapa, contexto)


# ─── Bucle principal ──────────────────────────────────────────────────────────


def iniciar_mapa(contexto):
    """Bucle principal del juego. Llamar después de iniciar_mapas()."""
    while True:
        dibujar_juego_centrado(contexto)

        tecla = obtener_tecla()
        procesar_entrada(tecla, contexto)

        # Slimes solo se mueven en el Prado (mapa 2)
        if contexto["mundo"]["numero_mapa"] == 2:
            contexto["mundo"]["pasos_jugador"] += 1
            if contexto["mundo"]["pasos_jugador"] % 2 == 0:
                mover_slimes(contexto["mundo"]["mapa_actual"], contexto)

        cambio_de_mapa(contexto)


# ─── Punto de entrada directo (para probar sin menú) ─────────────────────────

if __name__ == "__main__":
    iniciar_mapas()
    iniciar_mapa()
