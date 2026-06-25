# pantalla_batalla.py — Sistema de combate por turnos (RPG)
# Soporta: slimes, goblins, jefe estático, y RIVALES (personajes no elegidos)

import os
import random

from rich.console import Console
from rich.panel   import Panel
from rich.columns import Columns
from rich.align   import Align

from config    import CAMARA_ALTO, CATALOGO_ITEMS, aplicar_efecto_consumible
from entidades import STATS_ENEMIGOS, eliminar_enemigo
from estados import VICTORIA, GAME_OVER
from enemigos_dialogos import obtener_dialogo, ENCUENTRO, ATAQUE, DERROTA

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
ASCII_GUERRERO = r"""
    ___/\___
   |  O  O |
   | \___/ |
   |_______|
    |  |  |
   [GUERRERO]
"""
ASCII_PIRATA = r"""
    _  _
   ( \/ )
   /|  |\
  / |  | \
 /__|  |__\
  [PIRATA]
"""
ASCII_BUFON = r"""
   /\_/\
  ( ^.^ )
  /|   |\
 /_|   |_\
  [BUFON]
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
_ARTE = {
    "slime":   ASCII_SLIME,
    "ζ":       ASCII_SLIME,    # símbolo real del slime en el mapa
    "goblin":  ASCII_GOBLIN,
    "G":       ASCII_GOBLIN,   # símbolo real del goblin en el mapa
    "jefe":    ASCII_JEFE,
    "J":       ASCII_JEFE,     # símbolo real del jefe en el mapa
    "Guerrero": ASCII_GUERRERO,
    "Pirata":   ASCII_PIRATA,
    "Bufon":    ASCII_BUFON,
}

# ─── Catálogo de items: ahora vive en config.py (CATALOGO_ITEMS) ────────────
# para que el inventario fuera de combate y la batalla usen la misma data.

# ─── Helpers ─────────────────────────────────────────────────────────────────

def _barra(actual, maximo, largo=12):
    llenos = round((actual / maximo) * largo) if maximo > 0 else 0
    return "█" * llenos + "░" * (largo - llenos)


def _tipo_texto(tipo):
    return {"Ataque": "⚔ Ataque", "Maldición": "💀 Maldición",
            "Maldicion": "💀 Maldición", "Defensa": "🛡 Defensa",
            "Mejora": "✨ Mejora", "fisico": "⚔ Físico",
            "magico": "✨ Mágico"}.get(tipo, tipo)


def _stats_con_items(personaje, inventario, escudo_roto=False):
    from personajes import CLASES_DISPONIBLES
    base = CLASES_DISPONIBLES.get(personaje["clase"], {}).get("stats_base", {}).copy()
    for s in ("fuerza", "defensa", "agilidad", "suerte"):
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


def _danio_recibido(ataque, defensa):
    # la defensa resta, pero siempre pasa al menos el 25% del ataque
    return max(round(ataque * 0.25), ataque - defensa)


def _datos_rival(rival_seleccion):
    """Construye un dict estilo STATS_ENEMIGOS a partir de un personaje rival."""
    from personajes import CLASES_DISPONIBLES, crear_personaje
    clase  = rival_seleccion["clase"]
    datos_clase = CLASES_DISPONIBLES[clase]
    sb     = datos_clase["stats_base"]
    # Los rivales del coliseo tienen mucha más vida que un jugador normal
    # (x3) para que las peleas sean largas, pero su daño se mantiene
    # moderado (mismas fuerza/defensa base — ver fix de _turno_mob).
    return {
        "nombre":    rival_seleccion["nombre"],
        "simbolo":   clase,
        "hp_max":    sb["hp"] * 3,
        "fuerza":    sb["fuerza"],
        "defensa":   sb["defensa"],
        "agilidad":  sb["agilidad"],
        "habilidades": [
            {
                "nombre":       h["nombre"],
                "tipo":         h["tipo"],
                "valor":        h["valor"],
                "probabilidad": h["probabilidad"],
            }
            for h in datos_clase["habilidades"]
        ],
    }

# ─── Paneles ─────────────────────────────────────────────────────────────────

def _panel_enemigo(datos, hp_actual, etiqueta="ENEMIGO"):
    hp_max = datos["hp_max"]
    simbolo = datos["simbolo"]
    # Buscar arte por símbolo; si no existe, intentar por nombre de clase (rivales)
    arte = _ARTE.get(simbolo) or _ARTE.get(datos.get("nombre", ""), ASCII_DEFAULT)
    barra  = _barra(hp_actual, hp_max)
    stats  = f"FUE:{datos['fuerza']}  DEF:{datos['defensa']}  AGI:{datos['agilidad']}%"
    contenido = (
        f"[bold green]{arte}[/]\n"
        f"[bold white]{datos['nombre']}[/]\n"
        f"[red]HP  {barra}  {hp_actual}/{hp_max}[/]\n"
        f"[dim]{stats}[/]"
    )
    return Panel(contenido, title=f"[bold green]{etiqueta} — {datos['nombre']}[/]",
                 border_style="green", expand=True, padding=(1, 4))


def _panel_personaje(personaje, inventario, escudo_roto=False):
    hp      = personaje["stats_actuales"]["hp"]
    hp_max  = personaje["stats_base"]["hp"]
    mp      = personaje["stats_actuales"]["mp"]
    mp_max  = personaje["stats_base"]["mp"]
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
    ]
    if escudo_roto:
        lineas.append("\n[bold red]⚠ Escudo roto![/]")
    return Panel("\n".join(lineas), title="[bold green]PERSONAJE[/]",
                 border_style="green", expand=True, padding=(1, 2))


def _panel_acciones(cursor):
    ops = [("1","Luchar"), ("2","Habilidades"), ("3","Ítems"), ("4","Escapar")]
    lineas = [
        f"[bold green]▶ [{t}] {txt}[/]" if i == cursor else f"[dim]  [{t}] {txt}[/]"
        for i, (t, txt) in enumerate(ops)
    ]
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
        efecto_str = info.get("descripcion", "Sin descripción.")
        lineas.append(f"[white]{marca}{it['nombre']} x{it['cantidad']}[/]\n[dim]      {efecto_str}[/]")
    return Panel("\n".join(lineas), title="[bold green]ÍTEMS[/]",
                 border_style="yellow", expand=True, padding=(1, 2))


def _panel_log(mensaje):
    return Panel(f"[bold yellow]{mensaje}[/]" if mensaje else "[dim]...[/]",
                 border_style="green", expand=True, padding=(0, 2))

# ─── Render ───────────────────────────────────────────────────────────────────

def _renderizar(datos_en, hp_enemigo, contexto, cursor, mensaje,
                modo, cursor_sec, escudo_roto, etiqueta="ENEMIGO"):
    os.system('cls' if os.name == 'nt' else 'clear')
    personaje  = contexto["personaje"]
    inventario = contexto["inventario"]
    console.print(Align(_panel_enemigo(datos_en, hp_enemigo, etiqueta), align="center"))
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

def _turno_mob(datos, inventario, escudo_roto, personaje, tipo=None):
    totales, bonus = _stats_con_items(personaje, inventario, escudo_roto)
    defensa = totales.get("defensa", 0)
    agi_p   = totales.get("agilidad", 0)
    msgs    = []
    if tipo:
        frase = obtener_dialogo(tipo, ATAQUE)
        if frase:
            msgs.append(f"[italic]{datos['nombre']}: {frase}[/]")

    hab_usada = None
    for hab in datos["habilidades"]:
        if random.randint(1, 100) <= hab["probabilidad"]:
            hab_usada = hab
            break

    golpes = 1
    if hab_usada:
        msgs.append(f"[magenta]{datos['nombre']} usa {hab_usada['nombre']} ({_tipo_texto(hab_usada['tipo'])})![/]")

        nombre_hab = hab_usada["nombre"]

        if nombre_hab == "Disparo Ácido":
            dano = _danio_recibido(datos["fuerza"] * 2, defensa)
            if _esquivar(agi_p):
                msgs.append("[cyan]¡Esquivaste el Disparo Ácido![/]")
            else:
                personaje["stats_actuales"]["hp"] = max(0, personaje["stats_actuales"]["hp"] - dano)
                msgs.append(f"[red]Recibiste {dano} de daño ácido![/]")
            return " | ".join(msgs), escudo_roto

        elif nombre_hab == "Cuerpo Ácido":
            eq = [it for it in inventario if it.get("equipado") and it["tipo"] == "equipable"]
            if eq:
                destruida = random.choice(eq)
                destruida["equipado"] = False
                msgs.append(f"[bold red]¡{destruida['nombre']} fue destruida por el ácido![/]")
            else:
                msgs.append("[dim]Sin arma equipada, el ácido no hace nada.[/]")
            return " | ".join(msgs), escudo_roto

        elif nombre_hab == "Daga Rompe Escudos":
            msgs.append("[bold red]¡Tu escudo fue anulado![/]")
            return " | ".join(msgs), True

        elif nombre_hab in ("Modo Berserker", "Torbellino"):
            tirada = random.randint(1, 100)
            golpes = 3 if tirada <= 20 else 2
            msgs.append(f"[bold red]¡{nombre_hab}! Ataca {golpes} veces![/]")

        elif nombre_hab == "Golpe Devastador":
            dano = _danio_recibido(datos["fuerza"] * 2, defensa)
            if _esquivar(agi_p):
                msgs.append("[cyan]¡Esquivaste el Golpe Devastador![/]")
            else:
                personaje["stats_actuales"]["hp"] = max(0, personaje["stats_actuales"]["hp"] - dano)
                msgs.append(f"[red]¡Golpe Devastador! Recibiste {dano} de daño![/]")
            return " | ".join(msgs), escudo_roto

        elif nombre_hab == "Grito de Arena":
            msgs.append("[bold red]¡Grito de Arena! Tu escudo fue destrozado![/]")
            return " | ".join(msgs), True

        # Habilidades de rivales — actúan con valor adicional (sumado a la
        # fuerza base, igual que cuando el jugador usa sus propias habilidades).
        # Antes se multiplicaba (fuerza * valor), lo que generaba daño absurdo.
        else:
            dano_extra = _danio_recibido(datos["fuerza"] + int(hab_usada.get("valor", 0)), defensa)
            if _esquivar(agi_p):
                msgs.append(f"[cyan]¡Esquivaste {nombre_hab}![/]")
            else:
                personaje["stats_actuales"]["hp"] = max(0, personaje["stats_actuales"]["hp"] - dano_extra)
                msgs.append(f"[red]{nombre_hab}: recibiste {dano_extra} de daño![/]")
            return " | ".join(msgs), escudo_roto

    for _ in range(golpes):
        dano = _danio_recibido(datos["fuerza"], defensa)
        if _esquivar(agi_p):
            msgs.append("[cyan]¡Esquivaste el ataque![/]")
        else:
            personaje["stats_actuales"]["hp"] = max(0, personaje["stats_actuales"]["hp"] - dano)
            msgs.append(f"[red]Recibiste {dano} de daño.[/]")

    return " | ".join(msgs), escudo_roto

# ─── Loop de batalla (genérico) ───────────────────────────────────────────────

def _loop_batalla(datos, hp_max, contexto, obtener_tecla_fn, etiqueta="ENEMIGO", tipo=None):
    """
    Loop de combate reutilizable para cualquier tipo de enemigo.
    Devuelve True si el jugador ganó, False si murió/escapó.
    """
    personaje  = contexto["personaje"]
    inventario = contexto["inventario"]
    hp_enemigo = hp_max
    cursor     = 0
    mensaje    = f"¡{datos['nombre']} aparece!"
    if tipo:
        frase = obtener_dialogo(tipo, ENCUENTRO)
        if frase:
            mensaje += f" [italic]{frase}[/]"
    escudo_roto = False
    modo       = "menu"
    cursor_sec = 0

    while True:
        _renderizar(datos, hp_enemigo, contexto, cursor,
                    mensaje, modo, cursor_sec, escudo_roto, etiqueta)
        mensaje = ""
        t = obtener_tecla_fn()

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
                            dano = max(1, totales.get("fuerza", 10) + int(hab.get("valor", 0)))
                            if _esquivar(datos["agilidad"]):
                                mensaje = f"[cyan]{datos['nombre']} esquivó {hab['nombre']}![/]"
                            else:
                                hp_enemigo -= dano
                                mensaje = f"[bold]{hab['nombre']}[/] → {dano} daño."
                        else:
                            mensaje = f"{hab['nombre']} falló."
                        msg_mob, escudo_roto = _turno_mob(datos, inventario, escudo_roto, personaje, tipo)
                        mensaje += " | " + msg_mob
                        modo = "menu"
            elif t in ('q', '\x1b'):
                modo = "menu"

        elif modo == "items":
            consumibles = [it for it in inventario if it["tipo"] == "consumible"]
            if t == 'w':
                cursor_sec = (cursor_sec - 1) % max(1, len(consumibles))
            elif t == 's':
                cursor_sec = (cursor_sec + 1) % max(1, len(consumibles))
            elif t in ('\r', '\n', 'e', ' '):
                if consumibles:
                    it   = consumibles[cursor_sec]

                    resultado = aplicar_efecto_consumible(it, personaje)

                    it["cantidad"] -= 1
                    if it["cantidad"] <= 0:
                        inventario.remove(it)
                        cursor_sec = max(0, cursor_sec - 1)
                    mensaje = f"Usaste {it['nombre']}: {resultado}."
                    modo = "menu"
            elif t in ('q', '\x1b'):
                modo = "menu"

        else:
            if t == 'w':
                cursor = (cursor - 1) % 4
            elif t == 's':
                cursor = (cursor + 1) % 4
            elif t in ('\r', '\n', '1', '2', '3', '4'):
                accion = cursor if t in ('\r', '\n') else int(t) - 1

                if accion == 0:
                    totales, _ = _stats_con_items(personaje, inventario, escudo_roto)
                    dano_j = max(1, totales.get("fuerza", 10))
                    if _esquivar(datos["agilidad"]):
                        mensaje = f"[cyan]{datos['nombre']} esquivó tu ataque![/]"
                    else:
                        hp_enemigo -= dano_j
                        mensaje = f"⚔ Ataque físico: hiciste {dano_j} daño."
                    msg_mob, escudo_roto = _turno_mob(datos, inventario, escudo_roto, personaje, tipo)
                    mensaje += " | " + msg_mob

                elif accion == 1:
                    modo = "habilidades"
                    cursor_sec = 0

                elif accion == 2:
                    modo = "items"
                    cursor_sec = 0

                elif accion == 3:
                    totales, _ = _stats_con_items(personaje, inventario, escudo_roto)
                    prob = min(90, totales.get("agilidad", 20) + 10)
                    if random.randint(1, 100) <= prob:
                        _renderizar(datos, hp_enemigo, contexto, cursor,
                                    "¡Escapaste!", "menu", 0, escudo_roto, etiqueta)
                        obtener_tecla_fn()
                        return False
                    else:
                        mensaje = "No pudiste escapar..."
                        msg_mob, escudo_roto = _turno_mob(datos, inventario, escudo_roto, personaje, tipo)
                        mensaje += " | " + msg_mob

        hp_enemigo = max(0, hp_enemigo)

        if hp_enemigo <= 0:
            msg_fin = f"[bold green]¡Derrotaste a {datos['nombre']}![/]"
            if tipo:
                frase = obtener_dialogo(tipo, DERROTA)
                if frase:
                    msg_fin += f" [italic]{frase}[/]"
            msg_fin += " [bold green]Presioná una tecla.[/]"
            _renderizar(datos, 0, contexto, cursor, msg_fin,
                        "menu", 0, escudo_roto, etiqueta)
            obtener_tecla_fn()
            return True

        if personaje["stats_actuales"]["hp"] <= 0:
            _renderizar(datos, hp_enemigo, contexto, cursor,
                        "[bold red]¡Fuiste derrotado! Presioná una tecla.[/]",
                        "menu", 0, escudo_roto, etiqueta)
            obtener_tecla_fn()
            return False


# ─── Pantalla de Round ────────────────────────────────────────────────────────

def _pantalla_round(numero, nombre_rival, obtener_tecla_fn):
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Align(Panel(
        f"\n[bold yellow]¡ROUND {numero}![/]\n\n"
        f"[bold white]Tu próximo rival: {nombre_rival}[/]\n\n"
        f"[dim]Presioná cualquier tecla para continuar...[/]\n",
        title="[bold red]⚔  COLISEO[/]",
        border_style="red", expand=False, padding=(2, 6)
    ), align="center"))
    obtener_tecla_fn()


# ─── Pantalla de fin de coliseo ───────────────────────────────────────────────

def _pantalla_victoria_coliseo(obtener_tecla_fn):
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Align(Panel(
        "\n[bold yellow]¡¡¡CAMPEÓN DEL COLISEO!!![/]\n\n"
        "[white]Derrotaste a todos los rivales.\n"
        "El coliseo te acclama.[/]\n\n"
        "[dim]Presioná cualquier tecla...[/]\n",
        title="[bold yellow]🏆 VICTORIA[/]",
        border_style="yellow", expand=False, padding=(2, 6)
    ), align="center"))
    obtener_tecla_fn()


# ─── Entrada pública: batalla normal (mobs) ───────────────────────────────────

def iniciar_batalla(enemigo_dict, mapa, contexto, obtener_tecla_fn):
    """Batalla estándar contra un mob del mapa. Devuelve True si ganó."""
    tipo_mob = enemigo_dict["tipo"]
    datos    = STATS_ENEMIGOS[tipo_mob]
    hp_max   = datos["hp_max"]

    gano = _loop_batalla(datos, hp_max, contexto, obtener_tecla_fn, tipo=tipo_mob)

    if gano:
        eliminar_enemigo(enemigo_dict, mapa, contexto)
    else:
        _manejar_derrota(contexto, mapa)

    return gano


# ─── Entrada pública: pelea en coliseo (rivales) ─────────────────────────────

def iniciar_coliseo(mapa, contexto, obtener_tecla_fn):
    """
    Pelea por rounds contra los personajes no elegidos.
    Round 1 → rival[0], Round 2 → rival[1], etc.
    Cada victoria muestra pantalla de round y restaura MP al jugador.
    Devuelve True si completó todos los rounds.
    """
    rivales = contexto["progreso"].get("rivales_coliseo", [])
    if not rivales:
        return True

    personaje = contexto["personaje"]

    for i, rival_sel in enumerate(rivales):
        datos_rival = _datos_rival(rival_sel)
        numero_round = i + 1
        etiqueta = f"RIVAL — ROUND {numero_round}"

        _pantalla_round(numero_round, rival_sel["nombre"], obtener_tecla_fn)

        # Restaurar MP entre rounds (no HP — mantiene presión)
        personaje["stats_actuales"]["mp"] = personaje["stats_base"]["mp"]

        gano = _loop_batalla(datos_rival, datos_rival["hp_max"],
                             contexto, obtener_tecla_fn, etiqueta)

        if not gano:
            _manejar_derrota(contexto, mapa)
            return False

    _pantalla_victoria_coliseo(obtener_tecla_fn)
    contexto["progreso"]["coliseo_completado"] = True
    contexto["estado_actual"] = VICTORIA
    return True


# ─── Derrota y sistema de vidas ──────────────────────────────────────────────

def _manejar_derrota(contexto, mapa):
    """
    Gestiona la muerte del jugador:
    - Si tiene vidas (Amuleto de Resurrección): pierde 1 vida, va al cementerio,
      cierra las puertas (solo queda salida al Coliseo).
    - Si no tiene vidas: game over.
    """
    from personajes import revivir
    personaje = contexto["personaje"]

    if personaje["vidas"] > 0:
        revivir(personaje)
        _ir_al_cementerio_tras_muerte(contexto)
    else:
        contexto["estado_actual"] = GAME_OVER


def _ir_al_cementerio_tras_muerte(contexto):
    """Teletransporta al jugador al cementerio y bloquea las salidas."""
    from mapa_cementerio import generar_mapa_cementerio
    from entidades import inicializar_enemigos

    mundo = contexto["mundo"]
    mapa_cem = generar_mapa_cementerio()

    # Bloquear la salida sur (→ Prado): reemplazar O por '+'
    mapa_cem[86][73] = "+"   # cierra puerta sur

    mundo["mapa_actual"]    = mapa_cem
    mundo["numero_mapa"]    = 3
    mundo["pos_p"]          = [80, 65]
    mundo["simbolo_debajo"] = ";"
    mundo["dim_alto"]       = 90
    mundo["dim_ancho"]      = 130
    mundo["enemigos"]       = []

    # Marcar el contexto para que cambio_de_mapa sepa que las puertas están cerradas
    contexto["progreso"]["cementerio_bloqueado"] = True

    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Align(Panel(
        "\n[bold red]¡HAS CAÍDO EN BATALLA![/]\n\n"
        "[white]El Amuleto de Resurrección te devuelve a la vida...\n"
        "Pero despiertas en el Cementerio.\n\n"
        "[bold yellow]Las puertas al Prado están cerradas.\n"
        "Solo puedes ir al Coliseo.[/][/]\n\n"
        f"[dim]Vidas restantes: {'♥ ' * contexto['personaje']['vidas']}[/]\n\n"
        "[dim]Presioná cualquier tecla...[/]\n",
        title="[bold red]💀 RESURRECIÓN[/]",
        border_style="red", expand=False, padding=(2, 4)
    ), align="center"))
    import msvcrt
    msvcrt.getch()
