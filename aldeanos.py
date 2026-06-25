# aldeanos.py — NPCs comerciantes del mercado
#
# 3 aldeanos con quests:
#   "aldea_pala"   → El Vagabundo: regala la Pala Sagrada sin condición
#   "aldea_slime"  → Brotus el Alquimista: pide 5 Babas de Slime a cambio de una poción rara
#   "aldea_goblin" → Mordecai el Nigromante: pide 10 Cabezas de Goblin a cambio de un amuleto
#
# El resto son comerciantes de relleno con diálogos casuales.

import os
import msvcrt
from rich.console import Console
from rich.panel   import Panel
from rich.align   import Align

console = Console()

SIMBOLO_ALDEANO = "@"

# ─── IDs de items de quest ────────────────────────────────────────────────────
ID_PALA          = 50
ID_BABA_SLIME    = 51
ID_CABEZA_GOBLIN = 52

# ─── Recompensas de quest ─────────────────────────────────────────────────────
RECOMPENSA_SLIME = {
    "id_item": 60, "nombre": "Super Pocion de Curacion",
    "tipo": "consumible", "cantidad": 1, "equipado": False,
}
RECOMPENSA_GOBLIN = {
    "id_item": 61, "nombre": "Amuleto de la Fortuna",
    "tipo": "equipable", "cantidad": 1, "equipado": False,
}

# ─── Definición de aldeanos ───────────────────────────────────────────────────
ALDEANOS_MERCADO = [

    # ── QUEST: regala la pala ─────────────────────────────────────────────────
    {
        "id": "aldea_pala",
        "nombre": "El Vagabundo",
        "tipo": "quest_pala",
        "pos": None,
        "quest_completada": False,
        "dialogos_normal": [
            "...Eh, che, vos.",
            "Hacé algo bueno por tu vida.",
            "Agarrá esta pala. No sé para qué la tengo.",
            "Yo ya no excavo nada. Mis rodillas no aguantan.",
        ],
        "dialogo_ya_entregado": [
            "Ya te di la pala. No tengo más nada.",
            "Andate a excavar algo, muchacho.",
        ],
    },

    # ── QUEST: pide 5 babas de slime (repetible) ─────────────────────────────
    {
        "id": "aldea_slime",
        "nombre": "Brotus el Alquimista",
        "tipo": "quest_slime",
        "pos": None,
        "quest_completada": False,
        "dialogos_sin_items": [
            "¡Ah, un aventurero! Justo a tiempo.",
            "Por cada 5 Babas de Slime te doy una Super Pocion de Salud.",
            "Las conseguís matando slimes en el Prado.",
            "Volvé cuando tengas 5. O 10. O las que sean.",
        ],
        "dialogo_con_items": [
            "¡Tenés babas! Excelente.",
            "Tomá tu/s poción/es. Volvé cuando tengas más.",
        ],
        "dialogo_ya_completada": [
            "Siempre necesito más babas. Traé y te pago.",
        ],
    },

    # ── QUEST: pide 10 cabezas de goblin ─────────────────────────────────────
    {
        "id": "aldea_goblin",
        "nombre": "Mordecai el Nigromante",
        "tipo": "quest_goblin",
        "pos": None,
        "quest_completada": False,
        "dialogos_sin_items": [
            "Silencio... Acércate, mortal.",
            "Los goblins de la cueva profanan mis rituales.",
            "Tráeme 10 de sus cabezas y te daré poder.",
            "Las encontrarás en la cueva al norte del prado.",
        ],
        "dialogo_con_items": [
            "Las cabezas... perfectas. Las usaré bien.",
            "Toma el Amuleto de la Fortuna. Tu suerte aumentará en 50 puntos.",
        ],
        "dialogo_ya_completada": [
            "El ritual está en marcha. No me molestes.",
            "...Silencio.",
        ],
    },

    # ── RELLENO ───────────────────────────────────────────────────────────────
    {
        "id": "aldea_r1",
        "nombre": "Petra la Vendedora",
        "tipo": "relleno",
        "pos": None,
        "dialogos": [
            "¡Buen día! ¿Viste qué lindo clima hoy?",
            "Aunque para mañana dicen que llueve. Como siempre.",
        ],
    },
    {
        "id": "aldea_r2",
        "nombre": "Gundo el Carnicero",
        "tipo": "relleno",
        "pos": None,
        "dialogos": [
            "¿Viste el partido de ayer?",
            "Tres a uno. No lo puedo creer. Un desastre.",
        ],
    },
    {
        "id": "aldea_r3",
        "nombre": "Lina la Frutera",
        "tipo": "relleno",
        "pos": None,
        "dialogos": [
            "Las manzanas están caras este año.",
            "Todo está caro. Menos el peligro, ese está gratis.",
        ],
    },
    {
        "id": "aldea_r4",
        "nombre": "Viejo Ramón",
        "tipo": "relleno",
        "pos": None,
        "dialogos": [
            "En mis tiempos no había slimes en el prado.",
            "Ahora hay slimes, goblins y quién sabe qué más.",
            "¿A dónde vamos a parar?",
        ],
    },
    {
        "id": "aldea_r5",
        "nombre": "Tork el Mercader",
        "tipo": "relleno",
        "pos": None,
        "dialogos": [
            "¡Todo a mitad de precio! Bueno, no exactamente...",
            "El cofre que ves ahí lo traje de la cueva.",
            "No lo abras. En serio. Bueno, podés abrirlo.",
        ],
    },
    {
        "id": "aldea_r6",
        "nombre": "Nora la Costurera",
        "tipo": "relleno",
        "pos": None,
        "dialogos": [
            "¿Ese traje? Sí, tiene agujeros. Es la moda.",
            "La armadura perforada es lo que se usa ahora.",
        ],
    },
]

