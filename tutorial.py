import os
import msvcrt
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

console = Console()


def mostrar_tutorial():
    """
    Objetivo: mostrar una pantalla con lo basico del juego (moverse, pelear,
        usar habilidades y juntar items) al empezar una partida nueva.
    Salida: none. Espera a que el jugador presione una tecla.
    """
    os.system("cls" if os.name == "nt" else "clear")
    texto = (
        "\n[bold yellow]CÓMO JUGAR[/]\n\n"
        "[white]Moverte:[/] W A S D\n"
        "[white]Abrir el menú en juego:[/] O\n\n"
        "[white]Combate:[/] al chocar con un enemigo entrás en batalla por turnos.\n"
        "Elegí una habilidad; cada una gasta MP.\n\n"
        "[white]Items:[/] caminá sobre un [bold]*[/] para recogerlo, abrí cofres\n"
        "y excavá tumbas con la pala. Usá pociones desde el inventario.\n\n"
        "[white]Objetivo:[/] llegá al Coliseo y ganá todos los rounds.\n\n"
        "[dim]Presioná cualquier tecla para empezar...[/]\n"
    )
    console.print(Align(Panel(
        texto, title="[bold green]TUTORIAL[/]",
        border_style="green", expand=False, padding=(1, 4)
    ), align="center"))
    msvcrt.getch()
