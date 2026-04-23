import os
import random
import msvcrt # Librería para detectar teclas sin Enter (solo Windows)
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
#from entorno_caballero import ejecutar_entorno_caballero
from inventario import agregar_item, manejar_inventario

# Fundamentos Principales
# CConfiguracion tamaño del mapa
MAPA_REAL_ALTO = 90
MAPA_REAL_ANCHO = 130

# Definimos el tamaño de lo que se VE en pantalla (la cámara)
CAMARA_ALTO = 20
CAMARA_ANCHO = 40


CATALOGO_ITEMS = [
        {'id_item': 1, 'nombre': 'Pocion de HP pequeña', 'tipo': 'consumible', 'cantidad': 1, 'equipado': False},
        {'id_item': 2, 'nombre': 'Escudo de Obsidiana', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 3, 'nombre': 'Gema de vida', 'tipo': 'clave', 'cantidad': 1, 'equipado': False},
        {'id_item': 4, 'nombre': 'Hacha de Mitril', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 5, 'nombre': 'Pocion de Fuerza Grande', 'tipo': 'consumible', 'cantidad': 1, 'equipado': False},
        {'id_item': 6, 'nombre': 'Pocion Alucinogena', 'tipo': 'consumible', 'cantidad': 1, 'equipado': False},
        {'id_item': 7, 'nombre': 'Collar Paralizante', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 8, 'nombre': 'Lanza Maldita', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 9, 'nombre': 'Espada de Doble Filo', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 10, 'nombre': 'Casco de Dullahan', 'tipo': 'equipable', 'cantidad': 1, 'equipado': False},
        {'id_item': 11, 'nombre': 'Amuleto del Rey', 'tipo': 'clave', 'cantidad': 1, 'equipado': False},
        {'id_item': 12, 'nombre': 'Pocion de Potencia', 'tipo': 'consumible', 'cantidad': 1, 'equipado': False}
]


# Simbolos para el mapa

simbolos_pasto = [",", ";", "'", "´"]

#Simbolos de entorno: 0: Espacio vacío, 1: Entrada de cueva, 2: Pared de cueva, 3: Pared de tréboles, 4: Piso de cueva
simbolos_entorno = [" ", "O", "#", "♣", "."]
simbolos_entornos_no_remplazables = ["✿", "❀","⚜","=","🪨","░","≈","~"] # Elementos decorativos que no se reemplazan por pasto
#Simbolos especiales: 0: Jugador, 1: Ítem
simbolos_especiales = ["P", "*"]

# Informacion del personaje 
pos_p = [1, 52] # Fila, Columna

mp = 50
hp = 100
stats_jugador = [mp, hp]

console = Console()


TECLAS_MOVIMIENTO = ['w', 'a', 's', 'd']
#Teclaas de interacción # E para interactuar, I para inventario, Q salir O para opciones en juego, V para volver al juego desde el menú
TECLAS_ACCION = ['e', 'i', 'q','o','v'] 

ESTILOS = {
    "P": "bold white on dark_red", # Jugador resaltado
    "♣": "bold green",               # Muralla de tréboles
    "*": "bold yellow",              # Ítems brillantes
    ",": "dim green",                # Pasto tipo 1
    ";": "green",                    # Pasto tipo 2
    "'": "green4",                   # Pasto tipo 3 (un verde distinto)
    "´": "spring_green3",            # Pasto tipo 4
    " ": "white",                    # Espacio vacío, lo llenamos con pasto aleatorio
    "O": "bold yellow",              # Entrada de cueva        
    "#": "bold grey50",              # Pared de cueva
    ".": "bold grey30",               # Piso de cueva
    "✿": "bold magenta",              # Flor decorativa
    "❀": "bold blue",          # Flor decorativa 2
    "⚜": "bold red",          # Flor decorativa 3
    "=" : "bold brown",    # Tronco decorativo
    "░" : "bold grey70",    # Camino decorativo
    "≈" : "bold blue20", # Ola de agua decorativa
    "~" : "bold light_green" # Ola de agua decorativa 2
    
}