# ─── Registro ─────────────────────────────────────────────────────────────────
_registro_aldeanos = {}

def registrar_aldeano(aldeano):
    _registro_aldeanos[aldeano["id"]] = aldeano

def buscar_aldeano_en(pos, contexto):
    for ald in _registro_aldeanos.values():
        if ald["pos"] == list(pos):
            return ald
    return None

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _tecla():
    return msvcrt.getch().decode("utf-8", errors="ignore").lower()


def _panel_dialogo(nombre, texto, subtitulo=""):
    cuerpo = (
        f"[bold yellow]{nombre}[/]\n\n"
        f"[white]{texto}[/]"
        + (f"\n\n[dim]{subtitulo}[/]" if subtitulo else "")
    )
    return Panel(cuerpo, title="[bold green]DIÁLOGO[/]",
                 border_style="green", expand=False, padding=(1, 4))


def _mostrar_lineas(nombre, lineas):
    """Muestra una lista de líneas una a una. Cualquier tecla avanza, Q corta."""
    for linea in lineas:
        os.system("cls" if os.name == "nt" else "clear")
        console.print(Align(
            _panel_dialogo(nombre, linea, "Cualquier tecla para continuar... (Q salir)"),
            align="center"
        ))
        if _tecla() == "q":
            break


def _preguntar_interaccion(nombre):
    """Muestra '¿Hablar con [nombre]? (Y/N)' y devuelve True si Y."""
    os.system("cls" if os.name == "nt" else "clear")
    cuerpo = (
        f"[bold yellow]{nombre}[/]\n\n"
        f"[white]¿Querés hablar con este comerciante?[/]\n\n"
        f"[bold green]Y[/]  Sí     [bold red]N[/]  No"
    )
    console.print(Align(
        Panel(cuerpo, title="[bold green]INTERACCIÓN[/]",
              border_style="green", expand=False, padding=(1, 4)),
        align="center"
    ))
    t = ""
    while t not in ("y", "n"):
        t = _tecla()
    return t == "y"


def _contar_item(id_item, inventario):
    for it in inventario:
        if it["id_item"] == id_item:
            return it["cantidad"]
    return 0


def _quitar_items(id_item, cantidad, inventario):
    for i, it in enumerate(inventario):
        if it["id_item"] == id_item:
            it["cantidad"] -= cantidad
            if it["cantidad"] <= 0:
                inventario.pop(i)
            return True
    return False


def _dar_item(item, inventario):
    from inventario import agregar_item
    agregar_item(item, inventario)


def _pantalla_item_recibido(nombre_npc, item_nombre, mensaje_extra=""):
    os.system("cls" if os.name == "nt" else "clear")
    cuerpo = (
        f"[bold yellow]{nombre_npc}[/]\n\n"
        f"[white]{mensaje_extra}[/]\n\n"
        f"[bold cyan]Recibiste: {item_nombre}[/]\n\n"
        f"[dim]Presioná cualquier tecla...[/]"
    )
    console.print(Align(
        Panel(cuerpo, title="[bold cyan]ITEM RECIBIDO[/]",
              border_style="cyan", expand=False, padding=(1, 4)),
        align="center"
    ))
    _tecla()

# ─── Lógica de cada tipo de aldeano ──────────────────────────────────────────

