# config.py — Constantes, símbolos, estilos y fábrica de contexto

MAPA_REAL_ALTO  = 90
MAPA_REAL_ANCHO = 130
CAMARA_ALTO = 20
CAMARA_ANCHO = 40

simbolos_pasto      = [",", ";", "'", "´"]
simbolos_entorno    = [" ", "O", "#", "♣", "."]
simbolos_especiales = ["P", "*"]

simbolos_entornos_no_remplazables = [
    "✿", "❀", "⚜", "=", "🪨", "░", "≈", "~",
    "┌", "┐", "└", "┘", "─", "│", "▒", "N", "[", "]",
    "+",        # valla cementerio
    "🪦", "🗿", "🌲", "🏮", "📜",
    "ζ",        # slime
    "G",        # goblin
    "▓",        # camino cueva
    "C",        # cofre cueva
    "💀", "⛏",
    "J",        # jefe coliseo
    "I",        # columna coliseo
    "@",        # aldeano/NPC
    "C",        # cofre (mercado y cueva)
    "✦",        # tumba excavable
]

simbolo_slime  = "ζ"
simbolo_goblin = "G"

ESTILOS = {
    "P":  "bold white on dark_red",
    "*":  "bold yellow",
    ",":  "dim green",
    ";":  "green",
    "'":  "green4",
    "´":  "spring_green3",
    " ":  "white",
    "O":  "bold yellow",
    "#":  "bold grey50",
    ".":  "bold grey30",
    "♣":  "bold green",
    "✿":  "bold magenta",
    "❀":  "bold blue",
    "⚜":  "bold red",
    "=":  "bold yellow",
    "░":  "bold grey70",
    "≈":  "bold blue",
    "~":  "bold bright_green",
    "▒":  "bold grey37",
    "N":  "bold magenta",
    "─":  "bold grey37",
    "│":  "bold grey37",
    "┌":  "bold grey37",
    "┐":  "bold grey37",
    "└":  "bold grey37",
    "┘":  "bold grey37",
    "[":  "bold white",
    "]":  "bold white",
    "+":  "bold yellow",
    "🪦": "bold white",
    "🗿": "bold grey50",
    "🌲": "bold bright_green",
    "🏮": "bold yellow on magenta",
    "📜": "bold yellow on dark_magenta",
    "ζ":  "bold cyan",
    "G":  "bold green",
    "▓":  "bold grey50",
    "C":  "bold yellow",
    "💀": "bold white",
    "⛏": "bold grey70",
    "J":  "bold red on dark_red",   # jefe coliseo
    "I":  "bold grey50",             # columna coliseo
    "@":  "bold yellow on dark_blue",  # aldeano
    "✦":  "bold cyan",                 # tumba excavable
}

TECLAS_MOVIMIENTO = ['w', 'a', 's', 'd']
TECLAS_ACCION     = ['e', 'i', 'q', 'o', 'v']

