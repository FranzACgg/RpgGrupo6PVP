import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.console import Console, Group

# Mantenemos tu lógica de ingeniería
# $calcular\_vidas(i, p) = i - p$
calcular_vidas = lambda iniciales, perdidas: iniciales - perdidas

console = Console()

def obtener_contenido_titulo():
    """Genera el string con formato para el menú"""
    logo = (
        "[bold cyan]"
        "  _____  _               _____  _____ _______ _____ ____  _   _ \n"
        " / ____|| |        /\\   / ____|/ ____|__   __|_   _/ __ \\| \\ | |\n"
        "| |  __ | |       /  \\ | (___ | (___    | |    | || |  | |  \\| |\n"
        "| | |_ || |      / /\\ \\ \\___ \\ \\___ \\   | |    | || |  | | . ` |\n"
        "| |__| || |____ / ____ \\____) |____) |  | |   _| || |__| | |\\  |\n"
        " \\_____||______/_/    \\_\\_____/|_____/   |_|  |_____\\____/|_| \\_|\n"
        "[/]"
    )
    return logo 
def obtener_contenido_principal():
    return "\n\n[bold white][1] EMPEZAR[/]\n[bold white][2] SALIR[/]"


def menu_principal():
    ejecutando = True
    
    while ejecutando:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # 1. Preparamos el contenido del título (Logo)
        contenido_logo = obtener_contenido_titulo()
        
        # 2. Creamos el Panel PEQUEÑO (el de las opciones)
        contenido_opciones = "[bold white][1] EMPEZAR[/]\n[bold white][2] SALIR[/]"
        panel_opciones = Panel(
            Align.center(contenido_opciones, vertical="middle"),
            border_style="bright_magenta",
            expand=False,
            width=25,
            height=5
        )

        # 3. CREAMOS EL GRUPO INTERNO
        # Este grupo junta el logo y el panel de opciones
        render_interno = Group(
            Align.center(contenido_logo),
            "\n", # Espacio entre logo y opciones
            Align.center(panel_opciones)
        )

        # 4. Creamos el Panel GRANDE que envuelve a todo lo anterior
        pantalla_completa = Panel(
            Align.center(render_interno, vertical="middle"),
            title="[bold yellow]══ GLASSTION ══[/]",
            subtitle="[italic grey70]Seleccione su destino[/]",
            border_style="bright_blue",
            width=80,
            height=22, # Aumentamos un poquito el alto para que quepa todo cómodo
            padding=(1, 2)
        )

        # 5. Imprimimos el resultado final centrado en la terminal
        console.print(Align(pantalla_completa, align="center", vertical="middle", height=console.size.height))
        # 5. Input
        seleccion = input("\n > ").strip()
        
        if seleccion == "1":
            vidas = calcular_vidas(3, 0)
            console.print(f"\n[bold green]DESPERTANDO... Vidas: {vidas}[/]")
            time.sleep(2)
            ejecutando = False 
            capa_color_mapa.iniciar_mapa_recoleccion()
        elif seleccion == "2":
            console.print("[bold red]Saliendo...[/]")
            ejecutando = False
        else:
            console.print("[bold red][!] Opción no válida[/]")
            time.sleep(1)

if __name__ == "__main__":
    menu_principal()
    
