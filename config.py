# config.py — Constantes, símbolos, estilos y estado compartido

MAPA_REAL_ALTO  = 90
MAPA_REAL_ANCHO = 130
CAMARA_ALTO     = 20
CAMARA_ANCHO    = 40

simbolos_pasto   = [",", ";", "'", "´"]
simbolos_entorno = [" ", "O", "#", "♣", "."]
simbolos_especiales = ["P", "*"]

simbolos_entornos_no_remplazables = [
    "✿", "❀", "⚜", "=", "🪨", "░", "≈", "~",
    "┌", "┐", "└", "┘", "─", "│", "▒", "N", "[", "]",
    "+",        # valla cementerio (FIX: era 🚧)
    "🪦", "🗿", "🌲", "🏮", "📜",
    "ζ",        # slime
    "G",        # goblin (ASCII, cueva)
    "▓",        # camino cueva
    "C",        # cofre cueva
    "💀", "⛏", # decoración cueva
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
    "+":  "bold yellow",       # valla cementerio
    "🪦": "bold white",
    "🗿": "bold grey50",
    "🌲": "bold bright_green",
    "🏮": "bold yellow on magenta",
    "📜": "bold yellow on dark_magenta",
    "ζ":  "bold cyan",
    "G":  "bold green",        # goblin
    "▓":  "bold grey50",       # camino cueva
    "C":  "bold yellow",       # cofre
    "💀": "bold white",
    "⛏": "bold grey70",
}

TECLAS_MOVIMIENTO = ['w', 'a', 's', 'd']
TECLAS_ACCION     = ['e', 'i', 'q', 'o', 'v']

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

estado = {
    "pos_p":          [1, 65],   # spawn mercado: fila 1, columna central
    "simbolo_debajo": "░",
    "hp":             100,
    "mp":             50,
    "hp_max":         100,
    "mp_max":         50,
    "inventario":     [],
    "mapa_actual":    None,
    "numero_mapa":    1,
    "pasos_jugador":  0,
    "personaje":      None,
}
