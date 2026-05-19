# config.py — Constantes, símbolos, estilos y estado compartido

# ─── Tamaño del mapa y cámara ─────────────────────────────────────────────────
MAPA_REAL_ALTO  = 90
MAPA_REAL_ANCHO = 130
CAMARA_ALTO     = 20
CAMARA_ANCHO    = 40

# ─── Símbolos ─────────────────────────────────────────────────────────────────
simbolos_pasto   = [",", ";", "'", "´"]

# 0: Vacío  1: Entrada cueva  2: Pared cueva  3: Pared tréboles  4: Piso cueva
simbolos_entorno = [" ", "O", "#", "♣", "."]

simbolos_especiales = ["P", "*"]   # 0: Jugador  1: Ítem

simbolos_entornos_no_remplazables = [
    "✿",  # 0  Flor decorativa 1
    "❀",  # 1  Flor decorativa 2
    "⚜",  # 2  Flor decorativa 3
    "=",  # 3  Tronco
    "🪨", # 4  Roca
    "░",  # 5  Camino
    "≈",  # 6  Ola de agua 1
    "~",  # 7  Ola de agua 2
    # Mercado
    "┌", "┐", "└", "┘", "─", "│", "▒", "N", "[", "]",
    # Cementerio
    "🚧", "🪦", "🗿", "🌲", "🏮", "📜",
    # Mob
    "ζ",
]

simbolo_slime = "ζ"

# ─── Estilos Rich ─────────────────────────────────────────────────────────────
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
    "🚧": "bold yellow",
    "🪦": "bold white",
    "🗿": "bold grey50",
    "🌲": "bold bright_green",
    "🏮": "bold yellow on magenta",
    "📜": "bold yellow on dark_magenta",
    "ζ":  "bold cyan",
}

# ─── Teclas ───────────────────────────────────────────────────────────────────
TECLAS_MOVIMIENTO = ['w', 'a', 's', 'd']
# e: interactuar  i: inventario  q: salir  o: opciones  v: volver
TECLAS_ACCION     = ['e', 'i', 'q', 'o', 'v']

# ─── Items del mapa (formato compatible con inventario.py) ────────────────────
items_mapa = {
    "Pociones buenas": [
        {'id_item': 1, 'nombre': 'Pocion de Fuerza Grande', 'tipo': 'consumible', 'cantidad': 1, 'equipado': False},
        {'id_item': 2, 'nombre': 'Pocion de HP pequeña',    'tipo': 'consumible', 'cantidad': 1, 'equipado': False},
        {'id_item': 3, 'nombre': 'Pocion de HP Grande',     'tipo': 'consumible', 'cantidad': 1, 'equipado': False},
    ],
    "Accesorios buenas": [
        {'id_item': 4, 'nombre': 'Gema de vida',    'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 5, 'nombre': 'Hacha de Mitril', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 6, 'nombre': 'Latigo con Puas', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
    ],
    "Equipamiento buenas": [
        {'id_item': 7,  'nombre': 'Escudo de Obsidiana',          'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 8,  'nombre': 'Caso de Tungsteno',            'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 9,  'nombre': 'Pechera de escamas de Dragon', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
    ],
    "Pociones malas": [
        {'id_item': 10, 'nombre': 'Pocion Alucinogena',            'tipo': 'consumible', 'cantidad': 1, 'equipado': False},
        {'id_item': 11, 'nombre': 'Pocion de Potencia/Impotencia', 'tipo': 'consumible', 'cantidad': 1, 'equipado': False},
        {'id_item': 12, 'nombre': 'Pocion de I have no enemies',   'tipo': 'consumible', 'cantidad': 1, 'equipado': False},
    ],
    "Accesorios malas": [
        {'id_item': 13, 'nombre': 'Escudo del Heroe ;)',          'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 14, 'nombre': 'Lanza Maldita',                'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 15, 'nombre': 'Espada de Doble Filo Maldita', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
    ],
    "Equipamiento malas": [
        {'id_item': 16, 'nombre': 'Collar Paralizante',   'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 17, 'nombre': 'Guantes Benevolentes', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 18, 'nombre': 'Casco de Dullahan',    'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
    ],
}

# ─── Estado global del juego ──────────────────────────────────────────────────
# hp/mp/hp_max/mp_max se sobreescriben desde main.py con los stats del personaje
estado = {
    "pos_p":          [1, 52],
    "simbolo_debajo": "░",
    "hp":             100,
    "mp":             50,
    "hp_max":         100,
    "mp_max":         50,
    "inventario":     [],   # lista de dicts — formato de inventario.py
    "mapa_actual":    None,
    "numero_mapa":    1,
    "pasos_jugador":  0,
    "personaje":      None, # dict completo devuelto por crear_personaje()
}
