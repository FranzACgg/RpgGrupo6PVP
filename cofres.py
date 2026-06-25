# cofres.py — Cofres interactuables que dan item aleatorio (bueno o malo)

import os
import random
import msvcrt
from rich.console import Console
from rich.panel   import Panel
from rich.align   import Align

from catalogo import item_aleatorio

console = Console()

SIMBOLO_COFRE = "C"   # ya existía en mapa_cueva; también se usará en mercado

# ─── Items especiales de tumba ────────────────────────────────────────────────
# Se obtienen solo excavando tumbas ✦ con la Pala Sagrada
ITEMS_TUMBA = [
    {"id_item": 30, "nombre": "Amuleto de Hueso",       "tipo": "equipable",  "cantidad": 1, "equipado": False},
    {"id_item": 31, "nombre": "Anillo del Rey Muerto",   "tipo": "equipable",  "cantidad": 1, "equipado": False},
    {"id_item": 32, "nombre": "Poción de Resurrección",  "tipo": "consumible", "cantidad": 1, "equipado": False},
    {"id_item": 33, "nombre": "Espada del Espectro",     "tipo": "equipable",  "cantidad": 1, "equipado": False},
    {"id_item": 34, "nombre": "Tótem Maldito",           "tipo": "consumible", "cantidad": 1, "equipado": False},
    {"id_item": 35, "nombre": "Corona Rota",             "tipo": "equipable",  "cantidad": 1, "equipado": False},
]

# ─── Loot de cofres normales (item aleatorio del catálogo) ──────────────

def _loot_cofre_aleatorio():
    """Devuelve un item aleatorio del catálogo."""
    return item_aleatorio()


# ─── Abrir cofre ─────────────────────────────────────────────────────────────

def _obtener_tecla():
    """
    Objetivo: leer una tecla del teclado sin eco en la consola (bloquea hasta
        que el usuario presiona una tecla)
    Salida: String con el caracter en minuscula, o cadena vacia si el byte
        no es decodificable como UTF-8
    """
    return msvcrt.getch().decode("utf-8", errors="ignore").lower()


def abrir_cofre(inventario, mapa, pos_cofre):
    """
    Muestra animación de apertura, da un item aleatorio (bueno o malo) y
    reemplaza el símbolo 'C' del mapa por el símbolo de piso correspondiente.

    Parámetros:
        inventario : lista del contexto
        mapa       : mapa_actual del contexto
        pos_cofre  : [fila, col] del cofre en el mapa
    """
    from inventario import agregar_item

    item = _loot_cofre_aleatorio()
    agregar_item(item, inventario)

    # Reemplazar cofre en el mapa (para que no se pueda abrir dos veces)
    f, c = pos_cofre
    mapa[f][c] = "."   # piso de cueva, o se puede usar "░" si es mercado

    os.system("cls" if os.name == "nt" else "clear")
    bueno = "buenas" in item.get("nombre", "").lower() or item["id_item"] <= 9
    color = "bold green" if item["id_item"] <= 9 else "bold red"
    rareza = "¡Item encontrado!" if item["id_item"] <= 9 else "Hmm... esto no parece muy útil."

    cuerpo = (
        f"[bold yellow]COFRE ABIERTO[/]\n\n"
        f"[white]Dentro del cofre encuentras algo...[/]\n\n"
        f"[{color}]{rareza}[/]\n"
        f"[bold white]→ {item['nombre']}[/]\n\n"
        f"[dim]Presioná cualquier tecla...[/]"
    )
    panel = Panel(cuerpo, title="[bold yellow]⬛ COFRE[/]",
                  border_style="yellow", expand=False, padding=(1, 4))
    console.print(Align(panel, align="center"))
    _obtener_tecla()


# ─── Excavar tumba con Pala Sagrada ──────────────────────────────────────────

SIMBOLO_TUMBA_EXCAVABLE = "✦"   # tumba especial marcada en el mapa


def tiene_pala(inventario):
    """
    Entrada: Lista
    Params:
        inventario: Lista con todos los items en el inventario
    Objetivo: comprobar si el jugador tiene la Pala Sagrada (id 50)
    Salida: True si la tiene, False si no
    """
    for it in inventario:
        if it["id_item"] == 50:
            return True
    return False


def excavar_tumba(inventario, mapa, pos_tumba):
    """
    Excava una tumba marcada con ✦ si el jugador tiene la Pala Sagrada.
    Da un item de ITEMS_TUMBA y reemplaza ✦ por '🪦' (tumba normal ya excavada).
    """
    from inventario import agregar_item

    os.system("cls" if os.name == "nt" else "clear")

    if not tiene_pala(inventario):
        cuerpo = (
            "[white]La tumba está sellada...\n\n"
            "Necesitarías algo para excavar.[/]\n\n"
            "[dim]Presioná cualquier tecla...[/]"
        )
        panel = Panel(cuerpo, title="[bold white]TUMBA[/]",
                      border_style="white", expand=False, padding=(1, 4))
        console.print(Align(panel, align="center"))
        _obtener_tecla()
        return

    item = random.choice(ITEMS_TUMBA).copy()
    agregar_item(item, inventario)

    # Marcar como ya excavada
    f, c = pos_tumba
    mapa[f][c] = "🪦"

    cuerpo = (
        f"[bold yellow]TUMBA EXCAVADA[/]\n\n"
        f"[white]Cavás con la Pala Sagrada...\n"
        f"Tus manos tocan algo frío.[/]\n\n"
        f"[bold cyan]→ {item['nombre']}[/]\n\n"
        f"[dim]Presioná cualquier tecla...[/]"
    )
    panel = Panel(cuerpo, title="[bold yellow]⬛ TUMBA[/]",
                  border_style="cyan", expand=False, padding=(1, 4))
    console.print(Align(panel, align="center"))
    _obtener_tecla()