def _interactuar_pala(aldeano, inventario):
    if aldeano["quest_completada"]:
        _mostrar_lineas(aldeano["nombre"], aldeano["dialogo_ya_entregado"])
        return
    _mostrar_lineas(aldeano["nombre"], aldeano["dialogos_normal"])
    # Entregar pala
    pala = {"id_item": ID_PALA, "nombre": "Pala Sagrada",
            "tipo": "clave", "cantidad": 1, "equipado": False}
    _dar_item(pala, inventario)
    aldeano["quest_completada"] = True
    _pantalla_item_recibido(
        aldeano["nombre"], "Pala Sagrada",
        "Con ella podés excavar las tumbas marcadas con ✦ en el cementerio."
    )


def _interactuar_slime(aldeano, inventario):
    """
    Quest repetible: cada 5 Babas de Slime → 1 Super Pocion de Salud.
    Nunca se marca como completada — Brotus siempre compra más.
    """
    tiene = _contar_item(ID_BABA_SLIME, inventario)
    if tiene >= 5:
        veces = tiene // 5           # cuántas pociones puede dar
        babas_a_quitar = veces * 5
        _mostrar_lineas(aldeano["nombre"], aldeano["dialogo_con_items"])
        _quitar_items(ID_BABA_SLIME, babas_a_quitar, inventario)
        for _ in range(veces):
            _dar_item(RECOMPENSA_SLIME.copy(), inventario)
        _pantalla_item_recibido(
            aldeano["nombre"],
            f"{veces}x {RECOMPENSA_SLIME['nombre']}",
            f"Brotus te entrega {veces} poción/es a cambio de {babas_a_quitar} babas.\n"
            "Llena tu HP por completo y aumenta tu HP máximo en 50."
        )
    else:
        faltante = 5 - tiene
        _mostrar_lineas(aldeano["nombre"], aldeano["dialogos_sin_items"])
        os.system("cls" if os.name == "nt" else "clear")
        cuerpo = (
            f"[bold yellow]{aldeano['nombre']}[/]\n\n"
            f"[white]Todavía te faltan [bold red]{faltante}[/] Babas de Slime.[/]\n"
            f"[dim]Tenés {tiene}/5.[/]\n\n"
            f"[dim]Presioná cualquier tecla...[/]"
        )
        console.print(Align(
            Panel(cuerpo, title="[bold green]QUEST[/]",
                  border_style="yellow", expand=False, padding=(1, 4)),
            align="center"
        ))
        _tecla()


def _interactuar_goblin(aldeano, inventario):
    if aldeano["quest_completada"]:
        _mostrar_lineas(aldeano["nombre"], aldeano["dialogo_ya_completada"])
        return
    tiene = _contar_item(ID_CABEZA_GOBLIN, inventario)
    if tiene >= 10:
        _mostrar_lineas(aldeano["nombre"], aldeano["dialogo_con_items"])
        _quitar_items(ID_CABEZA_GOBLIN, 10, inventario)
        _dar_item(RECOMPENSA_GOBLIN.copy(), inventario)
        aldeano["quest_completada"] = True
        _pantalla_item_recibido(
            aldeano["nombre"], RECOMPENSA_GOBLIN["nombre"],
            "Mordecai murmura algo ininteligible y te entrega el amuleto.\n+50 de Suerte (equipalo para activar el efecto)."
        )
    else:
        faltante = 10 - tiene
        _mostrar_lineas(aldeano["nombre"], aldeano["dialogos_sin_items"])
        os.system("cls" if os.name == "nt" else "clear")
        cuerpo = (
            f"[bold yellow]{aldeano['nombre']}[/]\n\n"
            f"[white]Todavía te faltan [bold red]{faltante}[/] Cabezas de Goblin.[/]\n"
            f"[dim]Tenés {tiene}/10.[/]\n\n"
            f"[dim]Presioná cualquier tecla...[/]"
        )
        console.print(Align(
            Panel(cuerpo, title="[bold green]QUEST[/]",
                  border_style="yellow", expand=False, padding=(1, 4)),
            align="center"
        ))
        _tecla()


# ─── Punto de entrada ─────────────────────────────────────────────────────────

def mostrar_dialogo(aldeano, inventario):
    """
    Llamado desde jugador.py al intentar moverse sobre un '@'.
    Primero pregunta Y/N, luego ejecuta la lógica según el tipo.
    """
    if not _preguntar_interaccion(aldeano["nombre"]):
        return   # jugador dijo N

    tipo = aldeano["tipo"]

    if tipo == "quest_pala":
        _interactuar_pala(aldeano, inventario)
    elif tipo == "quest_slime":
        _interactuar_slime(aldeano, inventario)
    elif tipo == "quest_goblin":
        _interactuar_goblin(aldeano, inventario)
    else:
        # Relleno: solo muestra los diálogos
        _mostrar_lineas(aldeano["nombre"], aldeano["dialogos"])
