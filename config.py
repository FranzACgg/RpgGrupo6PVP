# config.py — Constantes, símbolos, estilos y contexto

# ─── Tamaño del mapa y cámara ─────────────────────────────────────────────────
MAPA_REAL_ALTO = 90
MAPA_REAL_ANCHO = 130
CAMARA_ALTO = 20
CAMARA_ANCHO = 40

# ─── Símbolos ─────────────────────────────────────────────────────────────────
simbolos_pasto = [
    ",",
    ";",
    "'",
    "´",
]  # TODO "normalizar nombres de constantes a MAYÚSCULAS"

# 0: Vacío  1: Entrada cueva  2: Pared cueva  3: Pared tréboles  4: Piso cueva
simbolos_entorno = [
    " ",
    "O",
    "#",
    "♣",
    ".",
]  # TODO "normalizar nombres de constantes a MAYÚSCULAS"

simbolos_especiales = ["P", "*"]  # 0: Jugador  1: Ítem

simbolos_entornos_no_remplazables = [
    "✿",  # 0  Flor decorativa 1
    "❀",  # 1  Flor decorativa 2
    "⚜",  # 2  Flor decorativa 3
    "=",  # 3  Tronco
    "🪨",  # 4  Roca
    "░",  # 5  Camino
    "≈",  # 6  Ola de agua 1
    "~",  # 7  Ola de agua 2
    # Mercado
    "┌",
    "┐",
    "└",
    "┘",
    "─",
    "│",
    "▒",
    "N",
    "[",
    "]",
    # Cementerio
    "🚧",
    "🪦",
    "🗿",
    "🌲",
    "🏮",
    "📜",
    # Mob
    "ζ",
]

simbolo_slime = "ζ"  # TODO "normalizar nombres de constantes a MAYÚSCULAS"

# ─── Estilos Rich ─────────────────────────────────────────────────────────────
ESTILOS = {
    "P": "bold white on dark_red",
    "*": "bold yellow",
    ",": "dim green",
    ";": "green",
    "'": "green4",
    "´": "spring_green3",
    " ": "white",
    "O": "bold yellow",
    "#": "bold grey50",
    ".": "bold grey30",
    "♣": "bold green",
    "✿": "bold magenta",
    "❀": "bold blue",
    "⚜": "bold red",
    "=": "bold yellow",
    "░": "bold grey70",
    "≈": "bold blue",
    "~": "bold bright_green",
    "▒": "bold grey37",
    "N": "bold magenta",
    "─": "bold grey37",
    "│": "bold grey37",
    "┌": "bold grey37",
    "┐": "bold grey37",
    "└": "bold grey37",
    "┘": "bold grey37",
    "[": "bold white",
    "]": "bold white",
    "🚧": "bold yellow",
    "🪦": "bold white",
    "🗿": "bold grey50",
    "🌲": "bold bright_green",
    "🏮": "bold yellow on magenta",
    "📜": "bold yellow on dark_magenta",
    "ζ": "bold cyan",
}

# ─── Teclas ───────────────────────────────────────────────────────────────────
TECLAS_MOVIMIENTO = ["w", "a", "s", "d"]
# e: interactuar  i: inventario  q: salir  o: opciones  v: volver
TECLAS_ACCION = ["e", "i", "q", "o", "v"]


def crear_contexto():
    return {
        "estado_actual": None,
        "personaje": None,  # toda la info del héroe agrupada
        "inventario": [],  # todos los items
        "buffs_activos": [],
        "mundo": {
            "pos_p": [1, 52],
            "simbolo_debajo": "░",
            "mapa_actual": None,
            "numero_mapa": 1,
            "pasos_jugador": 0,
            "enemigos": [],  # todos los enemigos, de cualquier tipo
        },  # mapa, posición, numero_mapa, simbolo_debajo
        "progreso": {
            "enemigos_derrotados": set(),
        },  # enemigos_derrotados, mapas_visitados?
    }
