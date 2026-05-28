# ui.py — Renderizado con Rich y menú en juego

import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

from config import (
    CAMARA_ALTO,
    CAMARA_ANCHO,
    MAPA_REAL_ALTO,
    MAPA_REAL_ANCHO,
    ESTILOS,
    TECLAS_ACCION,
)
from inventario import manejar_inventario

console = Console()


# ─── Renderizado del mapa ─────────────────────────────────────────────────────


def dibujar_juego_centrado(contexto):
    """Renderiza la cámara centrada en el jugador dentro de un Panel de Rich."""
    os.system("cls" if os.name == "nt" else "clear")

    pos_p = contexto["mundo"]["pos_p"]
    mapa_actual = contexto["mundo"]["mapa_actual"]
    hp = contexto["personaje"]["stats_actuales"]["hp"]
    mp = contexto["personaje"]["stats_actuales"]["mp"]
    hp_max = contexto["personaje"]["stats_base"]["hp"]
    mp_max = contexto["personaje"]["stats_base"]["mp"]

    inicio_f = max(
        0, min(pos_p[0] - CAMARA_ALTO // 2, MAPA_REAL_ALTO - CAMARA_ALTO)
    )
    inicio_c = max(
        0, min(pos_p[1] - CAMARA_ANCHO // 2, MAPA_REAL_ANCHO - CAMARA_ANCHO)
    )

    filas_coloreadas = []
    for f in range(inicio_f, inicio_f + CAMARA_ALTO):
        fila_str = ""
        for c in range(inicio_c, inicio_c + CAMARA_ANCHO):
            char = mapa_actual[f][c]
            color = ESTILOS.get(char, "white")
            fila_str += f"[{color}]{char}[/] "
        filas_coloreadas.append(fila_str)

    # Nombre del personaje si está disponible
    nombre_personaje = ""
    if contexto["personaje"]:
        p = contexto["personaje"]
        nombre_personaje = f" — {p['nombre']} ({p['clase']})"

    pantalla = Panel(
        "\n".join(filas_coloreadas),
        title=f"[bold yellow]GLASSTION{nombre_personaje} — POS: {pos_p[0]},{pos_p[1]}[/]",
        subtitle=f"[bold red]HP: {hp}/{hp_max}[/] | [bold blue]MP: {mp}/{mp_max}[/]",
        border_style="bright_blue",
        expand=False,
        padding=(1, 2),
    )

    console.print(
        Align(
            pantalla,
            align="center",
            vertical="middle",
            height=console.size.height,
        )
    )


# ─── Menú en juego ────────────────────────────────────────────────────────────


def pantalla_menu_en_juego(obtener_tecla_fn, contexto):
    """
    Menú de pausa en juego.
    - I  → abre el inventario completo (inventario.py)
    - V  → vuelve al juego
    - Q  → cierra el programa
    """
    en_menu = True
    while en_menu:
        os.system("cls" if os.name == "nt" else "clear")
        print("╔══════════════════════════╗")
        print("║     MENÚ DE OPCIONES     ║")
        print("╠══════════════════════════╣")
        print("║  I  →  Inventario        ║")
        print("║  V  →  Volver al juego   ║")
        print("║  Q  →  Salir             ║")
        print("╚══════════════════════════╝")

        opcion = obtener_tecla_fn()

        if opcion == TECLAS_ACCION[1]:  # i — inventario
            manejar_inventario(contexto["inventario"])

        elif opcion == "v":
            en_menu = False

        elif opcion == TECLAS_ACCION[2]:  # q — salir
            print("\nSaliendo del juego...")
            exit()  # TODO(estados): reemplazar exit() por devolver SALIR hacia el orquestador