# ─── Catálogo de items: efectos/bonus + descripción corta ──────────────────
# Centralizado acá para que tanto el inventario (fuera de combate) como la
# pantalla de batalla (en combate) usen exactamente la misma lógica y texto.
CATALOGO_ITEMS = {
    1:  {"tipo": "consumible", "efecto": {"hp": 50},
         "descripcion": "Cura 50 de HP al instante."},
    2:  {"tipo": "consumible", "efecto": {"hp": 30},
         "descripcion": "Cura 30 de HP al instante."},
    3:  {"tipo": "consumible", "efecto": {"hp": 100},
         "descripcion": "Cura 100 de HP al instante."},
    4:  {"tipo": "equipable",  "bonus_stats": {"hp": 30},
         "descripcion": "Equipable. Otorga +30 de HP máximo."},
    5:  {"tipo": "equipable",  "bonus_stats": {"fuerza": 25},
         "descripcion": "Equipable. Otorga +25 de Fuerza."},
    6:  {"tipo": "equipable",  "bonus_stats": {"fuerza": 15, "agilidad": 10},
         "descripcion": "Equipable. Otorga +15 Fuerza y +10 Agilidad."},
    7:  {"tipo": "equipable",  "bonus_stats": {"defensa": 30},
         "descripcion": "Equipable. Otorga +30 de Defensa."},
    8:  {"tipo": "equipable",  "bonus_stats": {"defensa": 15, "hp": 20},
         "descripcion": "Equipable. Otorga +15 Defensa y +20 HP máximo."},
    9:  {"tipo": "equipable",  "bonus_stats": {"defensa": 40, "hp": 50},
         "descripcion": "Equipable. Otorga +40 Defensa y +50 HP máximo."},
    10: {"tipo": "consumible", "efecto": {"mp": -30, "hp": -20},
         "descripcion": "¡Cuidado! Resta 30 MP y 20 HP."},
    11: {"tipo": "consumible", "efecto": {"fuerza": 30},
         "descripcion": "Otorga +30 de Fuerza."},
    12: {"tipo": "consumible", "efecto": {"defensa": -50},
         "descripcion": "Reduce tu Defensa en 50. Riesgoso."},
    13: {"tipo": "equipable",  "bonus_stats": {"defensa": -10},
         "descripcion": "Equipable. En realidad resta 10 de Defensa."},
    14: {"tipo": "equipable",  "bonus_stats": {"fuerza": 35, "hp": -30},
         "descripcion": "Equipable. +35 Fuerza, pero -30 HP máximo."},
    15: {"tipo": "equipable",  "bonus_stats": {"fuerza": 50, "defensa": -20},
         "descripcion": "Equipable. +50 Fuerza, pero -20 Defensa."},
    16: {"tipo": "equipable",  "bonus_stats": {"agilidad": -15},
         "descripcion": "Equipable. Resta 15 de Agilidad."},
    17: {"tipo": "equipable",  "bonus_stats": {"fuerza": -20},
         "descripcion": "Equipable. Resta 20 de Fuerza."},
    18: {"tipo": "equipable",  "bonus_stats": {"defensa": 20, "suerte": 15},
         "descripcion": "Equipable. +20 Defensa y +15 Suerte."},
    # ── Items del cementerio (cofres y tumbas) ───────────────────────────────
    30: {"tipo": "equipable",  "bonus_stats": {"defensa": 25},
         "descripcion": "Equipable. Otorga +25 de Defensa."},
    31: {"tipo": "equipable",  "bonus_stats": {"fuerza": 20, "suerte": -10},
         "descripcion": "Equipable. +20 Fuerza, pero -10 Suerte."},
    32: {"tipo": "consumible", "efecto": {"hp": 150},
         "descripcion": "Cura 150 de HP al instante."},
    33: {"tipo": "equipable",  "bonus_stats": {"fuerza": 25, "agilidad": 10},
         "descripcion": "Equipable. +25 Fuerza y +10 Agilidad."},
    34: {"tipo": "consumible", "efecto": {"mp": 40, "hp": -15},
         "descripcion": "Maldito: +40 MP, pero -15 HP."},
    35: {"tipo": "equipable",  "bonus_stats": {"suerte": 20, "defensa": -10},
         "descripcion": "Equipable. +20 Suerte, pero -10 Defensa."},
    # ── Items de quest ────────────────────────────────────────────────────────
    50: {"tipo": "clave",
         "descripcion": "Objeto clave. Sirve para excavar tumbas (✦) en el cementerio."},
    51: {"tipo": "consumible", "efecto": {"mp": 10},
         "descripcion": "Comestible. Te sube 10 de MP. También se la podés llevar a Brotus."},
    52: {"tipo": "clave",
         "descripcion": "Objeto clave. Canjeable con Mordecai el Nigromante."},
    60: {"tipo": "consumible", "efecto": {}, "especial": "super_curacion",
         "descripcion": "Llena tu HP por completo y aumenta tu HP máximo en 50."},
    61: {"tipo": "equipable",  "bonus_stats": {"suerte": 50},
         "descripcion": "Equipable. Otorga +50 de Suerte."},
    99: {"tipo": "clave",
         "descripcion": "Te revive automáticamente al caer en combate (vidas extra)."},
}


def aplicar_efecto_consumible(item, personaje):
    """
    Entrada: Diccionario (item del inventario), Diccionario (personaje)
    Objetivo: aplicar el efecto real de un consumible sobre las stats del
    personaje (HP/MP), sea que se use dentro o fuera de combate.
    Salida: string legible con los cambios aplicados (para mostrar en UI).
    """
    info = CATALOGO_ITEMS.get(item["id_item"], {})
    partes = []

    if info.get("especial") == "super_curacion":
        personaje["stats_base"]["hp"] += 50
        personaje["stats_actuales"]["hp"] = personaje["stats_base"]["hp"]
        partes.append(f"HP LLENO + HP Máx +50 ({personaje['stats_base']['hp']})")
        return ", ".join(partes)

    for stat, val in info.get("efecto", {}).items():
        if stat == "hp":
            personaje["stats_actuales"]["hp"] = max(0, min(
                personaje["stats_base"]["hp"],
                personaje["stats_actuales"]["hp"] + val
            ))
            partes.append(f"HP {'+' if val > 0 else ''}{val}")
        elif stat == "mp":
            personaje["stats_actuales"]["mp"] = max(0, min(
                personaje["stats_base"]["mp"],
                personaje["stats_actuales"]["mp"] + val
            ))
            partes.append(f"MP {'+' if val > 0 else ''}{val}")

    return ", ".join(partes) if partes else "sin efecto"


def crear_contexto():
    """Devuelve el dict de estado global del juego. Todo el juego lo pasa por parámetro."""
    return {
        "estado_actual": None,
        "personaje":      None,   # dict completo de personajes.py
        "inventario":     [],     # lista de dicts del sistema de inventario.py
        "buffs_activos":  [],
        "mundo": {
            "pos_p":          [1, 52],
            "simbolo_debajo": "░",
            "mapa_actual":    None,
            "numero_mapa":    1,
            "pasos_jugador":  0,
            "enemigos":       [],   # lista de dicts {tipo, pos, debajo, hp_actual}
            "dim_alto":       MAPA_REAL_ALTO,
            "dim_ancho":      MAPA_REAL_ANCHO,
        },
        "progreso": {
            "enemigos_derrotados": set(),
            "rivales_coliseo":      [],
            "rival_actual":         0,
            "cementerio_bloqueado": False,
            "coliseo_completado":   False,
        }}