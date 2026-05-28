# pantalla_batalla.py — Sistema de combate por turnos (RPG) v3
#
#  Mejoras sobre v2:
#  ─ Stats completos del personaje en el panel (fuerza, defensa, agilidad, suerte…)
#  ─ Bonificaciones de items equipados mostradas como +X en verde
#  ─ Esquiva del jugador y del enemigo según agilidad (texto en pantalla)
#  ─ Tipo de habilidad mostrado por texto ("Ataque físico", "Maldición", etc.)
#  ─ Stats y habilidades del enemigo (slime / goblin) integrados
#  ─ Items consumibles usables en batalla (curan HP/MP)
#  ─ Habilidades de personaje funcionales en batalla
#  ─ Habilidades especiales de mobs (Disparo Ácido, Modo Berserker, etc.)

import os
import random

from rich.console  import Console
from rich.panel    import Panel
from rich.columns  import Columns
from rich.align    import Align
from rich.text     import Text
from rich.table    import Table

from config import estado

console = Console()

# ─── ASCII art de enemigos ────────────────────────────────────────────────────

ASCII_SLIME = r"""
      .-~~~~-.
     /  o  o  \
    |    __    |
     \  \__/  /
      `------'
        (ζ)
"""

ASCII_GOBLIN = r"""
      _____
   <=( +.+ )=>
      [ O ]
     /|   |\
    o L   L o
"""

ASCII_DEFAULT = r"""
      ?????
     (     )
      \   /
       ---
"""

ARTE_ENEMIGO = {
    "ζ": ASCII_SLIME,
    "G": ASCII_GOBLIN,
}

# ─── Stats de enemigos ────────────────────────────────────────────────────────

STATS_ENEMIGOS = {
    "ζ": {   # Slime
        "nombre"    : "Slime",
        "hp_max"    : 50,
        "fuerza"    : 10,
        "defensa"   : 5,
        "agilidad"  : 20,   # % de probabilidad de esquivar
        "habilidades": [
            {
                "nombre"     : "Disparo Ácido",
                "tipo"       : "Ataque",
                "descripcion": "Disparo ácido que hace el doble de daño",
                "valor"      : 2.0,   # multiplicador
                "probabilidad": 30,
            },
            {
                "nombre"      : "Cuerpo Ácido",
                "tipo"        : "Maldición",
                "descripcion" : "20% de probabilidad de destruir un arma equipada",
                "valor"       : 0,
                "probabilidad": 20,
            },
        ],
    },
    "G": {   # Goblin
        "nombre"    : "Goblin",
        "hp_max"    : 100,
        "fuerza"    : 20,
        "defensa"   : 8,
        "agilidad"  : 15,   # % de probabilidad de esquivar
        "habilidades": [
            {
                "nombre"      : "Daga Rompe Escudos",
                "tipo"        : "Maldición",
                "descripcion" : "Reduce a 0 el bono de defensa del escudo equipado",
                "valor"       : 0,
                "probabilidad": 35,
            },
            {
                "nombre"      : "Modo Berserker",
                "tipo"        : "Ataque",
                "descripcion" : "40% de atacar 2 veces, 20% de atacar 3 veces",
                "valor"       : 1.0,
                "probabilidad": 60,
            },
        ],
    },
}

# ─── Catálogo de items (efectos en stats) ────────────────────────────────────
#  Cada item equipable puede tener "bonus_stats": {stat: valor}
#  Los items consumibles tienen "efecto": {"hp": X, "mp": X}