def elementos_decorativos(mapa):
    for _ in range(30):
        f_rand, c_rand = random.randint(1, MAPA_REAL_ALTO-2), random.randint(1, MAPA_REAL_ANCHO-2)
        mapa[f_rand][c_rand] = simbolos_entornos_no_remplazables[0] # Flor decorativa 
    for _ in range(30):
        f_rand, c_rand = random.randint(1, MAPA_REAL_ALTO-2), random.randint(1, MAPA_REAL_ANCHO-2)
        mapa[f_rand][c_rand] = simbolos_entornos_no_remplazables[1] # Flor decorativa 2
    for _ in range(30):
        f_rand, c_rand = random.randint(1, MAPA_REAL_ALTO-2), random.randint(1, MAPA_REAL_ANCHO-2)
        mapa[f_rand][c_rand] = simbolos_entornos_no_remplazables[2] # Flor decorativa 3
    for _ in range(5):
        f_rand, c_rand = random.randint(1, MAPA_REAL_ALTO-2), random.randint(1, MAPA_REAL_ANCHO-2)
        mapa[f_rand][c_rand] = simbolos_entornos_no_remplazables[3] # Tronco decorativo 
    for _ in range(8):
        f_rand, c_rand = random.randint(1, MAPA_REAL_ALTO-2), random.randint(1, MAPA_REAL_ANCHO-2)
        mapa[f_rand][c_rand] = simbolos_entornos_no_remplazables[4]  

def elementos_interactuables(mapa): # Va en el aarchivo de Elementos 
    for _ in range(7):
        f_rand, c_rand = random.randint(1, MAPA_REAL_ALTO-2), random.randint(1, MAPA_REAL_ANCHO-2)
        mapa[f_rand][c_rand] = simbolos_especiales[1] # Ítem 
        

