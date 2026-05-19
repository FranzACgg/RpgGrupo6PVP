# main_mapas.py — Bucle principal del juego (mapas)

import msvcrt   # Solo Windows. En Linux/Mac: import tty, sys, termios

from config      import estado, TECLAS_MOVIMIENTO, TECLAS_ACCION
from mapa_prado  import generar_mapa_prado
from jugador     import mover, cambio_de_mapa
from entidades   import mover_slimes
from ui          import dibujar_juego_centrado, pantalla_menu_en_juego


# ─── Entrada de teclado ───────────────────────────────────────────────────────

def obtener_tecla():
    """Lee una tecla sin necesidad de pulsar Enter (solo Windows)."""
    return msvcrt.getch().decode('utf-8', errors='ignore').lower()


# ─── Procesado de entrada ─────────────────────────────────────────────────────

def procesar_entrada(tecla):
    if tecla in TECLAS_MOVIMIENTO:
        mover(tecla)
    elif tecla == TECLAS_ACCION[3]:   # o → menú de pausa
        pantalla_menu_en_juego(obtener_tecla)


# ─── Configurar estado antes de entrar al bucle ───────────────────────────────

def iniciar_mapas():
    """
    Genera el mapa inicial (Prado) y configura el estado.
    Llamado desde main.py después de elegir personaje.
    Devuelve el mapa generado.
    """
    from mapa_prado import generar_mapa_prado
    mapa = generar_mapa_prado()
    estado["mapa_actual"]    = mapa
    estado["numero_mapa"]    = 2          # 2 = Prado
    estado["pos_p"][:]       = [1, 52]
    estado["simbolo_debajo"] = "░"
    estado["pasos_jugador"]  = 0
    return mapa


# ─── Bucle principal ──────────────────────────────────────────────────────────

def iniciar_mapa():
    """Bucle principal del juego. Llamar después de iniciar_mapas()."""
    while True:
        dibujar_juego_centrado()

        tecla = obtener_tecla()
        procesar_entrada(tecla)

        # Slimes solo se mueven en el Prado (mapa 2)
        if estado["numero_mapa"] == 2:
            estado["pasos_jugador"] += 1
            if estado["pasos_jugador"] % 2 == 0:
                mover_slimes(estado["mapa_actual"])

        cambio_de_mapa()


# ─── Punto de entrada directo (para probar sin menú) ─────────────────────────

if __name__ == "__main__":
    iniciar_mapas()
    iniciar_mapa()