CATALOGO_ITEMS = {
    1:  {"nombre": "Pocion de Fuerza Grande",          "tipo": "consumible", "efecto": {"fuerza": 20}},
    2:  {"nombre": "Pocion de HP pequeña",             "tipo": "consumible", "efecto": {"hp": 50}},
    3:  {"nombre": "Pocion de HP Grande",              "tipo": "consumible", "efecto": {"hp": 100}},
    4:  {"nombre": "Gema de vida",                     "tipo": "equipable",  "bonus_stats": {"hp": 30}},
    5:  {"nombre": "Hacha de Mitril",                  "tipo": "equipable",  "bonus_stats": {"fuerza": 25}},
    6:  {"nombre": "Latigo con Puas",                  "tipo": "equipable",  "bonus_stats": {"fuerza": 15, "agilidad": 10}},
    7:  {"nombre": "Escudo de Obsidiana",              "tipo": "equipable",  "bonus_stats": {"defensa": 30}},
    8:  {"nombre": "Casco de Tungsteno",               "tipo": "equipable",  "bonus_stats": {"defensa": 15, "hp": 20}},
    9:  {"nombre": "Pechera de escamas de Dragon",     "tipo": "equipable",  "bonus_stats": {"defensa": 40, "hp": 50}},
    10: {"nombre": "Pocion Alucinogena",               "tipo": "consumible", "efecto": {"mp": -30, "hp": -20}},
    11: {"nombre": "Pocion de Potencia/Impotencia",    "tipo": "consumible", "efecto": {"fuerza": 30}},  # al azar ±
    12: {"nombre": "Pocion de I have no enemies",      "tipo": "consumible", "efecto": {"defensa": -50}},
    13: {"nombre": "Escudo del Héroe ;)",              "tipo": "equipable",  "bonus_stats": {"defensa": -10}},
    14: {"nombre": "Lanza Maldita",                    "tipo": "equipable",  "bonus_stats": {"fuerza": 35, "hp": -30}},
    15: {"nombre": "Espada de Doble Filo Maldita",     "tipo": "equipable",  "bonus_stats": {"fuerza": 50, "defensa": -20}},
    16: {"nombre": "Collar Paralizante",               "tipo": "equipable",  "bonus_stats": {"agilidad": -15}},
    17: {"nombre": "Guantes Benevolentes",             "tipo": "equipable",  "bonus_stats": {"fuerza": -20}},
    18: {"nombre": "Casco de Dullahan",                "tipo": "equipable",  "bonus_stats": {"defensa": 20, "suerte": 15}},
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _barra(actual, maximo, largo=12):
    llenos = round((actual / maximo) * largo) if maximo > 0 else 0
    vacios  = largo - llenos
    return "█" * llenos + "░" * vacios


def _calcular_stats_con_items(personaje, inventario):
    """Retorna dict con stats base + bonus de items equipados."""
    clase = personaje.get("clase", "")
    from personajes import CLASES_DISPONIBLES
    base = CLASES_DISPONIBLES.get(clase, {}).get("stats_base", {}).copy()

    # Asegurar que todos los stats existen
    for s in ("fuerza", "defensa", "agilidad", "suerte", "magia", "espiritu"):
        base.setdefault(s, 0)

    bonus = {s: 0 for s in base}

    items_equipados = [it for it in inventario if it.get("equipado")]
    for it in items_equipados:
        info = CATALOGO_ITEMS.get(it["id_item"], {})
        for stat, val in info.get("bonus_stats", {}).items():
            bonus[stat] = bonus.get(stat, 0) + val

    return base, bonus, items_equipados


def _intentar_esquivar(agilidad):
    """Devuelve True si el personaje/enemigo esquiva según su agilidad (%)."""
    return random.randint(1, 100) <= agilidad


def _tipo_habilidad_texto(tipo):
    textos = {
        "Ataque"  : "⚔️  Ataque",
        "Defensa" : "🛡️  Defensa",
        "Mejora"  : "✨ Mejora",
        "Maldicion": "💀 Maldición",
        "Maldición": "💀 Maldición",
        "Curación": "💚 Curación",
    }
    return textos.get(tipo, tipo)

# ─── Paneles de la UI ────────────────────────────────────────────────────────

def _panel_enemigo(simbolo, stats_mob, hp_actual):
    arte = ARTE_ENEMIGO.get(simbolo, ASCII_DEFAULT)
    nombre = stats_mob["nombre"]
    hp_max = stats_mob["hp_max"]
    barra  = _barra(hp_actual, hp_max)

    contenido = (
        f"[bold green]{arte}[/]\n"
        f"[bold white]{nombre}[/]\n"
        f"[red]HP  {barra}  {hp_actual}/{hp_max}[/]\n"
        f"[dim]FUE:{stats_mob['fuerza']}  DEF:{stats_mob['defensa']}  AGI:{stats_mob['agilidad']}%[/]"
    )
    return Panel(
        contenido,
        title=f"[bold green]ENEMIGO — {nombre}[/]",
        border_style="green",
        expand=True,
        padding=(1, 4),
    )


def _panel_stats_jugador(inventario, escudo_roto=False):
    """Panel con stats completos + bonificaciones de items equipados."""
    p      = estado["personaje"]
    hp     = estado["hp"]
    hp_max = estado["hp_max"]
    mp     = estado["mp"]
    mp_max = estado["mp_max"]

    nombre = p["nombre"] if p else "Héroe"
    clase  = p["clase"]  if p else ""

    base, bonus, _ = _calcular_stats_con_items(p, inventario) if p else ({}, {}, [])

    barra_hp = _barra(hp, hp_max)
    barra_mp = _barra(mp, mp_max)

    def stat_linea(nombre_stat, key):
        b  = base.get(key, 0)
        bx = bonus.get(key, 0)
        if escudo_roto and key == "defensa":
            bx = 0
        if bx > 0:
            bonus_str = f" [bold green](+{bx})[/]"
        elif bx < 0:
            bonus_str = f" [bold red]({bx})[/]"
        else:
            bonus_str = ""
        return f"[dim]{nombre_stat:<10}[/] [white]{b + bx}[/]{bonus_str}"

    lineas = [
        f"[bold white]{nombre}[/]  [dim]{clase}[/]\n",
        f"[red]HP  {barra_hp}  {hp}/{hp_max}[/]",
        f"[blue]MP  {barra_mp}  {mp}/{mp_max}[/]\n",
        stat_linea("Fuerza",   "fuerza"),
        stat_linea("Defensa",  "defensa"),
        stat_linea("Agilidad", "agilidad"),
        stat_linea("Suerte",   "suerte"),
        stat_linea("Magia",    "magia"),
        stat_linea("Espiritu", "espiritu"),
    ]

    if escudo_roto:
        lineas.append("\n[bold red]⚠ Escudo roto![/]")

    return Panel(
        "\n".join(lineas),
        title="[bold green]PERSONAJE[/]",
        border_style="green",
        expand=True,
        padding=(1, 2),
    )


def _panel_opciones(cursor):
    opciones = [
        ("1", "Luchar"),
        ("2", "Habilidades"),
        ("3", "Ítems"),
        ("4", "Escapar"),
    ]
    lineas = []
    for i, (tecla, texto) in enumerate(opciones):
        if i == cursor:
            lineas.append(f"[bold green]▶ [{tecla}] {texto}[/]")
        else:
            lineas.append(f"[dim]  [{tecla}] {texto}[/]")

    return Panel(
        "\n".join(lineas),
        title="[bold green]ACCIONES[/]",
        border_style="green",
        expand=True,
        padding=(1, 2),
    )


def _panel_habilidades(personaje, cursor_hab):
    if not personaje:
        return Panel("[dim]Sin habilidades[/]", title="HABILIDADES", border_style="green")

    lineas = []
    for i, hab in enumerate(personaje.get("habilidades", [])):
        mp_ok = estado["mp"] >= hab["costo_mp"]
        color = "white" if mp_ok else "red"
        marca = "▶ " if i == cursor_hab else "  "
        tipo_txt = _tipo_habilidad_texto(hab["tipo"])
        lineas.append(
            f"[{color}]{marca}[bold]{hab['nombre']}[/bold]\n"
            f"      {tipo_txt}  | MP:{hab['costo_mp']}  | {hab['probabilidad']}% éxito[/]"
        )

    return Panel(
        "\n".join(lineas),
        title="[bold green]HABILIDADES[/]",
        border_style="cyan",
        expand=True,
        padding=(1, 2),
    )


def _panel_items_batalla(inventario, cursor_item):
    consumibles = [it for it in inventario if it["tipo"] == "consumible"]
    if not consumibles:
        return Panel("[dim]Sin consumibles[/]", title="ÍTEMS", border_style="green")

    lineas = []
    for i, it in enumerate(consumibles):
        marca = "▶ " if i == cursor_item else "  "
        info  = CATALOGO_ITEMS.get(it["id_item"], {})
        efecto_str = ", ".join(f"{k}+{v}" if v > 0 else f"{k}{v}"
                               for k, v in info.get("efecto", {}).items())
        lineas.append(f"[white]{marca}{it['nombre']} x{it['cantidad']}[/] [dim]{efecto_str}[/]")

    return Panel(
        "\n".join(lineas),
        title="[bold green]ÍTEMS[/]",
        border_style="yellow",
        expand=True,
        padding=(1, 2),
    )

# ─── Renderizado principal ────────────────────────────────────────────────────

def renderizar_batalla(simbolo_enemigo, stats_mob, hp_enemigo,
                       cursor=0, mensaje="", inventario=None,
                       modo="menu", cursor_sec=0, escudo_roto=False):
    if inventario is None:
        inventario = []

    os.system('cls' if os.name == 'nt' else 'clear')

    panel_enemigo  = _panel_enemigo(simbolo_enemigo, stats_mob, hp_enemigo)
    panel_stats    = _panel_stats_jugador(inventario, escudo_roto)

    if modo == "habilidades":
        panel_der = _panel_habilidades(estado.get("personaje"), cursor_sec)
    elif modo == "items":
        panel_der = _panel_items_batalla(inventario, cursor_sec)
    else:
        panel_der = _panel_opciones(cursor)

    console.print(Align(panel_enemigo, align="center"))
    console.print(Columns([panel_stats, panel_der], expand=True))

    if mensaje:
        console.print(Align(f"[bold yellow]>> {mensaje}[/]", align="center"))

# ─── Lógica de combate ────────────────────────────────────────────────────────

def _daño_jugador(inventario, escudo_roto):
    """Calcula el daño base del jugador con items equipados."""
    p = estado.get("personaje")
    if not p:
        return 10
    base, bonus, _ = _calcular_stats_con_items(p, inventario)
    fuerza = base.get("fuerza", 10) + bonus.get("fuerza", 0)
    return max(1, fuerza)


def _daño_enemigo(stats_mob, inventario, escudo_roto):
    """Calcula el daño que hace el mob reducido por defensa del jugador."""
    p = estado.get("personaje")
    base, bonus, _ = _calcular_stats_con_items(p, inventario) if p else ({}, {}, [])
    defensa = base.get("defensa", 0) + (0 if escudo_roto else bonus.get("defensa", 0))
    dano_bruto = stats_mob.get("fuerza", 10)
    return max(1, dano_bruto - defensa)


def _agilidad_jugador(inventario):
    p = estado.get("personaje")
    if not p:
        return 0
    base, bonus, _ = _calcular_stats_con_items(p, inventario)
    return base.get("agilidad", 0) + bonus.get("agilidad", 0)


def _turno_mob(stats_mob, inventario, escudo_roto, obtener_tecla_fn,
               simbolo, hp_enemigo, hp_max):
    """Ejecuta el turno del mob (puede usar habilidad especial) y devuelve mensaje."""
    mensajes = []

    # ¿El mob esquiva primero? No aplica — el mob ataca
    # Intentar habilidad especial (probabilidad independiente)
    habilidades = stats_mob.get("habilidades", [])
    hab_usada = None
    for hab in habilidades:
        if random.randint(1, 100) <= hab["probabilidad"]:
            hab_usada = hab
            break

    golpes = 1
    if hab_usada:
        tipo_txt = _tipo_habilidad_texto(hab_usada["tipo"])
        mensajes.append(f"[bold magenta]{stats_mob['nombre']} usa {hab_usada['nombre']} ({tipo_txt})![/]")

        if hab_usada["nombre"] == "Disparo Ácido":
            dano = _daño_enemigo(stats_mob, inventario, escudo_roto) * 2
            # ¿Jugador esquiva?
            if _intentar_esquivar(_agilidad_jugador(inventario)):
                mensajes.append("[bold cyan]¡Esquivaste el Disparo Ácido![/]")
                dano = 0
            else:
                estado["hp"] = max(0, estado["hp"] - int(dano))
                mensajes.append(f"[red]Recibiste {int(dano)} de daño ácido![/]")

        elif hab_usada["nombre"] == "Cuerpo Ácido":
            items_eq = [it for it in inventario if it.get("equipado") and it["tipo"] == "equipable"]
            if items_eq:
                destruida = random.choice(items_eq)
                destruida["equipado"] = False
                mensajes.append(f"[bold red]¡{destruida['nombre']} fue destruida por el ácido![/]")
            else:
                mensajes.append("[dim]El Cuerpo Ácido no encontró arma equipada.[/]")

        elif hab_usada["nombre"] == "Daga Rompe Escudos":
            return mensajes, True   # escudo_roto = True

        elif hab_usada["nombre"] == "Modo Berserker":
            tirada = random.randint(1, 100)
            golpes = 3 if tirada <= 20 else 2
            mensajes.append(f"[bold red]¡Modo Berserker! El Goblin ataca {golpes} veces![/]")

    # Ataque(s) normal(es)
    for g in range(golpes):
        if hab_usada and hab_usada["nombre"] == "Disparo Ácido":
            break   # ya se procesó
        dano = _daño_enemigo(stats_mob, inventario, escudo_roto)
        if _intentar_esquivar(_agilidad_jugador(inventario)):
            mensajes.append(f"[bold cyan]¡Esquivaste el ataque{'s'[g==0:]}![/]")
        else:
            estado["hp"] = max(0, estado["hp"] - dano)
            mensajes.append(f"[red]Recibiste {dano} de daño.[/]")

    return mensajes, escudo_roto


# ─── Loop principal de batalla ────────────────────────────────────────────────

def iniciar_batalla(simbolo_enemigo, nombre_enemigo, hp_max_enemigo, obtener_tecla_fn,
                    inventario=None):
    """
    Gestiona el loop de batalla completo.
    Retorna True si el jugador ganó, False si escapó o murió.
    """
    if inventario is None:
        inventario = estado.get("inventario", [])

    stats_mob  = STATS_ENEMIGOS.get(simbolo_enemigo, {
        "nombre": nombre_enemigo, "hp_max": hp_max_enemigo,
        "fuerza": 15, "defensa": 5, "agilidad": 10, "habilidades": []
    })
    stats_mob["nombre"] = nombre_enemigo
    hp_enemigo   = hp_max_enemigo
    cursor       = 0
    mensaje      = ""
    escudo_roto  = False
    modo         = "menu"
    cursor_sec   = 0   # cursor de habilidades o items

    while True:
        renderizar_batalla(simbolo_enemigo, stats_mob, hp_enemigo,
                           cursor, mensaje, inventario, modo, cursor_sec, escudo_roto)
        mensaje = ""

        tecla = obtener_tecla_fn()

        # ── Menú secundario: habilidades ──────────────────────────────────────
        if modo == "habilidades":
            habilidades = (estado.get("personaje") or {}).get("habilidades", [])
            if tecla == 'w':
                cursor_sec = (cursor_sec - 1) % max(1, len(habilidades))
            elif tecla == 's':
                cursor_sec = (cursor_sec + 1) % max(1, len(habilidades))
            elif tecla in ('\r', ' ', 'e'):
                if habilidades:
                    hab = habilidades[cursor_sec]
                    if estado["mp"] < hab["costo_mp"]:
                        mensaje = f"[red]Sin MP para {hab['nombre']}.[/]"
                    else:
                        tipo_txt = _tipo_habilidad_texto(hab["tipo"])
                        estado["mp"] -= hab["costo_mp"]
                        tirada  = random.randint(1, 100)
                        exito   = tirada <= hab["probabilidad"]
                        if exito:
                            dano_hab = _daño_jugador(inventario, escudo_roto) + hab.get("valor", 0)
                            # ¿Mob esquiva?
                            if _intentar_esquivar(stats_mob.get("agilidad", 0)):
                                mensaje = f"[cyan]{stats_mob['nombre']} esquivó {hab['nombre']}![/]"
                            else:
                                hp_enemigo -= int(dano_hab)
                                mensaje = (f"[bold]{hab['nombre']}[/] ({tipo_txt}) "
                                           f"¡Éxito! {int(dano_hab)} daño.")
                        else:
                            mensaje = f"{hab['nombre']} falló (tirada {tirada} > {hab['probabilidad']}%)."

                        # Turno del mob
                        msgs_mob, escudo_roto = _turno_mob(
                            stats_mob, inventario, escudo_roto,
                            obtener_tecla_fn, simbolo_enemigo, hp_enemigo, hp_max_enemigo)
                        mensaje += " | " + " ".join(msgs_mob)
                        modo = "menu"
            elif tecla in ('q', '\x1b'):
                modo = "menu"

        # ── Menú secundario: items ────────────────────────────────────────────
        elif modo == "items":
            consumibles = [it for it in inventario if it["tipo"] == "consumible"]
            if tecla == 'w':
                cursor_sec = (cursor_sec - 1) % max(1, len(consumibles))
            elif tecla == 's':
                cursor_sec = (cursor_sec + 1) % max(1, len(consumibles))
            elif tecla in ('\r', ' ', 'e'):
                if consumibles:
                    it   = consumibles[cursor_sec]
                    info = CATALOGO_ITEMS.get(it["id_item"], {})
                    efectos = info.get("efecto", {})
                    partes  = []
                    for stat, val in efectos.items():
                        if stat == "hp":
                            estado["hp"] = min(estado["hp_max"], estado["hp"] + val)
                            partes.append(f"HP {'+'if val>0 else ''}{val}")
                        elif stat == "mp":
                            estado["mp"] = min(estado["mp_max"], estado["mp"] + val)
                            partes.append(f"MP {'+'if val>0 else ''}{val}")
                    # consumir
                    it["cantidad"] -= 1
                    if it["cantidad"] <= 0:
                        inventario.remove(it)
                        cursor_sec = max(0, cursor_sec - 1)
                    mensaje = f"Usaste {it['nombre']}: {', '.join(partes) or 'sin efecto'}"
                    modo = "menu"
            elif tecla in ('q', '\x1b'):
                modo = "menu"

        # ── Menú principal ────────────────────────────────────────────────────
        else:
            if tecla == 'w':
                cursor = (cursor - 1) % 4
            elif tecla == 's':
                cursor = (cursor + 1) % 4

            elif tecla in ('\r', '1', '2', '3', '4'):
                accion = cursor if tecla == '\r' else int(tecla) - 1

                # ── Acción 0: Luchar ──────────────────────────────────────────
                if accion == 0:
                    tipo_txt = _tipo_habilidad_texto("Ataque")
                    dano_j = _daño_jugador(inventario, escudo_roto)

                    # ¿Mob esquiva?
                    if _intentar_esquivar(stats_mob.get("agilidad", 0)):
                        mensaje = f"[cyan]{stats_mob['nombre']} esquivó tu ataque ({tipo_txt})![/]"
                    else:
                        hp_enemigo -= dano_j
                        mensaje = f"{tipo_txt}: hiciste {dano_j} daño."

                    # Turno del mob
                    msgs_mob, escudo_roto = _turno_mob(
                        stats_mob, inventario, escudo_roto,
                        obtener_tecla_fn, simbolo_enemigo, hp_enemigo, hp_max_enemigo)
                    mensaje += " | " + " ".join(msgs_mob)

                # ── Acción 1: Habilidades ─────────────────────────────────────
                elif accion == 1:
                    modo       = "habilidades"
                    cursor_sec = 0

                # ── Acción 2: Ítems ───────────────────────────────────────────
                elif accion == 2:
                    modo       = "items"
                    cursor_sec = 0

                # ── Acción 3: Escapar ─────────────────────────────────────────
                elif accion == 3:
                    p = estado.get("personaje")
                    base, bonus, _ = _calcular_stats_con_items(p, inventario) if p else ({}, {}, [])
                    agi = base.get("agilidad", 20) + bonus.get("agilidad", 0)
                    prob_escape = min(90, agi + 10)
                    if random.randint(1, 100) <= prob_escape:
                        mensaje = "¡Escapaste!"
                        renderizar_batalla(simbolo_enemigo, stats_mob, hp_enemigo,
                                           cursor, mensaje, inventario, "menu", 0, escudo_roto)
                        obtener_tecla_fn()
                        return False
                    else:
                        mensaje = "No pudiste escapar..."
                        msgs_mob, escudo_roto = _turno_mob(
                            stats_mob, inventario, escudo_roto,
                            obtener_tecla_fn, simbolo_enemigo, hp_enemigo, hp_max_enemigo)
                        mensaje += " | " + " ".join(msgs_mob)

        # ── Verificar victoria / derrota ──────────────────────────────────────
        if hp_enemigo <= 0:
            renderizar_batalla(simbolo_enemigo, stats_mob, 0,
                               cursor, f"[bold green]¡Derrotaste al {nombre_enemigo}![/]",
                               inventario, "menu", 0, escudo_roto)
            obtener_tecla_fn()
            return True

        if estado["hp"] <= 0:
            renderizar_batalla(simbolo_enemigo, stats_mob, max(0, hp_enemigo),
                               cursor, "[bold red]¡Fuiste derrotado![/]",
                               inventario, "menu", 0, escudo_roto)
            obtener_tecla_fn()
            return False