def generar_cueva(mapa_actual, f_inicio, c_inicio, ancho, alto):
    # 1. Definimos los límites de la cueva
    f_fin = f_inicio + alto
    c_fin = c_inicio + ancho

    for f in range(f_inicio, f_fin + 1):
        for c in range(c_inicio, c_fin + 1):
            # Verificamos que no nos salgamos del mapa real de 50x50
            if 0 <= f < MAPA_REAL_ALTO and 0 <= c < MAPA_REAL_ANCHO:
                
                # A. Dibujamos las paredes externas ()
                if f == f_inicio or f == f_fin or c == c_inicio or c == c_fin:
                    # Dejamos un espacio para la entrada 'O' en la mitad de la pared izquierda
                    if c == c_inicio and f == f_inicio + (alto // 2):
                        mapa_actual[f][c] = simbolos_entorno[1] # Entrada de cueva
                    else:
                        mapa_actual[f][c] = simbolos_entorno[2] # Pared de cueva
                
                # B. Rellenamos el interior (Piso de cueva)
                else:
                    mapa_actual[f][c] = simbolos_entorno[4] # Piso de cueva
                                  
def generar_casaDestruida(mapa_actual, f_inicio, c_inicio, ancho, alto):
    # 1. Definimos los límites de la casa
    f_fin = f_inicio + alto
    c_fin = c_inicio + ancho

    for f in range(f_inicio, f_fin + 1):
        for c in range(c_inicio, c_fin + 1):
            # Verificamos que no nos salgamos del mapa real de 50x50
            if 0 <= f < MAPA_REAL_ALTO and 0 <= c < MAPA_REAL_ANCHO:
                
                # A. Dibujamos las paredes externas ()
                if f == f_inicio or f == f_fin or c == c_inicio or c == c_fin:
                    # Dejamos un espacio para la entrada 'O' en la mitad de la pared izquierda
                    if c == c_inicio and f == f_inicio + (alto // 2):
                        mapa_actual[f][c] = simbolos_entorno[1] # Entrada de cueva
                    else:
                        mapa_actual[f][c] = simbolos_entornos_no_remplazables[3] # Pared de Casa
                
                # B. Rellenamos el interior (Piso de cueva)
                else:
                    mapa_actual[f][c] = simbolos_entorno[4] # Piso de cueva
                    
def generar_lago(mapa_actual, f_inicio, c_inicio, ancho, alto):
    # 1. Definimos los límites de la casa
    f_fin = f_inicio + alto
    c_fin = c_inicio + ancho

    for f in range(f_inicio, f_fin + 1):
        for c in range(c_inicio, c_fin + 1):
            # Verificamos que no nos salgamos del mapa real de 50x50
            if 0 <= f < MAPA_REAL_ALTO and 0 <= c < MAPA_REAL_ANCHO:
                
                # A. Dibujamos las paredes externas ()
                if f == f_inicio or f == f_fin or c == c_inicio or c == c_fin:
                    mapa_actual[f][c] = simbolos_entornos_no_remplazables[random.randint(6, 7)] # Ola de agua decorativa
                else:
                    mapa_actual[f][c] = simbolos_entornos_no_remplazables[random.randint(6, 7)] # Ola de agua decorativa
                   
                
                    
def generar_caminos_principales(mapa_actual):
    # Calculamos el centro
    f_centro = MAPA_REAL_ALTO // 2
    c_centro = MAPA_REAL_ANCHO // 2

    # 1. Camino Horizontal (Cruza todas las columnas en la fila central)
    for c in range(MAPA_REAL_ANCHO):
        # Ponemos un símbolo de 'piso' o 'sendero' (.)
        # Evitamos pisar si hay algo muy importante, pero acá definimos el camino
        mapa_actual[f_centro][c] = simbolos_entornos_no_remplazables[5] # Camino decorativo (░)

    # 2. Camino Vertical (Cruza todas las filas en la columna central)
    for f in range(MAPA_REAL_ALTO):
        mapa_actual[f][c_centro] = simbolos_entornos_no_remplazables[5] # Camino decorativo (░)

    # 3. Colocar las Entradas 'O' en los extremos de los caminos
    # Estos puntos serán tus "Teleports" al interactuar
    puntos_entrada = [
        (f_centro, 0),                        # Extremo Izquierdo
        (f_centro, MAPA_REAL_ANCHO - 1),      # Extremo Derecho
        (0, c_centro),                        # Extremo Superior
        (MAPA_REAL_ALTO - 1, c_centro)        # Extremo Inferior
    ]

    for f, c in puntos_entrada:
        mapa_actual[f][c] = simbolos_entorno[1] # Entrada            


                                        
# 1. CREAR EL MAPA (Matriz)
def generar_mapa_prado():
    # Creamos una matriz llena de espacios vacíos ' '
    mapa = [[simbolos_entorno[0] for _ in range(MAPA_REAL_ANCHO)] for _ in range(MAPA_REAL_ALTO)]
    
    # Ponemos paredes '#' en los bordes
    for f in range(MAPA_REAL_ALTO):
        for c in range(MAPA_REAL_ANCHO):
            if f == 0 or f == MAPA_REAL_ALTO-1 or c == 0 or c == MAPA_REAL_ANCHO-1:
                mapa[f][c] = simbolos_entorno[3] # Pared de tréboles
            if mapa[f][c] == simbolos_entorno[0]: # Espacio vacío, lo llenamos con pasto aleatorio
                mapa[f][c] = simbolos_pasto[random.randint(0, len(simbolos_pasto) - 1)]
                
    # Colocamos 3 ítems '*' en lugares aleatorios (que no sean paredes ni la pos inicial)
    elementos_interactuables(mapa)
    elementos_decorativos(mapa)
    
    
    generar_caminos_principales(mapa)
        
    mapa[1][52] = simbolos_especiales[0] # Colocamos al jugador
    
    generar_cueva(mapa, 10, 10, 6, 4)
    generar_casaDestruida(mapa, 11, 90, 15, 10)
    generar_lago(mapa,60, 20, 15, 20)
    
    return mapa

# Arte ASCII para el puesto tipo bloque con mostrador
# 'N' representa al NPC que está atendiendo



simbolos_entornos_no_remplazables.extend(["┌", "┐", "└", "┘", "─", "│", "▒", "N", "[", "]", "="])
# Añadir a ESTILOS
ESTILOS.update({
    "▒": "bold grey37",    # Paredes del puesto
    "N": "bold magenta",   # El NPC atendiendo
    "=": "bold yellow",    # El mostrador
    "─": "bold grey37",    # Bordes
    "│": "bold grey37",
    "┌": "bold grey37",
    "┐": "bold grey37",
    "└": "bold grey37",
    "┘": "bold grey37",
    "[": "bold white",
    "]": "bold white"
})


ARTE_PUESTO_NPC = [
    "┌─────┐",
    "│▒▒▒▒▒│",
    "│▒ N ▒│",
    "│[===]│", # Mostrador
    "└─────┘"
]

def generar_puesto_con_npc(mapa, f, c):
    # f, c son las coordenadas donde empieza la esquina superior izquierda del puesto
    for i, fila in enumerate(ARTE_PUESTO_NPC):
        for j, caracter in enumerate(fila):
            if 0 <= f + i < MAPA_REAL_ALTO and 0 <= c + j < MAPA_REAL_ANCHO:
                mapa[f + i][c + j] = caracter

def generar_caminos_principales_mercado(mapa):
    for f in range(MAPA_REAL_ALTO):
        for c in range(MAPA_REAL_ANCHO):
            if f == 0 or f == MAPA_REAL_ALTO-1 or c == 0 or c == MAPA_REAL_ANCHO-1:
                mapa[f][c] = "▒"
            #Ubicacioes de Salida
            if f == 30 and c == 129 or f == 0 and c == 52:
                mapa[f][c] = simbolos_entorno[1] # Entrada/Salida del mercado
    
def generar_mapa_mercado_total():
    # 1. Suelo base (espacio vacío)
    mapa = [[simbolos_entorno[0] for _ in range(MAPA_REAL_ANCHO)] for _ in range(MAPA_REAL_ALTO)]
    
    # 2. Bordes de ciudad y Salida del mapa
    generar_caminos_principales_mercado(mapa)
    
    # --- LÓGICA DE CALLES (2H x 4V) ---
    filas_h = [MAPA_REAL_ALTO // 3, (MAPA_REAL_ALTO // 3) * 2]
    cols_v = [MAPA_REAL_ANCHO // 5, (MAPA_REAL_ANCHO // 5) * 2, 
              (MAPA_REAL_ANCHO // 5) * 3, (MAPA_REAL_ANCHO // 5) * 4]

    # --- COLOCACIÓN MASIVA DE PUESTOS ---
    for f_calle in filas_h:
        # Recorremos todo el ancho del mapa (dejando margen para los bordes)
        for c_pos in range(2, MAPA_REAL_ANCHO - 8, 8):
            
            # Verificamos si la posición actual NO coincide con una calle vertical
            # para no tapar los cruces de los caminos
            esta_en_cruce = any(c_pos in range(cv - 2, cv + 2) for cv in cols_v)
            
            if not esta_en_cruce:
                # Fila de arriba: la base del puesto toca la calle
                generar_puesto_con_npc(mapa, f_calle - 5, c_pos)
                
                # Fila de abajo: el techo del puesto empieza justo debajo de la calle
                generar_puesto_con_npc(mapa, f_calle + 1, c_pos)

    # 3. Dibujamos los caminos AL FINAL para que las calles "limpien" cualquier resto
    # Caminos horizontales
    for f in filas_h:
        for c in range(1, MAPA_REAL_ANCHO - 1):
            mapa[f][c] = "░"
            
    # Caminos verticales
    for c in cols_v:
        for f in range(1, MAPA_REAL_ALTO - 1):
            mapa[f][c] = "░"

    return mapa

# 1. Nuevos símbolos de entorno (BLOQUEANTES)
# 8: Valla de madera, 9: Tumba normal, 10: Tumba grande, 
# 11: Árbol tipo pino, 12: Farola, 13: Cartel
simbolos_entornos_no_remplazables.extend(["🚧", "🪦", "🗿", "🌲", "🏮", "📜"]) 

# 2. Definir los colores en ESTILOS
ESTILOS.update({
    # Fondo y Caminos (Piso)
    "▒": "bold grey30",      # Adoquines/Caminos de piedra
    ",": "dim green",        # Pasto base
    ";": "green",            
    "'": "green4",           
    "´": "spring_green3",     
    " ": "dim magenta",       # Espacio vacío (si queda)

    # Entorno Cementerio
    "🚧": "bold yellow",      # Valla de madera (un marrón claro)
    "🪦": "bold white",        # Tumba pequeña/lápida
    "🗿": "bold grey50",       # Tumba grande/Monumento
    "🌲": "bold bright_green", # Árboles (Pinos)
    "🏮": "bold yellow on magenta", # Farolas
    "📜": "bold yellow on dark_magenta", # Cartel/Arco de entrada
})

def generar_mapa_cementerio():
    # A. Inicializar el mapa lleno de pasto base aleatorio (como en tu mapa 1)
    mapa = [[random.choice(simbolos_pasto) for _ in range(MAPA_REAL_ANCHO)] for _ in range(MAPA_REAL_ALTO)]
    
    # B. Dibujar la valla periférica (deja un margen para las farolas afuera)
    for f in range(2, MAPA_REAL_ALTO - 2):
        for c in range(2, MAPA_REAL_ANCHO - 2):
            if f == 2 or f == MAPA_REAL_ALTO - 3 or c == 2 or c == MAPA_REAL_ANCHO - 3:
                mapa[f][c] = "🚧"
            if f == 86 and c == 73:
                mapa[f][c] = simbolos_entorno[1] # Ítem en el cementerio 

    
    # --- LÓGICA DE SENDEROS DE PIEDRA (2H x 3V) ---
    # Trazamos caminos fijos de 2 caracteres de ancho para la cámara 20x40
    filas_h = [MAPA_REAL_ALTO // 3, (MAPA_REAL_ALTO // 3) * 2]
    cols_v = [MAPA_REAL_ANCHO // 4, MAPA_REAL_ANCHO // 2, (MAPA_REAL_ANCHO // 4) * 3]

    # Dibujar caminos
    for f in filas_h:
        for c in range(3, MAPA_REAL_ANCHO - 3):
            mapa[f][c] = "▒"; mapa[f+1][c] = "▒" # Doble ancho
            
    for c in cols_v:
        for f in range(3, MAPA_REAL_ALTO - 3):
            mapa[f][c] = "▒"; mapa[f][c+1] = "▒" # Doble ancho

    # --- COLOCAR TUMBAS Y ÁRBOLES ESCOLTANDO LOS CAMINOS ---
    # Recorremos el mapa y donde haya pasto, si está cerca de un camino, 
    # hay una probabilidad de poner una tumba o un árbol.
    for f in range(4, MAPA_REAL_ALTO - 4):
        for c in range(4, MAPA_REAL_ANCHO - 4):
            # Solo si la celda es pasto
            if mapa[f][c] in simbolos_pasto:
                # Chequeamos si hay camino cerca (░ o ▒)
                hay_camino = False
                for df in range(-2, 3): # Chequeamos un radio mayor
                    for dc in range(-2, 3):
                        if 0 <= f+df < MAPA_REAL_ALTO and 0 <= c+dc < MAPA_REAL_ANCHO:
                            if mapa[f+df][c+dc] == "▒":
                                hay_camino = True
                
                if hay_camino:
                    prob = random.random()
                    if prob < 0.15: # 15% de chance de tumba pequeña
                        mapa[f][c] = "🪦"
                    elif prob < 0.18: # 3% para tumba grande
                        mapa[f][c] = "🗿"
                    elif prob < 0.23: # 5% para árboles (para que no tapen todo)
                        mapa[f][c] = "🌲"

    # D. ARCO DE ENTRADA GRANDE CON CARTEL
    # Lo ponemos en el centro de la valla inferior, en el medio del mapa real
    f_entrada = MAPA_REAL_ALTO - 3
    c_entrada = MAPA_REAL_ANCHO // 2
    # Estructura de 3x5 caracteres
    arte_entrada = [
        " ┌─────┐ ",
        " │📜📜📜│ ",
        " │░░░░░│ "
    ]
    for i, fila in enumerate(arte_entrada):
        for j, char in enumerate(fila):
            mapa[f_entrada - 2 + i][c_entrada - 4 + j] = char

    # E. Farolas exteriores
    for pos_f in [1, MAPA_REAL_ALTO - 1]:
        for pos_c in range(10, MAPA_REAL_ANCHO - 10, 20):
            mapa[pos_f][pos_c] = "🏮"

    return mapa




def dibujar_juego_centrado(hp, mp):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Lógica de Cámara
    inicio_f = max(0, min(pos_p[0] - CAMARA_ALTO // 2, MAPA_REAL_ALTO - CAMARA_ALTO))
    inicio_c = max(0, min(pos_p[1] - CAMARA_ANCHO // 2, MAPA_REAL_ANCHO - CAMARA_ANCHO))

    filas_coloreadas = []
    
    for f in range(inicio_f, inicio_f + CAMARA_ALTO):
        string_fila = ""
        for c in range(inicio_c, inicio_c + CAMARA_ANCHO):
            char = mapa_actual[f][c]
            
            # Buscamos el estilo en nuestro diccionario. 
            # Si no existe, usamos "white" por defecto.
            color = ESTILOS.get(char, "white")
            
            # Formateamos para Rich: [color]caracter[/color]
            string_fila += f"[{color}]{char}[/] " 
            
        filas_coloreadas.append(string_fila)
    
    mapa_renderizado = "\n".join(filas_coloreadas)

    # Creamos el Panel de Rich
    pantalla = Panel(
        mapa_renderizado,
        title=f"[bold yellow]GLASSTION - POS: {pos_p[0]},{pos_p[1]}[/]",
        subtitle=f"[bold red]HP: {hp}/100[/] | [bold blue]MP: {mp}/50[/]",
        border_style="bright_blue",
        expand=False,
        padding=(1, 2)
    )

    # Centrado total (Horizontal y Vertical)
    console.print(Align(pantalla, align="center", vertical="middle", height=console.size.height))


       
# 3. LÓGICA DE MOVIMIENTO
simbolo_debajo = "░" 
def mover(tecla, inventario):
    global pos_p, simbolo_debajo
    
    # ... (tu lógica de df, dc está perfecta) ...
    df, dc = 0, 0
    if tecla == TECLAS_MOVIMIENTO[2]: df = 1
    elif tecla == TECLAS_MOVIMIENTO[0]: df = -1
    elif tecla == TECLAS_MOVIMIENTO[1]: dc = -1
    elif tecla == TECLAS_MOVIMIENTO[3]: dc = 1
    else: return

    nueva_f = pos_p[0] + df
    nueva_c = pos_p[1] + dc

    # Verificamos límites de la matriz (importante para que no tire error de índice)
    if 0 <= nueva_f < MAPA_REAL_ALTO and 0 <= nueva_c < MAPA_REAL_ANCHO:
        
        celda_destino = mapa_actual[nueva_f][nueva_c]

        # Verificamos colisión con paredes (simbolos_entorno[3] y [2])
        if celda_destino != simbolos_entorno[3] and celda_destino != simbolos_entorno[2]:

            if mapa_actual[nueva_f][nueva_c] == simbolos_especiales[1]:
                respuesta = input("¿Deseas recoger el objeto? S/N: ")
                if respuesta.lower() == "s":
                    item_recogido = random.choice(CATALOGO_ITEMS).copy()
                    agregar_item(item_recogido, inventario)
                    celda_destino = random.choice(simbolos_pasto)
                else:
                    return
                    
        #El slime le quita vida al Jugador   
        
        #if celda_destino == simbolo_slime:
            #stats_jugador[1] -= 10
            #print("¡Has sido atacado por un slime! HP -10")
            # --- LÓGICA DE MOVIMIENTO "LIMPIA" ---
        
            # 1. RESTAURAMOS: En la posición donde ESTAMOS ahora, ponemos lo que había antes
            # Si estábamos sobre una 'O', devolvemos la 'O'. Si era pasto, devolvemos pasto.
            mapa_actual[pos_p[0]][pos_p[1]] = simbolo_debajo

            # 2. GUARDAMOS EL FUTURO: Antes de pisar la nueva celda, miramos qué hay
            # Si la celda de destino es reemplazable (pasto), decidimos que al salir 
            # de ahí se convierta en un pasto nuevo. Si no es reemplazable, guardamos la celda original.
            if celda_destino in simbolos_pasto or celda_destino == simbolos_especiales[1]: 
                simbolo_debajo = random.choice(simbolos_pasto)
            elif celda_destino == " ": # Si es suelo de ciudad vacío
                simbolo_debajo = " "
            else:
                simbolo_debajo = celda_destino

            # 3. TRASLACIÓN: Actualizamos las coordenadas
            pos_p[0], pos_p[1] = nueva_f, nueva_c

            # 4. RENDER: Dibujamos al jugador 'P' en la nueva posición
            mapa_actual[pos_p[0]][pos_p[1]] = simbolos_especiales[0]

def elementos_reemplazables(nueva_f, nueva_c):
    global pos_p # IMPORTANTE: Para que el cambio afecte a todo el juego
    
    # 1. Dejamos pasto en la posición VIEJA
    mapa_actual[pos_p[0]][pos_p[1]] = random.choice(simbolos_pasto)
    
    # 2. Actualizamos la coordenada global
    pos_p[0], pos_p[1] = nueva_f, nueva_c
    
    # 3. Dibujamos al jugador en la NUEVA posición
    # Esto tiene que ser lo último para que quede "arriba"
    mapa_actual[pos_p[0]][pos_p[1]] = simbolos_especiales[0]

def elementos_no_reemplazables(nueva_f, nueva_c,anterior_pos):
    global pos_p 
    
    mapa_actual[pos_p[0]][pos_p[1]] = anterior_pos
    
   
    pos_p[0], pos_p[1] = nueva_f, nueva_c
    
    
    mapa_actual[pos_p[0]][pos_p[1]] = simbolos_especiales[0]
    
    


def cambio_de_mapa(numero_mapa, mapa_actual):
    global pos_p, simbolo_debajo
    
    # Verificamos si estamos pisando una entrada 'O'
    #UBICACION MAPA 2: PRADO
    if simbolo_debajo == "O":
        # De Prado (2) a Mercado (1)
        if numero_mapa == 2 and pos_p[1] == 0:
            respuesta = input("¿Deseas entrar al Mercado? S/N: ")
            if respuesta.lower() == "s":
                # LIMPIEZA: Antes de irnos, restauramos la 'O' en el mapa viejo
                mapa_actual[pos_p[0]][pos_p[1]] = "O"
                
                # CARGA: Generamos el nuevo mapa
                nuevo_mapa = generar_mapa_mercado_total()
                pos_p = [30, 128] # Nueva posición
                simbolo_debajo = "░" # Suelo del nuevo mapa
                
                return nuevo_mapa, 1 # Retornamos el nuevo objeto y el ID
            
        
        elif numero_mapa == 2 and pos_p[0] == 89:
            respuesta = input("¿Deseas entrar al Mercado? S/N: ")
            if respuesta.lower() == "s":
                # LIMPIEZA: Antes de irnos, restauramos la 'O' en el mapa viejo
                mapa_actual[pos_p[0]][pos_p[1]] = "O"
                
                # CARGA: Generamos el nuevo mapa
                nuevo_mapa = generar_mapa_cementerio()
                pos_p = [85, 73] # Nueva posición
                simbolo_debajo = simbolos_pasto[1] # Suelo del nuevo mapa
                
                
                return nuevo_mapa, 3 # Retornamos el nuevo objeto y el ID
            
        elif numero_mapa == 3 and pos_p[0] == 86:
            respuesta = input("¿Deseas entrar al Mercado? S/N: ")
            if respuesta.lower() == "s":
                # LIMPIEZA: Antes de irnos, restauramos la 'O' en el mapa viejo
                mapa_actual[pos_p[0]][pos_p[1]] = "O"
                
                # CARGA: Generamos el nuevo mapa
                nuevo_mapa = generar_mapa_prado()
                pos_p = [88, 65] # Nueva posición
                simbolo_debajo = "░"
                
                return nuevo_mapa, 2 # Nos movemos del cementerio al prado
            
        elif numero_mapa == 1 and pos_p[1] == 129:
            respuesta = input("¿Deseas salir del Mercado? S/N: ")
            if respuesta.lower() == "s":
                mapa_actual[pos_p[0]][pos_p[1]] = "O"
                
                nuevo_mapa = generar_mapa_prado()
                pos_p = [45, 1] # Volvemos a la posición de entrada del mapa anterior
                simbolo_debajo = "░" 
                
                return nuevo_mapa, 2
        
    
    return mapa_actual, numero_mapa
        

def obtener_tecla():
    # msvcrt.getch() lee un byte de la tecla presionada
    # .decode() lo transforma en un string normaL
    char = msvcrt.getch().decode('utf-8', errors='ignore').lower()
    
    
    return char


def procesar_entrada(tecla, inventario):
    
    # VALIDACIÓN: ¿Está la tecla en nuestro "diccionario" de permitidas?
    if tecla in TECLAS_MOVIMIENTO:
        mover(tecla, inventario)
    elif tecla == TECLAS_ACCION[3]: 
        pantalla_menu_en_juego(inventario)
    
    # Si no es ninguna, el juego no hace nada y sigue el bucle
    return "continuar"

def pantalla_menu_en_juego(inventario):
    en_menu = True
    
    while en_menu:
        os.system('cls' if os.name == 'nt' else 'clear') 
        print("=== MENÚ DE OPCIONES ===")
        print("I - Mostrar Inventario")
        print("E - Equipamiento")
        print("V - Volver al Juego")
        print("Q - Salir del Juego")
        print("========================")
        
        # Usamos obtener_tecla() para que sea instantáneo como el movimiento
        opcion = obtener_tecla() 

        if opcion == TECLAS_ACCION[1]: # 'i' para inventario
            manejar_inventario(inventario)
            input("\nPresioná Enter para volver al menú...") # Pausa para leer
        elif opcion == TECLAS_ACCION[0]: 
            print("\nAun no está listo...")
            input("\nPresioná Enter para continuar...")
        elif opcion == "v":
            en_menu = False # Esto rompe el bucle del menú y vuelve al mapa
        elif opcion == "q":
            print("\nSaliendo del juego...")
            exit() # Cierra el programa por completo
            
# Mobs
 # Símbolo para el Slime
simbolo_slime = "ζ" # Un carácter que parece una masita

# Lo agregamos a los bloqueantes para que no camines "sobre" ellos (o sí, si querés pelea)
simbolos_entornos_no_remplazables.append(simbolo_slime)

# Color en ESTILOS
ESTILOS.update({
    "ζ": "bold light_blue20" # Slime verde clásico
})       
        
# Lista para guardar la posición de cada slime y qué piso están pisando
lista_slimes = [
    {"pos": [40, 20], "debajo": "."},
    {"pos": [50, 60], "debajo": ","},
    {"pos": [30, 100], "debajo": "░"}
]
        
# BUCLE PRINCIPAL

def mover_slimes(mapa):
    global lista_slimes
    
    for slime in lista_slimes:
        f, c = slime["pos"]
        
        # 1. Elegir dirección al azar: (Arriba, Abajo, Izquierda, Derecha, Quieto)
        df, dc = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
        nf, nc = f + df, c + dc
        
        # 2. Verificar límites y colisiones
        # No pueden pisar muros (▒), otros NPCs, ni al jugador (P)
        if 0 <= nf < MAPA_REAL_ALTO and 0 <= nc < MAPA_REAL_ANCHO:
            celda_destino = mapa[nf][nc]
            
            if celda_destino in simbolos_pasto or celda_destino == "░":
                # Restaurar el piso donde estaba el slime
                mapa[f][c] = slime["debajo"]
                
                # Guardar el nuevo piso
                slime["debajo"] = celda_destino
                slime["pos"] = [nf, nc]
                
                # Dibujar el slime en la nueva posición
                mapa[nf][nc] = simbolo_slime
                
mapa_actual = generar_mapa_mercado_total()
numero_mapa = 1
pasos_jugador = 0

def iniciar_mapa(mapa_inicial, numero_inicial, inventario):
    # 1. Declaramos global al inicio para que Python sepa de qué hablamos
    global mapa_actual, pasos_jugador 
    
    mapa_actual = mapa_inicial
    m_actual = mapa_inicial
    n_mapa = numero_inicial
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')     
        dibujar_juego_centrado(hp, mp)
            
        tecla = obtener_tecla()
        procesar_entrada(tecla,inventario) 
        
        # 2. Lógica de Slimes corregida
        if n_mapa == 2: 
            pasos_jugador += 1
            if pasos_jugador % 2 == 0:
                # Usamos m_actual que es la matriz que se está renderizando
                mover_slimes(m_actual)
        
        mapa_antes = m_actual
        
        # 3. Cambio de mapa
        m_actual, n_mapa = cambio_de_mapa(n_mapa, m_actual)
        
        # 4. Si cambió, actualizamos la referencia global para que el resto del programa se entere
        if m_actual is not mapa_antes:
            mapa_actual = m_actual 

