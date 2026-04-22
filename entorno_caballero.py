import os
import msvcrt
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# --- CONFIGURACIÓN TÉCNICA ---
SALA_ALTO = 15  # 15 filas de alto según tu arte
SALA_ANCHO = 120 # Largo para recorrer
FILA_SUELO = 12 # El personaje camina en la fila donde pusiste la 'p' y la 'O'

pos_p = [FILA_SUELO, 45] # Empieza cerca del trono (donde estaba la p minúscula)
simbolo_debajo = " "

# Arte de 120 columnas exactas
ARTE_FRONTAL = [
    r"|                                                                                                                      |",
    r"|      / \          /|                         |\          / \                                                         |",
    r"|     | o |        | |      ESPADAS REALES     | |        | o |                                                        |",
    r"|      \_/         | |            ()           | |         \_/                                                         |",
    r"|   ARMADURA       | |            ||           | |       CABEZA                                                        |",
    r"|    [888]         |/             ||            \|      MONSTRUO                                                       |",
    r"|    /[ ]\         |              ||             |        (O)                                                          |",
    r"|    _|_|_        /  \          __||__          /  \      /   \                                                        |",
    r"|   |     |      |____|        |      |        |____|    | [ ] |                                                       |",
    r"|   |  N  |       |  |        --|--|--|--       |  |     |  V  |                                                       |",
    r"|   |_____|      --|--         --|--|--|--     --|--      \___/                                             SALIDA     |",
    r"|__________________|___________________________|____________________________________________________________________   |",
    r"|                                                                                                           O          |",
    r"|                [=======================================]                                                             |",
    r"|                [         TRONO DEL REY FRANZ           ]                                                             |",
    r"|________________[_______________________________________]_____________________________________________________________|",
]

def generar_sala():
    # 1. Creamos la matriz vacía con las medidas exactas
    mapa = [[" " for _ in range(SALA_ANCHO)] for _ in range(SALA_ALTO)]
    
    for i, fila_txt in enumerate(ARTE_FRONTAL):
        if i >= SALA_ALTO: break  # Seguridad: no pasarnos de las 15 filas
        
        # 2. Rellenamos la línea con espacios hasta llegar a 120
        # Esto evita el error si una línea quedó más corta
        fila_normalizada = fila_txt.ljust(SALA_ANCHO)
        
        for j in range(SALA_ANCHO):
            mapa[i][j] = fila_normalizada[j]
    
    # 3. Colocamos al jugador en la posición inicial (fila 12)
    # IMPORTANTE: Asegurate que pos_p[0] sea 12
    mapa[pos_p[0]][pos_p[1]] = "P"
    
    return mapa

mapa_actual = generar_sala()

def obtener_tecla():
    return msvcrt.getch().decode('utf-8', errors='ignore').lower()

def mover_lateral(tecla):
    global pos_p, simbolo_debajo
    dc = 0
    if tecla == 'a' and pos_p[1] > 1: dc = -1
    elif tecla == 'd' and pos_p[1] < SALA_ANCHO - 2: dc = 1
    
    if dc != 0:
        # Restaurar el símbolo que estaba antes (espacio o la 'O')
        mapa_actual[pos_p[0]][pos_p[1]] = simbolo_debajo
        
        # Mover
        pos_p[1] += dc
        
        # Guardar lo que hay en la nueva posición
        simbolo_debajo = mapa_actual[pos_p[0]][pos_p[1]]
        
        # Dibujar al jugador
        mapa_actual[pos_p[0]][pos_p[1]] = "P"

def dibujar_habitacion():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Cámara de 40 de ancho que sigue al jugador
    inicio_c = max(0, min(pos_p[1] - 20, SALA_ANCHO - 40))
    fin_c = inicio_c + 40

    render_mapa = ""
    for fila in mapa_actual:
        linea = "".join(fila[inicio_c:fin_c])
        render_mapa += linea + "\n"
        
    pantalla = Panel(render_mapa, title="[bold yellow]PALACIO DE GLASSTION[/]", border_style="gold1", width=42)
    console.print(Align(pantalla, align="center", vertical="middle", height=console.size.height))

console = Console()

# BUCLE DE PRUEBA
def ejecutar_entorno_caballero():
    while True:
        dibujar_habitacion()
        
        # Lógica de transporte: Si pisamos la 'O'
        if simbolo_debajo == "O":
            False

        tecla = obtener_tecla()
        if tecla in ['a', 'd']:
            mover_lateral(tecla)