import os
import random
import msvcrt # Librería para detectar teclas sin Enter (solo Windows)
from rich.console import Console
from rich.panel import Panel
from rich.align import Align


# Fundamentos Principales
# CConfiguracion tamaño del mapa
MAPA_REAL_ALTO = 90
MAPA_REAL_ANCHO = 130

# Definimos el tamaño de lo que se VE en pantalla (la cámara)
CAMARA_ALTO = 20
CAMARA_ANCHO = 40

# Simbolos para el mapa

simbolos_pasto = [",", ";", "'", "´"]

#Simbolos de entorno: 0: Espacio vacío, 1: Entrada de cueva, 2: Pared de cueva, 3: Pared de tréboles, 4: Piso de cueva
simbolos_entorno = [" ", "O", "#", "♣", "."]

#Simbolos especiales: 0: Jugador, 1: Ítem
simbolos_especiales = ["P", "*"]

# Informacion del personaje 
pos_p = [1, 1] # Fila, Columna
inventario = []

mp = 50
hp = 100
stats_jugador = [mp, hp]

console = Console()

#Tipos de Items
#Maatriz de Items 1: 1 Fila Pociones Buenas 2: 2 Fila Items Buenos : 3 Fila Equipamiento Bueno : 4 Fila Pociones Malas 2: 5 Fila Items Malos : 6 Fila Equipamiento Malo 
#Matriz 6 x 3 

items = {"Pociones buenas": ["Pocion de Fuerza Grande","Pocion de HP pequeña","Poción de HP Grande"],
         "Accesorios buenas": ["Gema de vida","Hacha de Mitril","Latigo con Puas"],
         "Equipamiento buenas": ["Escudo de Obsidiana","Caso de Tungsteno","Pechera de escamas de Dragon"],
         "Pociones malas" : ["Pocion Alucinogena","Pocion de Potencia / Impotencia","Pocion de I have no enemies"],
         "Accesorios malas": ["Escudo del Heroe ;)","Lanza Maldita","Espada de Doble Filo Maldita"],
         "Equipamiento malas": ["Collar Paralizante","Guantes Benevolentes","Casco de Dullahan"]
}


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
    ".": "bold grey30"               # Piso de cueva
}


#Que deberia
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
                    
# 1. CREAR EL MAPA (Matriz)
def generar_mapa():
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
    for _ in range(7):
        f_rand, c_rand = random.randint(1, MAPA_REAL_ALTO-2), random.randint(1, MAPA_REAL_ANCHO-2)
        mapa[f_rand][c_rand] = simbolos_especiales[1] # Ítem 
        
    mapa[pos_p[0]][pos_p[1]] = simbolos_especiales[0] # Colocamos al jugador
    
    generar_cueva(mapa, 10, 10, 6, 4)
    
    return mapa

mapa_actual = generar_mapa()

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
def mover(tecla):
    global pos_p
    df, dc = 0, 0
    if tecla == TECLAS_MOVIMIENTO[2]: df = 1
    elif tecla == TECLAS_MOVIMIENTO[0]: df = -1
    elif tecla == TECLAS_MOVIMIENTO[1]: dc = -1
    elif tecla == TECLAS_MOVIMIENTO[3]: dc = 1
    else: return

    nueva_f = pos_p[0] + df
    nueva_c = pos_p[1] + dc
    

    # Verificamos colisión con pared (En este caso, la pared de tréboles '♣' es la que bloquea el paso) y que no sea la pared de la cueva #
    if mapa_actual[nueva_f][nueva_c] != simbolos_entorno[3] and mapa_actual[nueva_f][nueva_c] != simbolos_entorno[2]:
        # Si hay un ítem, lo recolectamos
        if mapa_actual[nueva_f][nueva_c] == simbolos_especiales[1]:
            respuesta = ""
            respuesta = input("¿Deseas Recoger el Objeto? S/N: ")
            if respuesta == "s" or respuesta == "S":
                inventario.append(items[random.choice(list(items.keys()))][random.randint(0,2)])
                
        # Actualizamos matriz: borramos viejo, ponemos nuevo
        anterior_pos = ""
       
        anterior_pos = mapa_actual[pos_p[0]][pos_p[1]]
        mapa_actual[pos_p[0]][pos_p[1]] = simbolos_pasto[random.randint(0, len(simbolos_pasto) - 1)]
        pos_p = [nueva_f, nueva_c]
        mapa_actual[pos_p[0]][pos_p[1]] = simbolos_especiales[0]
        pos_p = [nueva_f, nueva_c]
        mapa_actual[pos_p[0]][pos_p[1]] = anterior_pos

# ... (Mantené tus variables ANCHO, ALTO y pos_p igual) ...

def obtener_tecla():
    # msvcrt.getch() lee un byte de la tecla presionada
    # .decode() lo transforma en un string normaL
    char = msvcrt.getch().decode('utf-8', errors='ignore').lower()
    
    
    return char

def mostrar_inventario():
    print(inventario)


def procesar_entrada(tecla):
    
    # VALIDACIÓN: ¿Está la tecla en nuestro "diccionario" de permitidas?
    if tecla in TECLAS_MOVIMIENTO:
        mover(tecla)
    elif tecla == TECLAS_ACCION[3]: 
        pantalla_menu_en_juego()
    
    # Si no es ninguna, el juego no hace nada y sigue el bucle
    return "continuar"

def pantalla_menu_en_juego():
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
            mostrar_inventario()
            input("\nPresioná Enter para volver al menú...") # Pausa para leer
        elif opcion == TECLAS_ACCION[0]: 
            print("\nAun no está listo...")
            input("\nPresioná Enter para continuar...")
        elif opcion == "v":
            en_menu = False # Esto rompe el bucle del menú y vuelve al mapa
        elif opcion == "q":
            print("\nSaliendo del juego...")
            exit() # Cierra el programa por completo
        
# BUCLE PRINCIPAL

def iniciar_mapa_recoleccion():
    dibujar_juego_centrado(hp,mp)   

    while True:
        dibujar_juego_centrado(hp,mp)   
        # getch() PAUSA el programa hasta que toques una tecla
        # Agregamos un try/except por si tocan teclas raras (Clase 10 del cronograma)
        tecla = obtener_tecla()
        procesar_entrada(tecla)


iniciar_mapa_recoleccion()