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
        }}