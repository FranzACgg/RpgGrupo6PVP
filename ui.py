# ui.py — Renderizado con Rich y menú en juego

import os
from rich.console import Console
from rich.panel   import Panel
from rich.align   import Align

from config import (
    CAMARA_ALTO, CAMARA_ANCHO,
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    ESTILOS, TECLAS_ACCION, estado,
)
from inventario import manejar_inventario

console = Console()

# Dimensiones de cámara para la cueva (más estrecha)
from mapa_cueva import CUEVA_ALTO, CUEVA_ANCHO
CAMARA_CUEVA_ALTO  = 15
CAMARA_CUEVA_ANCHO = 30


def dibujar_juego_centrado():
    os.system('cls' if os.name == 'nt' else 'clear')

    pos_p       = estado["pos_p"]
    mapa_actual = estado["mapa_actual"]
    hp, hp_max  = estado["hp"],  estado["hp_max"]
    mp, mp_max  = estado["mp"],  estado["mp_max"]
    n           = estado["numero_mapa"]

    # Cámara adaptada al mapa
    if n == 4:   # cueva
        cam_alto  = CAMARA_CUEVA_ALTO
        cam_ancho = CAMARA_CUEVA_ANCHO
        mapa_alto = CUEVA_ALTO
        mapa_ancho = CUEVA_ANCHO
    else:
        cam_alto  = CAMARA_ALTO
        cam_ancho = CAMARA_ANCHO
        mapa_alto = MAPA_REAL_ALTO
        mapa_ancho = MAPA_REAL_ANCHO

    inicio_f = max(0, min(pos_p[0] - cam_alto  // 2, mapa_alto  - cam_alto))
    inicio_c = max(0, min(pos_p[1] - cam_ancho // 2, mapa_ancho - cam_ancho))

    filas = []
    for f in range(inicio_f, inicio_f + cam_alto):
        fila_str = ""
        for c in range(inicio_c, inicio_c + cam_ancho):
            char  = mapa_actual[f][c]
            color = ESTILOS.get(char, "white")
            fila_str += f"[{color}]{char}[/] "
        filas.append(fila_str)

    nombre_personaje = ""
    if estado["personaje"]:
        p = estado["personaje"]
        nombre_personaje = f" — {p['nombre']} ({p['clase']})"

    nombres_mapa = {1: "Mercado", 2: "Prado", 3: "Cementerio", 4: "Cueva"}
    titulo_mapa  = nombres_mapa.get(n, "?")

    pantalla = Panel(
        "\n".join(filas),
        title    = f"[bold yellow]GLASSTION · {titulo_mapa}{nombre_personaje}[/]",
        subtitle = f"[bold red]HP: {hp}/{hp_max}[/] | [bold blue]MP: {mp}/{mp_max}[/]",
        border_style = "bright_blue",
        expand   = False,
        padding  = (1, 2),
    )
    console.print(Align(pantalla, align="center", vertical="middle",
                        height=console.size.height))


def pantalla_menu_en_juego(obtener_tecla_fn):
    en_menu = True
    while en_menu:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("╔══════════════════════════╗")
        print("║     MENÚ DE OPCIONES     ║")
        print("╠══════════════════════════╣")
        print("║  I  →  Inventario        ║")
        print("║  V  →  Volver al juego   ║")
        print("║  Q  →  Salir             ║")
        print("╚══════════════════════════╝")

        opcion = obtener_tecla_fn()

        if opcion == TECLAS_ACCION[1]:
            manejar_inventario(estado["inventario"])
        elif opcion == "v":
            en_menu = False
        elif opcion == TECLAS_ACCION[2]:
            print("\nSaliendo del juego...")
            exit()
