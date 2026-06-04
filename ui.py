# ui.py — Renderizado con Rich y menú en juego

import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

from config import (
<<<<<<< HEAD
    CAMARA_ALTO, CAMARA_ANCHO,
    MAPA_REAL_ALTO, MAPA_REAL_ANCHO,
    ESTILOS, TECLAS_ACCION,
)
from inventario import manejar_inventario
from mapa_cueva import CUEVA_ALTO, CUEVA_ANCHO
from mapa_coliseo import COLISEO_ALTO, COLISEO_ANCHO
=======
    CAMARA_ALTO,
    CAMARA_ANCHO,
    MAPA_REAL_ALTO,
    MAPA_REAL_ANCHO,
    ESTILOS,
    TECLAS_ACCION,
)
from inventario import manejar_inventario
from estados import SALIR
>>>>>>> origin/integracion_40

console = Console()

NOMBRES_MAPA = {1: "Mercado", 2: "Prado", 3: "Cementerio", 4: "Cueva", 5: "Coliseo"}


<<<<<<< HEAD
def dibujar_juego_centrado(contexto):
    os.system('cls' if os.name == 'nt' else 'clear')

    mundo       = contexto["mundo"]
    pos_p       = mundo["pos_p"]
    mapa_actual = mundo["mapa_actual"]
    n           = mundo["numero_mapa"]
    p           = contexto["personaje"]
    hp          = p["stats_actuales"]["hp"]
    mp          = p["stats_actuales"]["mp"]
    hp_max      = p["stats_base"]["hp"]
    mp_max      = p["stats_base"]["mp"]

    if n == 4:
        cam_alto, cam_ancho = 15, 30
        m_alto,   m_ancho  = CUEVA_ALTO, CUEVA_ANCHO
    elif n == 5:
        cam_alto, cam_ancho = 20, 40
        m_alto,   m_ancho  = COLISEO_ALTO, COLISEO_ANCHO
    else:
        cam_alto, cam_ancho = CAMARA_ALTO, CAMARA_ANCHO
        m_alto,   m_ancho  = MAPA_REAL_ALTO, MAPA_REAL_ANCHO
=======

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
>>>>>>> origin/integracion_40

    inicio_f = max(0, min(pos_p[0] - cam_alto  // 2, m_alto  - cam_alto))
    inicio_c = max(0, min(pos_p[1] - cam_ancho // 2, m_ancho - cam_ancho))

    filas = []
    for f in range(inicio_f, inicio_f + cam_alto):
        fila_str = ""
<<<<<<< HEAD
        for c in range(inicio_c, inicio_c + cam_ancho):
            char  = mapa_actual[f][c]
=======
        for c in range(inicio_c, inicio_c + CAMARA_ANCHO):
            char = mapa_actual[f][c]
>>>>>>> origin/integracion_40
            color = ESTILOS.get(char, "white")
            fila_str += f"[{color}]{char}[/] "
        filas.append(fila_str)

<<<<<<< HEAD
    nombre_mapa = NOMBRES_MAPA.get(n, "?")
    titulo = f"[bold yellow]GLASSTION · {nombre_mapa} — {p['nombre']} ({p['clase']})[/]"

    pantalla = Panel(
        "\n".join(filas),
        title    = titulo,
        subtitle = f"[bold red]HP: {hp}/{hp_max}[/] | [bold blue]MP: {mp}/{mp_max}[/]",
        border_style = "bright_blue",
        expand   = False,
        padding  = (1, 2),
    )
    console.print(Align(pantalla, align="center", vertical="middle",
                        height=console.size.height))


def pantalla_menu_en_juego(obtener_tecla_fn, contexto):
=======
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
>>>>>>> origin/integracion_40
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

<<<<<<< HEAD
        if opcion == TECLAS_ACCION[1]:
            manejar_inventario(contexto["inventario"])
        elif opcion == "v":
            en_menu = False
        elif opcion == TECLAS_ACCION[2]:
            print("\nSaliendo del juego...")
            exit()
=======
        if opcion == TECLAS_ACCION[1]:  # i — inventario
            manejar_inventario(contexto["inventario"])

        elif opcion == "v":
            en_menu = False

        elif opcion == TECLAS_ACCION[2]:  # q — salir
            contexto["estado_actual"] = SALIR
            en_menu = False
>>>>>>> origin/integracion_40
