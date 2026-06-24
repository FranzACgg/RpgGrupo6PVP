# pantalla_batalla.py — Sistema de combate por turnos (RPG)
# ARQUITECTURA: recibe contexto como parámetro, no usa estado global.

import os
import random

from rich.console import Console
from rich.panel   import Panel
from rich.columns import Columns
from rich.align   import Align

from config import CAMARA_ALTO
from entidades import STATS_ENEMIGOS, eliminar_enemigo

console = Console()

# ─── ASCII art ───────────────────────────────────────────────────────────────

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
      [ G ]
     /|   |\
    o L   L o
"""

ASCII_DEFAULT = r"""
      ?????
     (     )
      \   /
       ---
"""

ASCII_JEFE = r"""
  /\___/\
 (  >.<  )
  ) J J (
 (________)
  |  |  |
"""
_ARTE = {"slime": ASCII_SLIME, "goblin": ASCII_GOBLIN, "jefe": ASCII_JEFE}

# ─── Catálogo de items (bonus_stats y efecto) ─────────────────────────────────
CATALOGO_ITEMS = {
    1:  {"tipo": "consumible", "efecto": {"hp": 50}},
    2:  {"tipo": "consumible", "efecto": {"hp": 30}},
    3:  {"tipo": "consumible", "efecto": {"hp": 100}},
    4:  {"tipo": "equipable",  "bonus_stats": {"hp": 30}},
    5:  {"tipo": "equipable",  "bonus_stats": {"fuerza": 25}},
    6:  {"tipo": "equipable",  "bonus_stats": {"fuerza": 15, "agilidad": 10}},
    7:  {"tipo": "equipable",  "bonus_stats": {"defensa": 30}},
    8:  {"tipo": "equipable",  "bonus_stats": {"defensa": 15, "hp": 20}},
    9:  {"tipo": "equipable",  "bonus_stats": {"defensa": 40, "hp": 50}},
    10: {"tipo": "consumible", "efecto": {"mp": -30, "hp": -20}},
    11: {"tipo": "consumible", "efecto": {"fuerza": 30}},
    12: {"tipo": "consumible", "efecto": {"defensa": -50}},
    13: {"tipo": "equipable",  "bonus_stats": {"defensa": -10}},
    14: {"tipo": "equipable",  "bonus_stats": {"fuerza": 35, "hp": -30}},
    15: {"tipo": "equipable",  "bonus_stats": {"fuerza": 50, "defensa": -20}},
    16: {"tipo": "equipable",  "bonus_stats": {"agilidad": -15}},
    17: {"tipo": "equipable",  "bonus_stats": {"fuerza": -20}},
    18: {"tipo": "equipable",  "bonus_stats": {"defensa": 20, "suerte": 15}},
}

# ─── Helpers ─────────────────────────────────────────────────────────────────

def _barra(actual, maximo, largo=12):
    llenos = round((actual / maximo) * largo) if maximo > 0 else 0
    return "█" * llenos + "░" * (largo - llenos)


def _tipo_texto(tipo):
    return {"Ataque": "⚔  Ataque", "Maldición": "💀 Maldición",
            "Maldicion": "💀 Maldición", "Defensa": "🛡  Defensa",
            "Mejora": "✨ Mejora", "fisico": "⚔  Físico",
            "magico": "✨ Mágico"}.get(tipo, tipo)


def _stats_con_items(personaje, inventario, escudo_roto=False):
    """
    Devuelve (stats_totales, bonus_dict).
    stats_totales = stats_base + bonus de items equipados (escudo ignorado si roto).
    """
    from personajes import CLASES_DISPONIBLES
    base  = CLASES_DISPONIBLES.get(personaje["clase"], {}).get("stats_base", {}).copy()
    for s in ("fuerza", "defensa", "agilidad", "suerte", "magia", "espiritu"):
        base.setdefault(s, 0)

    bonus = {s: 0 for s in base}
    for it in inventario:
        if not it.get("equipado"):
            continue
        info  = CATALOGO_ITEMS.get(it["id_item"], {})
        bstat = info.get("bonus_stats", {})
        for stat, val in bstat.items():
            if stat == "defensa" and escudo_roto:
                continue
            bonus[stat] = bonus.get(stat, 0) + val

    totales = {k: max(0, base[k] + bonus[k]) for k in base}
    return totales, bonus


def _esquivar(agilidad):
    return random.randint(1, 100) <= max(5, min(50, agilidad))

# ─── Paneles ─────────────────────────────────────────────────────────────────

def _panel_enemigo(tipo_mob, hp_actual):
    datos  = STATS_ENEMIGOS[tipo_mob]
    hp_max = datos["hp_max"]
    arte   = _ARTE.get(tipo_mob, ASCII_DEFAULT)
    barra  = _barra(hp_actual, hp_max)
    stats  = f"FUE:{datos['fuerza']}  DEF:{datos['defensa']}  AGI:{datos['agilidad']}%"
    contenido = (
        f"[bold green]{arte}[/]\n"
        f"[bold white]{datos['nombre']}[/]\n"
        f"[red]HP  {barra}  {hp_actual}/{hp_max}[/]\n"
        f"[dim]{stats}[/]"
    )
    return Panel(contenido, title=f"[bold green]ENEMIGO — {datos['nombre']}[/]",
                 border_style="green", expand=True, padding=(1, 4))


def _panel_personaje(personaje, inventario, escudo_roto=False):
    hp     = personaje["stats_actuales"]["hp"]
    hp_max = personaje["stats_base"]["hp"]
    mp     = personaje["stats_actuales"]["mp"]
    mp_max = personaje["stats_base"]["mp"]
    totales, bonus = _stats_con_items(personaje, inventario, escudo_roto)

    def sl(etiqueta, key):
        b  = totales.get(key, 0)
        bx = bonus.get(key, 0)
        if bx > 0:   sfx = f" [bold green](+{bx})[/]"
        elif bx < 0: sfx = f" [bold red]({bx})[/]"
        else:        sfx = ""
        return f"[dim]{etiqueta:<10}[/] [white]{b}[/]{sfx}"

    vidas = "♥ " * personaje["vidas"] + "♡ " * (3 - personaje["vidas"])
    lineas = [
        f"[bold white]{personaje['nombre']}[/]  [dim]{personaje['clase']}[/]  {vidas}",
        "",
        f"[red]HP  {_barra(hp,hp_max,10)}  {hp}/{hp_max}[/]",
        f"[blue]MP  {_barra(mp,mp_max,10)}  {mp}/{mp_max}[/]",
        "",
        sl("Fuerza",   "fuerza")  + "   " + sl("Defensa",  "defensa"),
        sl("Agilidad", "agilidad") + "   " + sl("Suerte",   "suerte"),
        sl("Magia",    "magia")   + "   " + sl("Espíritu", "espiritu"),
    ]
    if escudo_roto:
        lineas.append("\n[bold red]⚠ Escudo roto![/]")

    return Panel("\n".join(lineas), title="[bold green]PERSONAJE[/]",
                 border_style="green", expand=True, padding=(1, 2))


def _panel_acciones(cursor):
    ops = [("1","Luchar"), ("2","Habilidades"), ("3","Ítems"), ("4","Escapar")]
    lineas = []
    for i, (t, txt) in enumerate(ops):
        lineas.append(f"[bold green]▶ [{t}] {txt}[/]" if i == cursor
                      else f"[dim]  [{t}] {txt}[/]")
    return Panel("\n".join(lineas), title="[bold green]ACCIONES[/]",
                 border_style="green", expand=True, padding=(1, 2))


def _panel_habilidades(personaje, cursor_sec):
    lineas = []
    for i, h in enumerate(personaje.get("habilidades", [])):
        mp_ok = personaje["stats_actuales"]["mp"] >= h["costo_mp"]
        color = "white" if mp_ok else "red"
        marca = "▶ " if i == cursor_sec else "  "
        lineas.append(
            f"[{color}]{marca}[bold]{h['nombre']}[/bold]\n"
            f"      {_tipo_texto(h['tipo'])}  | MP:{h['costo_mp']}  | {h['probabilidad']}% éxito[/]"
        )
    return Panel("\n".join(lineas), title="[bold green]HABILIDADES[/]",
                 border_style="cyan", expand=True, padding=(1, 2))


def _panel_items(inventario, cursor_sec):
    consumibles = [it for it in inventario if it["tipo"] == "consumible"]
    if not consumibles:
        return Panel("[dim]Sin consumibles[/]", title="ÍTEMS",
                     border_style="yellow", expand=True, padding=(1, 2))
    lineas = []
    for i, it in enumerate(consumibles):
        marca = "▶ " if i == cursor_sec else "  "
        info  = CATALOGO_ITEMS.get(it["id_item"], {})
        efecto_str = ", ".join(
            f"{k}{'+'if v>0 else ''}{v}" for k, v in info.get("efecto", {}).items()
        )
        lineas.append(f"[white]{marca}{it['nombre']} x{it['cantidad']}[/] [dim]{efecto_str}[/]")
    return Panel("\n".join(lineas), title="[bold green]ÍTEMS[/]",
                 border_style="yellow", expand=True, padding=(1, 2))


def _panel_log(mensaje):
    return Panel(f"[bold yellow]{mensaje}[/]" if mensaje else "[dim]...[/]",
                 border_style="green", expand=True, padding=(0, 2))

# ─── Render principal ────────────────────────────────────────────────────────

def _renderizar(tipo_mob, hp_enemigo, contexto, cursor, mensaje,
                modo, cursor_sec, escudo_roto):
    os.system('cls' if os.name == 'nt' else 'clear')
    personaje  = contexto["personaje"]
    inventario = contexto["inventario"]
    console.print(Align(_panel_enemigo(tipo_mob, hp_enemigo), align="center"))
    if modo == "habilidades":
        panel_der = _panel_habilidades(personaje, cursor_sec)
    elif modo == "items":
        panel_der = _panel_items(inventario, cursor_sec)
    else:
        panel_der = _panel_acciones(cursor)
    console.print(Columns([
        _panel_personaje(personaje, inventario, escudo_roto),
        panel_der,
    ], expand=True))
    console.print(Align(_panel_log(mensaje), align="center"))

# ─── Turno del mob ────────────────────────────────────────────────────────────

def _turno_mob(tipo_mob, inventario, escudo_roto, personaje):
    """
    Ejecuta el ataque del mob. Devuelve (mensaje, nuevo_escudo_roto).
    Lee hp del personaje desde stats_actuales y lo actualiza ahí.
    """
    datos   = STATS_ENEMIGOS[tipo_mob]
    totales, bonus = _stats_con_items(personaje, inventario, escudo_roto)
    defensa = totales.get("defensa", 0)
    agi_p   = totales.get("agilidad", 0)
    msgs    = []

    # ¿habilidad especial?
    hab_usada = None
    for hab in datos["habilidades"]:
        if random.randint(1, 100) <= hab["probabilidad"]:
            hab_usada = hab
            break

    golpes = 1
    if hab_usada:
        msgs.append(f"[magenta]{datos['nombre']} usa {hab_usada['nombre']} ({_tipo_texto(hab_usada['tipo'])})![/]")

        if hab_usada["nombre"] == "Disparo Ácido":
            dano = max(1, int(datos["fuerza"] * 2) - defensa)
            if _esquivar(agi_p):
                msgs.append("[cyan]¡Esquivaste el Disparo Ácido![/]")
            else:
                personaje["stats_actuales"]["hp"] = max(0, personaje["stats_actuales"]["hp"] - dano)
                msgs.append(f"[red]Recibiste {dano} de daño ácido![/]")
            return " | ".join(msgs), escudo_roto

        elif hab_usada["nombre"] == "Cuerpo Ácido":
            eq = [it for it in inventario if it.get("equipado") and it["tipo"] == "equipable"]
            if eq:
                destruida = random.choice(eq)
                destruida["equipado"] = False
                msgs.append(f"[bold red]¡{destruida['nombre']} fue destruida por el ácido![/]")
            else:
                msgs.append("[dim]Sin arma equipada, el ácido no hace nada.[/]")
            return " | ".join(msgs), escudo_roto

        elif hab_usada["nombre"] == "Daga Rompe Escudos":
            msgs.append("[bold red]¡Tu escudo fue anulado![/]")
            return " | ".join(msgs), True   # escudo_roto = True

        elif hab_usada["nombre"] == "Modo Berserker":
            tirada = random.randint(1, 100)
            golpes = 3 if tirada <= 20 else 2
            msgs.append(f"[bold red]¡Modo Berserker! Ataca {golpes} veces![/]")

        elif hab_usada["nombre"] == "Golpe Devastador":
            dano = max(1, int(datos["fuerza"] * 2) - defensa)
            if _esquivar(agi_p):
                msgs.append("[cyan]¡Esquivaste el Golpe Devastador![/]")
            else:
                personaje["stats_actuales"]["hp"] = max(0, personaje["stats_actuales"]["hp"] - dano)
                msgs.append(f"[red]¡Golpe Devastador! Recibiste {dano} de daño![/]")
            return " | ".join(msgs), escudo_roto

        elif hab_usada["nombre"] == "Torbellino":
            golpes = 3
            msgs.append("[bold red]¡Torbellino! El Campeón ataca 3 veces![/]")

        elif hab_usada["nombre"] == "Grito de Arena":
            msgs.append("[bold red]¡Grito de Arena! Tu escudo fue destrozado![/]")
            return " | ".join(msgs), True

    for _ in range(golpes):
        dano = max(1, datos["fuerza"] - defensa)
        if _esquivar(agi_p):
            msgs.append("[cyan]¡Esquivaste el ataque![/]")
        else:
            personaje["stats_actuales"]["hp"] = max(0, personaje["stats_actuales"]["hp"] - dano)
            msgs.append(f"[red]Recibiste {dano} de daño.[/]")

    return " | ".join(msgs), escudo_roto

# ─── Loop principal ──────────────────────────────────────────────────────────

def iniciar_batalla(enemigo_dict, mapa, contexto, obtener_tecla_fn):
    """
    Parámetros:
        enemigo_dict  : entrada de contexto["mundo"]["enemigos"]
        mapa          : mapa actual (para eliminar el sprite al morir)
        contexto      : contexto completo del juego
        obtener_tecla_fn : función de lectura de teclado

    Devuelve True si el jugador ganó, False si escapó o murió.
    """
    personaje   = contexto["personaje"]
    inventario  = contexto["inventario"]
    tipo_mob    = enemigo_dict["tipo"]
    datos       = STATS_ENEMIGOS[tipo_mob]
    hp_enemigo  = enemigo_dict["hp_actual"]   # FIX: usa hp_actual del dict, que es hp_max al inicio
    hp_max_en   = datos["hp_max"]
    cursor      = 0
    mensaje     = f"¡Un {datos['nombre']} aparece!"
    escudo_roto = False
    modo        = "menu"
    cursor_sec  = 0

    while True:
        _renderizar(tipo_mob, hp_enemigo, contexto, cursor,
                    mensaje, modo, cursor_sec, escudo_roto)
        mensaje = ""
        t = obtener_tecla_fn()

        # ── Menú habilidades ──────────────────────────────────────────────────
        if modo == "habilidades":
            habs = personaje.get("habilidades", [])
            if t == 'w':
                cursor_sec = (cursor_sec - 1) % max(1, len(habs))
            elif t == 's':
                cursor_sec = (cursor_sec + 1) % max(1, len(habs))
            elif t in ('\r', '\n', 'e', ' '):
                if habs:
                    hab = habs[cursor_sec]
                    if personaje["stats_actuales"]["mp"] < hab["costo_mp"]:
                        mensaje = f"[red]Sin MP para {hab['nombre']}.[/]"
                    else:
                        personaje["stats_actuales"]["mp"] -= hab["costo_mp"]
                        totales, _ = _stats_con_items(personaje, inventario, escudo_roto)
                        exito = random.randint(1, 100) <= hab["probabilidad"]
                        if exito:
                            dano = max(1, totales.get("fuerza", 10) + hab.get("valor", 0))
                            if _esquivar(datos["agilidad"]):
                                mensaje = f"[cyan]{datos['nombre']} esquivó {hab['nombre']}![/]"
                            else:
                                hp_enemigo -= int(dano)
                                mensaje = f"[bold]{hab['nombre']}[/] ({_tipo_texto(hab['tipo'])}) → {int(dano)} daño."
                        else:
                            mensaje = f"{hab['nombre']} falló."
                        msg_mob, escudo_roto = _turno_mob(tipo_mob, inventario, escudo_roto, personaje)
                        mensaje += " | " + msg_mob
                        modo = "menu"
            elif t in ('q', '\x1b'):
                modo = "menu"

        # ── Menú ítems ────────────────────────────────────────────────────────
        elif modo == "items":
            consumibles = [it for it in inventario if it["tipo"] == "consumible"]
            if t == 'w':
                cursor_sec = (cursor_sec - 1) % max(1, len(consumibles))
            elif t == 's':
                cursor_sec = (cursor_sec + 1) % max(1, len(consumibles))
            elif t in ('\r', '\n', 'e', ' '):
                if consumibles:
                    it   = consumibles[cursor_sec]
                    info = CATALOGO_ITEMS.get(it["id_item"], {})
                    partes = []
                    for stat, val in info.get("efecto", {}).items():
                        if stat == "hp":
                            personaje["stats_actuales"]["hp"] = min(
                                personaje["stats_base"]["hp"],
                                personaje["stats_actuales"]["hp"] + val
                            )
                            partes.append(f"HP {'+'if val>0 else ''}{val}")
                        elif stat == "mp":
                            personaje["stats_actuales"]["mp"] = min(
                                personaje["stats_base"]["mp"],
                                personaje["stats_actuales"]["mp"] + val
                            )
                            partes.append(f"MP {'+'if val>0 else ''}{val}")
                    it["cantidad"] -= 1
                    if it["cantidad"] <= 0:
                        inventario.remove(it)
                        cursor_sec = max(0, cursor_sec - 1)
                    mensaje = f"Usaste {it['nombre']}: {', '.join(partes) or 'sin efecto'}."
                    modo = "menu"
            elif t in ('q', '\x1b'):
                modo = "menu"

        # ── Menú principal ────────────────────────────────────────────────────
        else:
            if t == 'w':
                cursor = (cursor - 1) % 4
            elif t == 's':
                cursor = (cursor + 1) % 4

            elif t in ('\r', '\n', '1', '2', '3', '4'):
                accion = cursor if t in ('\r', '\n') else int(t) - 1

                if accion == 0:   # LUCHAR
                    totales, _ = _stats_con_items(personaje, inventario, escudo_roto)
                    dano_j = max(1, totales.get("fuerza", 10))
                    tipo_hab = "⚔  Ataque físico"
                    if _esquivar(datos["agilidad"]):
                        mensaje = f"[cyan]{datos['nombre']} esquivó tu ataque ({tipo_hab})![/]"
                    else:
                        hp_enemigo -= dano_j
                        mensaje = f"{tipo_hab}: hiciste {dano_j} daño."
                    msg_mob, escudo_roto = _turno_mob(tipo_mob, inventario, escudo_roto, personaje)
                    mensaje += " | " + msg_mob

                elif accion == 1:   # HABILIDADES
                    modo = "habilidades"
                    cursor_sec = 0

                elif accion == 2:   # ÍTEMS
                    modo = "items"
                    cursor_sec = 0

                elif accion == 3:   # ESCAPAR
                    totales, _ = _stats_con_items(personaje, inventario, escudo_roto)
                    prob = min(90, totales.get("agilidad", 20) + 10)
                    if random.randint(1, 100) <= prob:
                        _renderizar(tipo_mob, hp_enemigo, contexto, cursor,
                                    "¡Escapaste!", "menu", 0, escudo_roto)
                        obtener_tecla_fn()
                        return False
                    else:
                        mensaje = "No pudiste escapar..."
                        msg_mob, escudo_roto = _turno_mob(tipo_mob, inventario, escudo_roto, personaje)
                        mensaje += " | " + msg_mob

        # ── Verificar victoria / derrota ──────────────────────────────────────
        hp_enemigo = max(0, hp_enemigo)

        if hp_enemigo <= 0:
            _renderizar(tipo_mob, 0, contexto, cursor,
                        f"[bold green]¡Derrotaste al {datos['nombre']}! Presioná una tecla.[/]",
                        "menu", 0, escudo_roto)
            obtener_tecla_fn()
            # FIX: eliminar del mapa Y de la lista
            eliminar_enemigo(enemigo_dict, mapa, contexto)
            return True

        if personaje["stats_actuales"]["hp"] <= 0:
            from personajes import revivir
            _renderizar(tipo_mob, hp_enemigo, contexto, cursor,
                        "[bold red]¡Fuiste derrotado! Presioná una tecla.[/]",
                        "menu", 0, escudo_roto)
            obtener_tecla_fn()
            revivir(personaje)
            return False
