import os
import msvcrt
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from estados import SALIR

console = Console()


def manejar_victoria(contexto):
    """
    Entrada: Diccionario (contexto)
    Objetivo: cerrar la partida cuando el jugador gana el coliseo. La pantalla
        de campeon ya se mostro en el combate, asi que aca solo se marca el
        motivo de salida y se termina el juego.
    Salida: none. Modifica el contexto.
    """
    contexto["razon_salida"] = "victoria"
    contexto["estado_actual"] = SALIR


def manejar_game_over(contexto):
    """
    Entrada: Diccionario (contexto)
    Objetivo: mostrar la pantalla de game over y cerrar la partida.
    Salida: none. Modifica el contexto.
    """
    os.system("cls" if os.name == "nt" else "clear")
    console.print(Align(Panel(
        "\n[bold red]GAME OVER[/]\n\n"
        "[white]Tu aventura termina aquí.[/]\n\n"
        "[dim]Presioná cualquier tecla para salir...[/]\n",
        title="[bold red]💀 FIN[/]",
        border_style="red", expand=False, padding=(2, 6)
    ), align="center"))
    msvcrt.getch()
    contexto["razon_salida"] = "game_over"
    contexto["estado_actual"] = SALIR
